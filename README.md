# Image Moderation API 🖼️

A robust Flask-based REST API that leverages Google Cloud Vision AI for detecting and moderating inappropriate image content. This service provides comprehensive image analysis through SafeSearch detection and label detection, suitable for applications requiring content moderation.

## 🌟 Features

- **Flexible Input Methods**
  - URL submission
  - Base64 encoded images
  - Direct file upload

- **Multiple Content Type Support**
  - `multipart/form-data`
  - `application/json`
  - `application/x-www-form-urlencoded`

- **Advanced Image Analysis**
  - Google Cloud Vision AI integration
  - SafeSearch detection
  - Label detection for inappropriate content
  - Comprehensive content classification

- **API Features**
  - CORS enabled
  - Robust error handling
  - Detailed logging
  - Request timeout management

## 🚀 Quick Start

1. **Install Dependencies**
```bash
pip install poetry
poetry install
```

2. **Configure Google Cloud**
   - Place your service account JSON in project root
   - Set environment variable:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"
   ```

3. **Launch the API**
```bash
python main.py
```

## 📡 API Reference

### POST /upload

Analyzes images for inappropriate content through multiple input methods.

#### Input Methods

1. **JSON Request**
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/image.jpg"}' \
  https://your-api-endpoint/upload
```

2. **URL-encoded Form**
```bash
curl -X POST \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data "url=https://example.com/image.jpg" \
  https://your-api-endpoint/upload
```

3. **Multipart Form**
```bash
curl -X POST \
  -F "image=@/path/to/local/image.jpg" \
  https://your-api-endpoint/upload
```

#### Response Format

```json
{
  "is_appropriate": true|false,
  "message": "Analysis result description",
  "analysis": {
    "adult": "VERY_UNLIKELY",
    "violence": "VERY_UNLIKELY",
    "racy": "VERY_UNLIKELY"
  }
}
```

#### Status Codes

| Code | Description |
|------|-------------|
| 200 | Successful analysis |
| 400 | Bad Request - Invalid input |
| 415 | Unsupported Media Type |
| 500 | Internal Server Error |

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|-----------|
| GOOGLE_APPLICATION_CREDENTIALS | Path to service account JSON | Yes |
| FLASK_ENV | Development/Production mode | No |
| PORT | API port (default: 5000) | No |

### Dependencies

```toml
[tool.poetry.dependencies]
python = ">=3.10.0,<3.12"
flask = "^2.0.1"
google-cloud-vision = "^3.1.0"
Pillow = "^9.0.0"
requests = "^2.27.1"
flask-cors = "^3.0.10"
```

## 🛡️ Security Features

- **Input Validation**
  - Content type verification
  - Image format validation
  - File size limits
  - URL validation

- **Content Analysis**
  - Adult content detection
  - Violence detection
  - Racy content detection
  - Custom label detection

- **Request Protection**
  - Timeout handling
  - Rate limiting
  - CORS configuration

## 🔍 Error Handling

The API provides detailed error responses:

```json
{
  "error": "Error description",
  "code": "ERROR_CODE",
  "details": {}
}
```

### Common Error Scenarios

| Error Code | Description | HTTP Status |
|------------|-------------|-------------|
| INVALID_INPUT | Malformed request data | 400 |
| UNSUPPORTED_TYPE | Invalid content type | 415 |
| ANALYSIS_FAILED | Vision API error | 500 |
| URL_ERROR | Invalid or inaccessible URL | 400 |

## 📊 Performance Considerations

- **Rate Limits**
  - Google Cloud Vision API quotas apply
  - Consider implementing client-side rate limiting

- **Image Size**
  - Maximum file size: 10MB
  - Recommended dimensions: ≤ 4096px
  - Supported formats: JPG, PNG, GIF

## 🚧 Development

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/image-moderation-api.git
cd image-moderation-api
```

2. Install dependencies:
```bash
poetry install
```

3. Set up pre-commit hooks:
```bash
pre-commit install
```

### Testing

Run the test suite:
```bash
poetry run pytest
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📮 Support

For support or queries:
- Open an issue in the GitHub repository
- Contact the maintainers
- Check the [Wiki](wiki) for additional documentation