import streamlit as st
import os
import tempfile
from pathlib import Path
import shutil

# Import custom modules
from utils.pdf_processor import PDFProcessor
from utils.embeddings import EmbeddingGenerator
from utils.vector_store import VectorStore
from utils.llm_handler import LLMHandler

# Page configuration
st.set_page_config(
    page_title="PDF Q&A System",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None
if 'pdf_processed' not in st.session_state:
    st.session_state.pdf_processed = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def initialize_models():
    """Initialize models with loading indicators"""
    with st.spinner("Loading embedding model..."):
        embedding_gen = EmbeddingGenerator()
    with st.spinner("Loading language model..."):
        llm_handler = LLMHandler()
    return embedding_gen, llm_handler

def main():
    st.title("📚 PDF Question-Answering System")
    st.markdown("Upload a PDF and ask questions about its content using AI!")
    
    # Sidebar for PDF upload
    with st.sidebar:
        st.header("📄 Document Upload")
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type="pdf",
            help="Upload a PDF document to analyze"
        )
        
        if uploaded_file is not None:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            # Process PDF button
            if st.button("Process PDF", type="primary"):
                with st.spinner("Processing PDF..."):
                    # Initialize components
                    embedding_gen, llm_handler = initialize_models()
                    
                    # Extract text from PDF
                    pdf_processor = PDFProcessor()
                    chunks = pdf_processor.extract_and_chunk_text(tmp_path)
                    
                    if chunks:
                        # Create vector store
                        vector_store = VectorStore(embedding_gen)
                        vector_store.add_documents(chunks)
                        
                        # Store in session state
                        st.session_state.vector_store = vector_store
                        st.session_state.llm_handler = llm_handler
                        st.session_state.pdf_processed = True
                        st.session_state.pdf_name = uploaded_file.name
                        
                        st.success(f"✅ Processed {len(chunks)} text chunks from {uploaded_file.name}")
                    else:
                        st.error("Failed to extract text from PDF")
                
                # Clean up temp file
                os.unlink(tmp_path)
        
        # Display current document info
        if st.session_state.pdf_processed:
            st.divider()
            st.info(f"📖 Current document: {st.session_state.pdf_name}")
            if st.button("Clear Document"):
                st.session_state.vector_store = None
                st.session_state.pdf_processed = False
                st.session_state.chat_history = []
                st.rerun()
    
    # Main content area
    if st.session_state.pdf_processed:
        # Chat interface
        st.header("💬 Ask Questions")
        
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Question input
        if question := st.chat_input("Ask a question about the PDF..."):
            # Add user message to chat
            st.session_state.chat_history.append({"role": "user", "content": question})
            
            with st.chat_message("user"):
                st.markdown(question)
            
            # Generate answer
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # Retrieve relevant documents
                    relevant_docs = st.session_state.vector_store.similarity_search(question, k=3)
                    
                    # Generate answer using LLM
                    answer = st.session_state.llm_handler.generate_answer(
                        question, 
                        relevant_docs
                    )
                    
                    st.markdown(answer)
                    
                    # Add to chat history
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": answer}
                    )
                    
                    # (Source excerpts display removed)
    else:
        # Welcome message
        st.info("👆 Please upload a PDF document in the sidebar to get started!")
        
        # Feature showcase
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🚀 Features")
            st.markdown("""
            - PDF text extraction
            - Intelligent chunking
            - Vector embeddings
            - Semantic search
            """)
        
        with col2:
            st.markdown("### 🛠️ Technology")
            st.markdown("""
            - Open-source LLMs
            - FAISS vector DB
            - Sentence Transformers
            - LangChain framework
            """)
        
        with col3:
            st.markdown("### 💡 Use Cases")
            st.markdown("""
            - Research papers
            - Technical manuals
            - Legal documents
            - Educational content
            """)

if __name__ == "__main__":
    main()
