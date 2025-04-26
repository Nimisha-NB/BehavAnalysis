# Student Story Classification System
This project is designed to classify student stories into behavioral shifts and indicators using a custom-trained AWS Comprehend model.
It provides a simple upload interface, processes text files dynamically, and visualizes classification results to support impact team reporting.

#  How to Run Locally
1. Clone the repository:
```bash
git clone https://github.com/your-username/your-repo-name.git
```

2. Navigate into backend folder:
```bash
cd backend
```
3. Create a .env file inside /backend directory:
```bash
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
AWS_REGION=ap-south-1
COMPREHEND_ENDPOINT_ARN=your-comprehend-endpoint-arn
```
4. Install dependencies:
```bash
pip install -r requirements.txt
```
5. Start the server:

```bash
python app.py
```
6. Run the frontend

```bash
cd frontend
npm run dev
```

# Features
Upload .docx and .txt files dynamically (no need to manually store)

Predict labels using a custom AWS Comprehend endpoint

Automatically save classification predictions into an Excel file
