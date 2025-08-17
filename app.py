#!/usr/bin/env python3
"""
Harmful Meme Detection API
Using YOLOv5 for detecting harmful vs normal memes
"""

import os
import io
import json
import base64
import torch
import logging
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from pathlib import Path
import tempfile

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Model configuration
MODEL_PATH = os.environ.get('MODEL_PATH', 'yolov5s.pt')
CONFIDENCE_THRESHOLD = float(os.environ.get('CONFIDENCE_THRESHOLD', '0.5'))

# Initialize model
model = None

def load_model():
    """Load YOLOv5 model"""
    global model
    try:
        # Clone YOLOv5 if not exists
        if not os.path.exists('yolov5'):
            os.system('git clone https://github.com/ultralytics/yolov5.git')
        
        # Load model
        import sys
        sys.path.insert(0, 'yolov5')
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=MODEL_PATH, force_reload=True)
        model.conf = CONFIDENCE_THRESHOLD
        logger.info(f"Model loaded successfully from {MODEL_PATH}")
        return True
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        # Fallback to pretrained model
        try:
            model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
            model.conf = CONFIDENCE_THRESHOLD
            logger.info("Loaded pretrained YOLOv5s model as fallback")
            return True
        except Exception as e2:
            logger.error(f"Failed to load fallback model: {e2}")
            return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'version': '1.0.0'
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict if a meme is harmful or normal
    Accepts image in base64 or as file upload
    """
    try:
        if model is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        # Get image from request
        image = None
        
        # Check if image is in JSON body (base64)
        if request.json and 'image' in request.json:
            image_data = base64.b64decode(request.json['image'])
            image = Image.open(io.BytesIO(image_data))
        
        # Check if image is uploaded as file
        elif 'image' in request.files:
            image = Image.open(request.files['image'].stream)
        
        else:
            return jsonify({'error': 'No image provided'}), 400
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Save to temp file for processing
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            image.save(tmp_file.name)
            
            # Run inference
            results = model(tmp_file.name)
            
            # Clean up temp file
            os.unlink(tmp_file.name)
        
        # Process results
        detections = results.pandas().xyxy[0].to_dict(orient='records')
        
        # Classify as harmful or normal based on detections
        # This is a simplified classification - adjust based on actual model output
        is_harmful = False
        confidence = 0.0
        
        if detections:
            # Check if any detection indicates harmful content
            for det in detections:
                if 'harmful' in str(det.get('name', '')).lower():
                    is_harmful = True
                    confidence = max(confidence, det.get('confidence', 0))
                elif 'normal' not in str(det.get('name', '')).lower():
                    # If detection is not explicitly normal, consider it potentially harmful
                    is_harmful = True
                    confidence = max(confidence, det.get('confidence', 0) * 0.7)
        
        # Return classification result
        return jsonify({
            'harmful': is_harmful,
            'confidence': float(confidence),
            'classification': 'harmful' if is_harmful else 'normal',
            'detections': detections,
            'message': 'Meme classified successfully'
        })
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/info', methods=['GET'])
def info():
    """Get model information"""
    return jsonify({
        'model': 'YOLOv5 Harmful Meme Detector',
        'version': '1.0.0',
        'description': 'Detects whether a meme is harmful or normal',
        'confidence_threshold': CONFIDENCE_THRESHOLD,
        'classes': ['harmful', 'normal'],
        'endpoints': {
            '/health': 'Health check',
            '/predict': 'Predict meme classification (POST)',
            '/info': 'Model information (GET)'
        }
    })

@app.route('/', methods=['GET'])
def index():
    """Root endpoint with API documentation"""
    return jsonify({
        'title': 'Harmful Meme Detection API',
        'description': 'YOLOv5-based API for detecting harmful memes',
        'usage': {
            'endpoint': '/predict',
            'method': 'POST',
            'body': {
                'option1': 'JSON with base64 image: {"image": "base64_string"}',
                'option2': 'Multipart form with image file upload'
            }
        },
        'response': {
            'harmful': 'boolean',
            'confidence': 'float (0-1)',
            'classification': 'string (harmful/normal)',
            'detections': 'array of detected objects'
        }
    })

if __name__ == '__main__':
    # Load model on startup
    if not load_model():
        logger.warning("Starting without model - predictions will fail")
    
    # Get port from environment or default
    port = int(os.environ.get('PORT', 5000))
    
    # Run app
    app.run(host='0.0.0.0', port=port, debug=False)
