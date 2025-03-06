import os
import glob
from typing import List
from langchain_community.document_loaders import PyPDFLoader, UnstructuredEPubLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from settings import settings
from langchain.chains import RetrievalQA
from langchain.llms import Ollama
from langchain.schema import Document

class RAGManager:
    def __init__(self):
        self.vector_store = None
        self.documents = []
        self.ollama_embeddings = OllamaEmbeddings(
            base_url=settings.OLLAMA_HOST,
            model=settings.OLLAMA_MODEL
        )
        
        self.initialize_knowledge_base()

    def initialize_knowledge_base(self):
        """Initialize the knowledge base with documents from the data directory"""
        try:
            # PDF files
            pdf_files = glob.glob(os.path.join(settings.DATA_DIR, "**/*.pdf"), recursive=True)
            for pdf_file in pdf_files:
                try:
                    loader = PyPDFLoader(pdf_file)
                    self.documents.extend(loader.load())
                    print(f"------------------------------ Loaded PDF: {pdf_file}")
                except Exception as e:
                    print(f"Error loading PDF {pdf_file}: {e}")
            
            # EPUB files
            epub_files = glob.glob(os.path.join(settings.DATA_DIR, "**/*.epub"), recursive=True)
            for epub_file in epub_files:
                try:
                    loader = UnstructuredEPubLoader(epub_file)
                    self.documents.extend(loader.load())
                    print(f"------------------------------ Loaded EPUB: {epub_file}")
                except Exception as e:
                    print(f"------------------------------ Error loading EPUB {epub_file}: {e}")
            
            # Split the documents into chunks
            if self.documents:
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=settings.RAG_CHUNK_SIZE,
                    chunk_overlap=settings.RAG_CHUNK_OVERLAP
                )
                chunks = text_splitter.split_documents(self.documents)
                
                # Create vector store
                self.vector_store = FAISS.from_documents(chunks, self.ollama_embeddings)
                print(f"------------------------------ Created vector store with {len(chunks)} chunks from {len(self.documents)} documents")
            else:
                print("No documents found in the data directory")
        except Exception as e:
            print(f"Error initializing knowledge base: {e}")

    def query_knowledge_base(self, query):
        """Query the knowledge base"""
        if not self.vector_store:
            return "Knowledge base is not initialized or empty."
        
        try:
            # Create retriever
            retriever = self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": settings.RAG_TOP_K_RESULTS}
            )
            
            # Create QA chain
            qa = RetrievalQA.from_chain_type(
                llm=Ollama(base_url=settings.OLLAMA_HOST, model=settings.OLLAMA_MODEL),
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=False
            )
            
            # Run the query
            result = qa.run(query)
            return result
        except Exception as e:
            print(f"Error querying knowledge base: {e}")
            return f"Error querying knowledge base: {str(e)}"
    
    def get_all_documents(self) -> List[Document]:
        """
        Retrieve all documents from the knowledge base
        
        Returns:
            List of Document objects containing all parsed documents
        """
        if not self.documents:
            return []
        
        return self.documents

# Create a singleton instance
rag_manager = RAGManager() 