import boto3

comprehend = boto3.client(
    'comprehend',
    aws_access_key_id="AKIASIHRMN25GGCEPQ6S",
    aws_secret_access_key="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",
    region_name="ap-south-1",
)
# response = comprehend.list_document_classifiers()

# for classifier in response['DocumentClassifierPropertiesList']:
#     print(f"Model ARN: {classifier['DocumentClassifierArn']}")
#     print(f"Status: {classifier['Status']}")

endpoint_arn = "arn:aws:comprehend:ap-south-1:155125051066:document-classifier-endpoint/endpoint2"
test_text= ["Before Agastya, I was afraid to ask questions, but now I keep asking until I understand. My curiosity has grown so much"
            ,"I always read about the importance of clean energy, but it was not until I built my own wind turbine that I understood the practical significance of what was in my textbook."
            ,"Aarav used to be quiet during discussions but then began to explore his interests in astronomy. He started researching constellations and even built a model of the solar system, demonstrating his active exploration of the subject."
            ]

for i in test_text:
    response = comprehend.classify_document(
        Text = i,
        EndpointArn = endpoint_arn
    )

    print("Classification Result", response['Classes'])