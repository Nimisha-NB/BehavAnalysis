from flask import Flask, request, jsonify
import os,chardet
from toExcel_forPredictions import process_file_and_store
from classify_utils import process_file
from flask_cors import CORS
from dotenv import load_dotenv
from docx import Document

load_dotenv()
app = Flask(__name__)

# Enable CORS
CORS(app)

# UPLOAD_FOLDER = './uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

    # filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    # file.save(filepath)

    try:
        endpoint_arn = os.getenv("ENDPOINT_ARN")

        if file.filename.endswith(".docx"):
            doc = Document(file)
            file_content = "\n".join([p.text for p in doc.paragraphs])
        else:
            # Detect encoding
            raw_data = file.read()
            encoding_result = chardet.detect(raw_data)
            file_encoding = encoding_result.get("encoding", "utf-8")  # Default to utf-8 if detection fails
            file.seek(0)  # Reset file pointer
            file_content = file.read().decode(file_encoding, errors="ignore")

        results = process_file(endpoint_arn, file_content)
        process_file_and_store(results)
    
    except Exception as e:
        print("Error reading file:", str(e))
        return jsonify({"error": "Failed to read file: " + str(e)}), 400

    return jsonify({"results": results})

    
if __name__ == '__main__':
    print("Processing existing files before starting the server...")
    
    app.run(debug=True)
    
