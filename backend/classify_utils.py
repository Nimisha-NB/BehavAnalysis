import boto3,os
# from docx import Document
import time
from dotenv import load_dotenv

load_dotenv()

# Function to classify text chunks using the AWS Comprehend custom classifier
def classify_text_chunks(endpoint_arn, text_chunks):
    client = boto3.client(
        'comprehend',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )
    results = []

    for idx, chunk in enumerate(text_chunks):
        try:
            response = client.classify_document(
                Text=chunk,
                EndpointArn=endpoint_arn
            )
            results.append(response)
        except client.exceptions.TooManyRequestsException as e:
            print(f"Rate limit exceeded for chunk {idx + 1}. Retrying...")
            time.sleep(1)  # Wait before retrying
            continue
        classes = response.get('Classes', [])
        labels_with_confidence = [
            {"Label": label['Name'], "Confidence": label['Score']}
            for label in classes
        ]

        # Print details for debugging
        print(f"Chunk {idx + 1}: {chunk}")
        print("Predicted Labels with Confidence Scores:")
        for entry in labels_with_confidence:
            print(f"  - {entry['Label']} ({entry['Confidence']:.2f})")
        print()

        results.append({"Text": chunk, "Predictions": labels_with_confidence})
    
    return results


# Function to split text into manageable chunks
def split_text_into_chunks(text, max_chunk_size=500):
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        if sum(len(w) + 1 for w in current_chunk) + len(word) + 1 > max_chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
        current_chunk.append(word)

    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def process_file(endpoint_arn, text):
   

    text_chunks = split_text_into_chunks(text)
    print(f"Processing {len(text_chunks)} text chunks...\n")
    results = classify_text_chunks(endpoint_arn, text_chunks)
    return results
