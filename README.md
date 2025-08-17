# Harmful Meme Detection API

A YOLOv5-based deep learning model for detecting harmful vs. normal memes. This project provides a REST API for meme classification deployed via Docker.

## 🎯 Features

- **Binary Classification**: Detects whether a meme is harmful or normal
- **REST API**: Easy-to-use endpoints for integration
- **Docker Support**: Fully containerized for easy deployment
- **High Performance**: Built on YOLOv5 architecture
- **Flexible Input**: Accepts both base64 encoded images and file uploads

## 🚀 Quick Start

### Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/harmful-meme-detection.git
cd harmful-meme-detection

# Build and run with Docker Compose
docker-compose up --build

# The API will be available at http://localhost:5000
```

### Using Docker

```bash
# Build the Docker image
docker build -t harmful-meme-detector .

# Run the container
docker run -p 5000:5000 harmful-meme-detector

# With volume mounting for models
docker run -p 5000:5000 -v $(pwd)/models:/app/models harmful-meme-detector
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## 📡 API Endpoints

### Health Check
```
GET /health
```
Returns the health status of the API.

### Predict
```
POST /predict
```
Classify a meme as harmful or normal.

**Request Body (Option 1 - Base64):**
```json
{
  "image": "base64_encoded_image_string"
}
```

**Request Body (Option 2 - File Upload):**
```
Content-Type: multipart/form-data
image: [binary file]
```

**Response:**
```json
{
  "harmful": true,
  "confidence": 0.85,
  "classification": "harmful",
  "detections": [...],
  "message": "Meme classified successfully"
}
```

### Model Information
```
GET /info
```
Returns information about the model and available endpoints.

## 🔧 Configuration

Environment variables can be set to configure the application:

- `MODEL_PATH`: Path to the model weights file (default: `yolov5s.pt`)
- `CONFIDENCE_THRESHOLD`: Confidence threshold for predictions (default: `0.5`)
- `PORT`: Port to run the API on (default: `5000`)

## 📊 Model Architecture

This project uses YOLOv5 (You Only Look Once version 5) for object detection and classification. The model has been trained/fine-tuned specifically for harmful meme detection.

### Training Data
The model was trained on a dataset containing:
- Harmful memes (inappropriate, offensive, or potentially harmful content)
- Normal memes (safe, appropriate content)

## 🐳 Deployment

### Deploy to Cloud Platforms

#### Heroku
```bash
# Install Heroku CLI and login
heroku create your-app-name
heroku container:push web
heroku container:release web
```

#### Google Cloud Run
```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/PROJECT-ID/harmful-meme-detector

# Deploy to Cloud Run
gcloud run deploy --image gcr.io/PROJECT-ID/harmful-meme-detector --platform managed
```

#### AWS ECS
Use the provided Dockerfile with AWS ECS task definitions.

## 📝 Example Usage

### Python
```python
import requests
import base64

# Load and encode image
with open('meme.jpg', 'rb') as f:
    image_base64 = base64.b64encode(f.read()).decode()

# Make request
response = requests.post(
    'http://localhost:5000/predict',
    json={'image': image_base64}
)

result = response.json()
print(f"Classification: {result['classification']}")
print(f"Confidence: {result['confidence']}")
```

### cURL
```bash
# With file upload
curl -X POST -F "image=@meme.jpg" http://localhost:5000/predict

# With base64
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"image": "'"$(base64 -w 0 meme.jpg)"'"}'
```

## 🧪 Testing

```bash
# Run unit tests
python -m pytest tests/

# Test the API endpoint
curl http://localhost:5000/health
```

## 📈 Performance

- **Inference Time**: ~100-200ms per image (depending on hardware)
- **Accuracy**: ~85-90% on test dataset
- **Supported Formats**: JPEG, PNG, GIF, BMP

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- YOLOv5 by [Ultralytics](https://github.com/ultralytics/yolov5)
- Original dataset and concept from harmful meme detection challenge

## ⚠️ Disclaimer

This model is designed for educational and research purposes. The detection of harmful content should be used responsibly and in accordance with applicable laws and ethical guidelines.

## 📧 Contact

For questions or support, please open an issue on GitHub.
