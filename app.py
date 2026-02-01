import os
import base64
import requests
from flask import Flask, request, render_template, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
from stegano import lsb  # Changed this import
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# --- Configuration ---
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
SECRET_KEY = os.urandom(24)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
IMAGEN_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={GOOGLE_API_KEY}"

# --- Flask App Initialization ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Helper Functions ---
def allowed_file(filename):
    """Checks if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_image_from_prompt(prompt: str) -> bytes:
    """
    Calls the Google AI API (Imagen 3) to generate an image from a text prompt.
    Returns the image data as bytes.
    """
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not found. Please set it in the .env file.")

    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {"sampleCount": 1}
    }
    headers = {'Content-Type': 'application/json'}

    response = requests.post(IMAGEN_API_URL, json=payload, headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

    result = response.json()
    if "predictions" not in result or not result["predictions"]:
        raise ValueError("API did not return any predictions.")

    base64_image_data = result["predictions"][0].get("bytesBase64Encoded")
    if not base64_image_data:
        raise ValueError("API response did not contain image data.")

    return base64.b64decode(base64_image_data)


# --- Flask Routes ---
@app.route('/', methods=['GET'])
def index():
    """Renders the main page with encode and decode forms."""
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    """
    Handles the encoding process: generates image, hides message,
    and serves the final image for download.
    """
    prompt = request.form.get('prompt')
    secret_message = request.form.get('secret_message')

    if not prompt or not secret_message:
        flash("Both an image prompt and a secret message are required.", "error")
        return redirect(url_for('index'))
    
    if not GOOGLE_API_KEY:
        flash("Server is not configured with a Google API Key.", "error")
        return redirect(url_for('index'))

    try:
        # 1. Generate the image
        image_bytes = generate_image_from_prompt(prompt)

        # 2. Save the generated image temporarily
        original_image_path = os.path.join(app.config['UPLOAD_FOLDER'], "original_image.png")
        with open(original_image_path, "wb") as f:
            f.write(image_bytes)

        # 3. Encode the secret message into the image using stegano
        encoded_image_path = os.path.join(app.config['UPLOAD_FOLDER'], "encoded_image.png")
        secret_image = lsb.hide(original_image_path, secret_message)
        secret_image.save(encoded_image_path)

        # 4. Send the final image to the user for download
        return send_file(
            encoded_image_path,
            mimetype='image/png',
            as_attachment=True,
            download_name='secret-image.png'
        )

    except requests.exceptions.RequestException as e:
        flash(f"Error communicating with Google AI API: {e}", "error")
    except ValueError as e:
        flash(f"An error occurred: {e}", "error")
    except Exception as e:
        # General catch-all for other errors, including steganography errors
        flash(f"An unexpected error occurred during encoding: {e}", "error")

    return redirect(url_for('index'))


@app.route('/decode', methods=['POST'])
def decode():
    """
    Handles the decoding process: user uploads an image,
    the app extracts and displays the hidden message.
    """
    if 'file' not in request.files:
        flash('No file part in the request.', 'error')
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading.', 'error')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # Decode the message from the uploaded image using stegano
            decoded_message = lsb.reveal(filepath)
            if decoded_message:
                 flash("Decoding successful!", "success")
                 return render_template('index.html', decoded_message=decoded_message)
            else:
                 flash("Could not find a hidden message in the image.", "warning")

        except Exception as e:
            flash(f"An error occurred during decoding: {e}", "error")

        finally:
            # Clean up the uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
    else:
        flash('Allowed image types are .png, .jpg, .jpeg', 'error')

    return redirect(url_for('index'))


# --- Main Execution ---
if __name__ == '__main__':
    app.run(debug=True)