import os,boto3
from docx import Document
import time

# Function to classify text chunks using the AWS Comprehend custom classifier
def classify_text_chunks(endpoint_arn, text_chunks):
    client = boto3.client(
        'comprehend',
        aws_access_key_id="AKIASIHRMN25GGCEPQ6S",
        aws_secret_access_key="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",
        region_name="ap-south-1",
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

# Function to read .txt files
def read_txt_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()

# Function to read .docx files
def read_docx_file(filepath):
    document = Document(filepath)
    return "\n".join([paragraph.text for paragraph in document.paragraphs])

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

def process_file(endpoint_arn, file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension == ".txt":
        text = read_txt_file(file_path)
    elif file_extension == ".docx":
        text = read_docx_file(file_path)
    else:
        raise ValueError("Unsupported file format. Only .txt and .docx are supported.")

    text_chunks = split_text_into_chunks(text)
    print(f"Processing {len(text_chunks)} text chunks...\n")
    results = classify_text_chunks(endpoint_arn, text_chunks)
    return results

# if __name__ == "__main__":
#     endpoint_arn = "arn:aws:comprehend:ap-south-1:155125051066:document-classifier-endpoint/sairam"  # Replace with your actual endpoint ARN
#     file_path = "(INL-1) INTEL-MSL-BELGAUM-Divya.docx"  # Replace with your .txt or .docx file path

#     results = process_file(endpoint_arn, file_path)
#     print("Classification completed.\n")
#     print("Detailed Results:")
#     for result in results:
#         print("Chunk Text:")
#         print(result["Text"])
#         print("Predictions:")
#         for pred in result["Predictions"]:
#             print(f"  - {pred['Label']} ({pred['Confidence']:.2f})")
#         print("-" * 80)
