from langchain_community.document_loaders import PyMuPDFLoader
from dotenv import load_dotenv
load_dotenv()

def load_cv(file_path):
    loader = PyMuPDFLoader(file_path)
    return loader.load()
