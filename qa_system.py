from langchain_community.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import LlamaCpp
from langchain.chains import RetrievalQA
import pandas as pd

class QASystem:
    def __init__(self):
        # Pre-filter data
        df = pd.read_csv("books.csv")
        self.filtered_df = df[df["price"] < 20.0]
        self.filtered_df.to_csv("filtered_books.csv", index=False)
        
        # Initialize QA system
        self.qa = self._initialize_qa()
    
    def _initialize_qa(self):
        loader = CSVLoader(file_path="filtered_books.csv")
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)
        
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        db = FAISS.from_documents(texts, embeddings)
        
        llm = LlamaCpp(
            model_path="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
            temperature=0.0,
            max_tokens=200,
            n_ctx=2048
        )
        
        return RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=db.as_retriever()
        )
    
    def ask(self, question: str) -> str:
        result = self.qa.invoke({"query": question})
        return (
            result["result"]
            .replace("$", "£")  # Fix currency symbol
            .replace("\n", "<br>")  # Preserve line breaks
            .replace("\"", "")  # Remove quotes
        )

# Initialize once at startup
qa_engine = QASystem()