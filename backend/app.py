from flask import Flask, request, jsonify
import os
from classify_utils import process_file
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS
CORS(app)

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return "please work!"

@app.route("/api/ping", methods=['GET'])
def ping():
    return jsonify({"message": "Pong!"})

@app.route('/upload', methods=['POST'])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    try:
        endpoint_arn = "arn:aws:comprehend:ap-south-1:155125051066:document-classifier-endpoint/checkerrors"
        results = process_file(endpoint_arn, filepath)
    except ValueError as e:
        os.remove(filepath)
        return jsonify({"error": str(e)}), 400

    return jsonify({"results": results})
    # return jsonify({"message": f"File {file.filename} uploaded successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
