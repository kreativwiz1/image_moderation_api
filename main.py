from flask import Flask, request, jsonify
from flask_cors import CORS
import io
import os
import requests
import logging
from google.cloud import vision
from PIL import Image
from io import BytesIO
import base64

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for the entire app
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set the environment variable for Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "kinetic-anvil-437123-r1-1330863832b9.json"

def detect_safe_search(image_content):
    """Detect SafeSearch attributes in the image using Google Cloud Vision API."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    try:
        response = client.safe_search_detection(image=image)
        safe = response.safe_search_annotation

        return {
            'adult': safe.adult,
            'violence': safe.violence,
            'racy': safe.racy,
            'spoof': safe.spoof,
            'medical': safe.medical,
        }
    except Exception as e:
        logging.error(f"Error in detect_safe_search: {e}")
        return None

def detect_labels(image_content):
    """Detect labels in the image using Google Cloud Vision API."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    try:
        response = client.label_detection(image=image)
        return response.label_annotations
    except Exception as e:
        logging.error(f"Error in detect_labels: {e}")
        return None

def analyze_image(image_content):
    """Analyze the image using both SafeSearch and Label Detection."""
    try:
        # Perform SafeSearch detection
        safe_search_results = detect_safe_search(image_content)
        if safe_search_results is None:
            logging.error("SafeSearch detection failed")
            return False

        # Check SafeSearch results
        safe_search_flag = False
        if (safe_search_results['adult'] >= 2 or 
            safe_search_results['violence'] >= 2 or 
            safe_search_results['racy'] >= 2):
            safe_search_flag = True
            logging.info(f"SafeSearch flagged: {safe_search_results}")

        # Perform Label Detection
        labels = detect_labels(image_content)
        if labels is None:
            logging.error("Label detection failed")
            return False

        # Define inappropriate labels
        inappropriate_labels = {
            "gun", "knife", "weapon", "nude", "pornography", "child",
            "firearm", "pistol", "sword", "dagger", 
            "assault rifle", "machine gun", "violence", "blood",
            "sexual", "explicit", "adult", "underage"
        }

        # Check each label for inappropriate content
        label_flag = False
        for label in labels:
            if label.description.lower() in inappropriate_labels and label.score >= 0.5:
                label_flag = True
                logging.info(f"Inappropriate label detected: {label.description}")
                break

        # Final Decision
        return not (safe_search_flag or label_flag)
    except Exception as e:
        logging.error(f"Error in analyze_image: {e}")
        return False

def fetch_image_from_url(image_url):
    """Fetch image content from a URL, ensuring it's an image."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(image_url, headers=headers, timeout=10)
        response.raise_for_status()

        content_type = response.headers.get('Content-Type', '')
        if 'image' not in content_type:
            logging.error(f"Invalid content type: {content_type}")
            return None

        image = Image.open(BytesIO(response.content))
        byte_arr = BytesIO()
        image.save(byte_arr, format='PNG')
        return byte_arr.getvalue()
    except requests.RequestException as e:
        logging.error(f"Error fetching image from URL: {e}")
    except IOError as e:
        logging.error(f"Error processing image: {e}")
    except Exception as e:
        logging.error(f"Unexpected error in fetch_image_from_url: {e}")
    return None

@app.route('/upload', methods=['POST'])
def upload_image():
    """Endpoint to upload an image or provide an image URL for moderation."""
    try:
        content_type = request.content_type or ''
        logging.info(f"Content-Type: {content_type}")

        # Initialize image_content
        image_content = None

        # Handle multipart/form-data
        if 'multipart/form-data' in content_type:
            if 'url' in request.form:
                image_url = request.form['url']
                image_content = fetch_image_from_url(image_url)
            elif 'file' in request.files:
                file = request.files['file']
                image_content = file.read()
            else:
                return jsonify({'error': 'No file or URL provided in form data'}), 400

        # Handle JSON data
        elif request.is_json:
            data = request.get_json()
            if 'file' in data:
                image_content = base64.b64decode(data['file'])
            elif 'url' in data:
                image_url = data['url']
                image_content = fetch_image_from_url(image_url)
            else:
                return jsonify({'error': 'No file or URL provided in JSON'}), 400

        # Handle URL-encoded form data
        elif content_type == 'application/x-www-form-urlencoded':
            if 'url' in request.form:
                image_url = request.form['url']
                image_content = fetch_image_from_url(image_url)
            else:
                return jsonify({'error': 'No URL provided in form data'}), 400

        else:
            return jsonify({'error': f'Unsupported content type: {content_type}. Supported types are multipart/form-data, application/json, and application/x-www-form-urlencoded'}), 415

        if image_content is None:
            return jsonify({'error': 'Could not fetch or process image'}), 400

        # Analyze the image using SafeSearch and Label Detection
        is_appropriate = analyze_image(image_content)

        return jsonify({
            'message': 'Image is appropriate for upload.' if is_appropriate else 'Image is inappropriate and cannot be uploaded.',
            'is_appropriate': is_appropriate
        }), 200

    except Exception as e:
        logging.error(f"Unexpected error in upload_image: {e}")
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)