from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from app.models import SummarizeRequest, SummarizeResponse, HealthResponse
from app.summarizer import summarizer
from app.middleware import RateLimitMiddleware, ContentSizeMiddleware
from app.config import settings
import time

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="A production-style document summarization API with rate limiting and health checks"
)

# Add middleware
app.add_middleware(RateLimitMiddleware)
app.add_middleware(ContentSizeMiddleware)

# Store app start time for health check
app.state.start_time = time.time()

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Document Summarizer API",
        "version": settings.version,
        "endpoints": {
            "health": "/health",
            "summarize": "/summarize",
            "upload": "/upload-summarize",
            "docs": "/docs"
        }
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Check API health and readiness"""
    uptime = time.time() - app.state.start_time
    
    return HealthResponse(
        status="healthy",
        version=settings.version,
        model_ready=True,
        requests_remaining=settings.rate_limit_requests
    )

@app.post("/summarize", response_model=SummarizeResponse, tags=["Summarization"])
async def summarize_text(request: SummarizeRequest):
    """
    Summarize text with extractive summarization
    
    - **text**: Input text (100-50000 chars)
    - **max_sentences**: Maximum sentences in summary (1-20)
    """
    try:
        result = summarizer.summarize(
            text=request.text,
            max_sentences=request.max_sentences
        )
        
        return SummarizeResponse(**result)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Summarization failed: {str(e)}"
        )

@app.post("/upload-summarize", response_model=SummarizeResponse, tags=["Summarization"])
async def summarize_file(
    file: UploadFile = File(...),
    max_sentences: int = 5
):
    """
    Upload and summarize a text file
    
    - **file**: Text or markdown file (.txt, .md)
    - **max_sentences**: Maximum sentences in summary
    """
    # Validate file type
    if not file.filename.endswith(('.txt', '.md')):
        raise HTTPException(
            status_code=400,
            detail="Only .txt and .md files are supported"
        )
    
    # Read file content
    try:
        content = await file.read()
        text = content.decode('utf-8')
        
        if len(text) < 100:
            raise HTTPException(
                status_code=400,
                detail="File content too short (minimum 100 characters)"
            )
        
        if len(text) > settings.max_content_length:
            raise HTTPException(
                status_code=413,
                detail=f"File too large (max {settings.max_content_length} bytes)"
            )
        
        result = summarizer.summarize(text=text, max_sentences=max_sentences)
        return SummarizeResponse(**result)
    
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="File must be valid UTF-8 text"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Processing failed: {str(e)}"
        )

@app.exception_handler(413)
async def content_too_large_handler(request, exc):
    return JSONResponse(
        status_code=413,
        content={
            "detail": f"Content too large. Maximum size: {settings.max_content_length} bytes",
            "max_size": settings.max_content_length
        }
    )

@app.exception_handler(429)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={
            "detail": str(exc.detail),
            "rate_limit": settings.rate_limit_requests,
            "window_seconds": settings.rate_limit_window
        }
    )
