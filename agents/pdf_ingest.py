from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

Data_Path = "data/policies"          # PDFs 
CHROMA_PATH = "db/chroma_policies"   # vector DB saved here

# 1) Load PDFs
def load_pdf_files(data):
    loader = DirectoryLoader(data, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents

documents = load_pdf_files(data=Data_Path)

# 2) Create chunks
def create_chunks(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks

text_chunks = create_chunks(extracted_data=documents)

# 3) Embeddings
def get_embedding_model():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

embedding_model = get_embedding_model()

# 4) Store in Chroma (persistent)
db = Chroma.from_documents(
    documents=text_chunks,
    embedding=embedding_model,
    persist_directory=CHROMA_PATH,
    collection_name="policies",
)
db.persist()

print(f"Stored {len(text_chunks)} chunks in Chroma at: {CHROMA_PATH}")