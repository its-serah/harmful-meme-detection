# Deployment Guide for Harmful Meme Detection API

## Repository Information
- **GitHub Repository**: https://github.com/its-serah/harmful-meme-detection
- **Technology Stack**: Python, Flask, YOLOv5, Docker
- **API Port**: 5000

## Quick Deploy Options

### Option 1: Deploy with Docker Compose (Recommended)
```bash
# Clone the repository
git clone https://github.com/its-serah/harmful-meme-detection.git
cd harmful-meme-detection

# Deploy using the script
./deploy.sh up -d

# Or manually with docker-compose
docker-compose up --build -d
```

### Option 2: Deploy to Heroku
```bash
# Install Heroku CLI first
# Create Heroku app
heroku create your-app-name

# Deploy using container
heroku container:push web
heroku container:release web
```

### Option 3: Deploy to Railway
1. Fork the repository
2. Go to https://railway.app
3. Create new project from GitHub
4. Select the forked repository
5. Railway will auto-detect Dockerfile and deploy

### Option 4: Deploy to Render
1. Go to https://render.com
2. Create new Web Service
3. Connect GitHub repository
4. Select Docker runtime
5. Deploy

### Option 5: Deploy to Google Cloud Run
```bash
# Build and submit to Google Container Registry
gcloud builds submit --tag gcr.io/YOUR-PROJECT-ID/harmful-meme-detector

# Deploy to Cloud Run
gcloud run deploy harmful-meme-detector \
  --image gcr.io/YOUR-PROJECT-ID/harmful-meme-detector \
  --platform managed \
  --allow-unauthenticated \
  --port 5000
```

### Option 6: Deploy to AWS ECS
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR-ECR-URI
docker build -t harmful-meme-detector .
docker tag harmful-meme-detector:latest YOUR-ECR-URI/harmful-meme-detector:latest
docker push YOUR-ECR-URI/harmful-meme-detector:latest

# Create ECS task and service through AWS Console or CLI
```

### Option 7: Deploy to DigitalOcean App Platform
1. Push code to GitHub
2. Go to DigitalOcean App Platform
3. Create new app from GitHub
4. Select repository
5. Choose Dockerfile as build type
6. Deploy

## API Endpoints

### Base URL
```
http://your-domain:5000
```

### Available Endpoints
- `GET /` - API documentation
- `GET /health` - Health check
- `GET /info` - Model information
- `POST /predict` - Predict meme classification

## Testing the Deployment

### Test with cURL
```bash
# Health check
curl http://localhost:5000/health

# Get model info
curl http://localhost:5000/info

# Test prediction with image
curl -X POST -F "image=@test_meme.jpg" http://localhost:5000/predict
```

### Test with Python
```python
import requests
import base64

# Test health
response = requests.get('http://localhost:5000/health')
print(response.json())

# Test prediction
with open('test_meme.jpg', 'rb') as f:
    image_base64 = base64.b64encode(f.read()).decode()

response = requests.post(
    'http://localhost:5000/predict',
    json={'image': image_base64}
)
print(response.json())
```

## Environment Variables

Configure these for production:
- `MODEL_PATH` - Path to model weights (default: `yolov5s.pt`)
- `CONFIDENCE_THRESHOLD` - Detection confidence (default: `0.5`)
- `PORT` - API port (default: `5000`)

## Monitoring

### View Logs
```bash
# Docker Compose logs
docker-compose logs -f

# Or using deployment script
./deploy.sh logs
```

### Health Monitoring
Set up monitoring to check `/health` endpoint every 30 seconds.

## Scaling

### Horizontal Scaling
```yaml
# In docker-compose.yml, add:
deploy:
  replicas: 3
```

### Load Balancing
Use nginx or HAProxy in front of multiple container instances.

## Troubleshooting

### Container won't start
- Check logs: `docker-compose logs`
- Verify port 5000 is not in use: `lsof -i :5000`

### Model not loading
- Ensure model file exists in `models/` directory
- Check MODEL_PATH environment variable

### Out of memory
- Increase Docker memory limit
- Use smaller batch size in model configuration

## Security Considerations

1. Use HTTPS in production (add nginx reverse proxy with SSL)
2. Implement rate limiting
3. Add API key authentication for production
4. Validate and sanitize all inputs
5. Set up CORS properly for your domain

## Support

For issues or questions, open an issue on GitHub:
https://github.com/its-serah/harmful-meme-detection/issues
