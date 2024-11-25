import os
from uuid import uuid4
import pandas as pd

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Set up the embeddings
MODEL = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
embeddings = SentenceTransformer(MODEL)

# Load documents from the data folder
data_folder = "data2"
documents = []
text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=400)

for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)
    if filename.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
        pdf_docs = loader.load_and_split(text_splitter)
        for doc in pdf_docs:
            documents.append({
                "page_content": doc.page_content,
                "metadata": doc.metadata
            })
    elif filename.endswith(".csv"):
        df = pd.read_csv(file_path)
        for index, row in df.iterrows():
            # Concatenate question and answer into a single text entry
            text = f"Question: {row['Question']} Answer: {row['Answer']}"
            chunked_text = text_splitter.split_text(text)
            for chunk in chunked_text:
                documents.append({
                    "page_content": chunk,
                    "metadata": {
                        "source": file_path,
                        "page": index + 1  # Row number as the "page" indicator for CSV
                    }
                })

# Set up Qdrant client
client = QdrantClient("localhost", port=6333)

# Create collection in Qdrant database
if not client.collection_exists("info"):
    client.create_collection(
        collection_name="info",
        vectors_config={
            "content": VectorParams(size=384, distance=Distance.COSINE)
        }
    )

# Function to chunk documents and upload to Qdrant
def chunked_metadata(data, client=client, collection_name="info", batch_size=100):
    chunked_metadata = []

    for item in data:
        id = str(uuid4())
        content = item["page_content"]  # Accessing as dictionary keys
        source = item["metadata"]["source"]
        page = item["metadata"]["page"]

        # Generate embeddings
        content_vector = embeddings.encode([content])[0]
        vector_dict = {"content": content_vector}

        payload = {
            "page_content": content,
            "metadata": {
                "id": id,
                "source": source,
                "page": page,
            }
        }

        metadata = PointStruct(id=id, vector=vector_dict, payload=payload)
        chunked_metadata.append(metadata)

        # Upload in batches
        if len(chunked_metadata) >= batch_size:
            client.upsert(
                collection_name=collection_name,
                wait=True,
                points=chunked_metadata
            )
            chunked_metadata = []  # Reset after each batch

    # Upload any remaining points
    if chunked_metadata:
        client.upsert(
            collection_name=collection_name,
            wait=True,
            points=chunked_metadata
        )

# Upload all documents to Qdrant
chunked_metadata(documents)

# Print information about the collection
document_collection = client.get_collection("info")
print(f"Points in collection: {document_collection.points_count}")
