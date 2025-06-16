# ingest.py
import os
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
loader = PyMuPDFLoader("TTB.pdf")
documents = loader.load()
print(f"Loaded {len(documents)} pages from the PDF.")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
docs = text_splitter.split_documents(documents)
print(f"Split the document into {len(docs)} chunks.")

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

print("Creating vector store... This may take a moment.")
vectorstore = FAISS.from_documents(docs, embeddings)
vectorstore.save_local("faiss_index")
print("Vector store created and saved successfully!")
