# Document Summarizer API 📄✨

A production-style FastAPI service that summarizes text documents with rate limiting, input validation, and health monitoring.

## Features

✅ Extractive text summarization using frequency-based ranking  
✅ Rate limiting (10 requests/minute per IP)  
✅ Input size validation (max 50KB)  
✅ Health check endpoint with uptime  
✅ File upload support (.txt, .md)  
✅ Auto-generated interactive docs  
✅ Comprehensive error handling  

## Tech Stack

- **FastAPI**: Modern, fast web framework
- **NLTK**: Natural language processing
- **Pydantic**: Data validation
- **Pytest**: Testing framework

## Quick Start

### 1. Clone & Setup
\`\`\`bash
git clone https://github.com/yourusername/document-summarizer.git
cd document-summarizer
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
\`\`\`

### 2. Run the Server
\`\`\`bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
\`\`\`

### 3. Access Docs
Open http://localhost:8000/docs

## API Endpoints

### GET /health
Check API status and readiness
\`\`\`json
{
  "status": "healthy",
  "version": "1.0.0",
  "model_ready": true,
  "requests_remaining": 10
}
\`\`\`

### POST /summarize
Summarize text input
\`\`\`bash
curl -X POST "http://localhost:8000/summarize" \\
  -H "Content-Type: application/json" \\
  -d '{
    "text": "Your long document text here...",
    "max_sentences": 5
  }'
\`\`\`

**Response:**
\`\`\`json
{
  "summary": "Key sentences extracted...",
  "original_length": 1500,
  "summary_length": 450,
  "sentences_count": 5,
  "truncated": true
}
\`\`\`

### POST /upload-summarize
Upload and summarize a file
\`\`\`bash
curl -X POST "http://localhost:8000/upload-summarize" \\
  -F "file=@document.txt" \\
  -F "max_sentences=5"
\`\`\`

## Rate Limits & Constraints

| Feature | Limit |
|---------|-------|
| Requests per minute | 10 per IP |
| Max input size | 50KB |
| Min text length | 100 chars |
| Max sentences | 20 |

## Testing

\`\`\`bash
pytest tests/ -v
\`\`\`

## Project Structure

\`\`\`
document-summarizer/
├── app/
│   ├── main.py          # FastAPI app & routes
│   ├── models.py        # Pydantic schemas
│   ├── summarizer.py    # Core summarization logic
│   ├── middleware.py    # Rate limit & size checks
│   └── config.py        # Settings
├── tests/
│   └── test_api.py      # API tests
├── requirements.txt
└── README.md
\`\`\`

## Configuration

Edit `app/config.py` to adjust:
- `max_content_length`: Max payload size
- `rate_limit_requests`: Requests per window
- `rate_limit_window`: Time window (seconds)
- `summary_ratio`: Summary length ratio

## Error Handling

- **400**: Invalid input (too short, wrong format)
- **413**: Content too large
- **422**: Validation error
- **429**: Rate limit exceeded
- **500**: Server error

## Next Steps

- [ ] Add caching for repeated documents
- [ ] Integrate transformer-based summarization
- [ ] Multi-language support
- [ ] User authentication & API keys
- [ ] Async document URL fetching

## Contributing

Pull requests welcome! Please add tests for new features.

## License

MIT License - see LICENSE file

## Author

**Aradhay Sharma**  
Class 11 Student | Aspiring AI/ML Engineer  
SNBP International School, Pune  

📧 sharmaaradhayasharma@gmail.com
🔗 https://www.linkedin.com/in/aradhay-sharma-660a14305/ 
💻 https://github.com/aradhaysharma673

---

Built with 💙 using FastAPI
\`\`\`

---

## File 12: `LICENSE`
