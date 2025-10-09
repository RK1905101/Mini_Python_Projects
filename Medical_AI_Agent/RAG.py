from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import hub
from datasets import load_dataset
from langchain.document_loaders import DataFrameLoader



def get_medical_data():
    data = load_dataset("keivalya/MedQuad-MedicalQnADataset", split='train')
    data = data.to_pandas()
    df_loader = DataFrameLoader(data, page_content_column="Answer")
    documents = df_loader.load()
    return documents


def get_text_chunks(raw_text):

 
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200,separators='\n')

    chunks = splitter.split_documents(raw_text)

    return chunks

def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    vectorstore = FAISS.from_documents(documents=text_chunks, embedding=embeddings)

    vectorstore.save_local("Medical_database")

    return vectorstore


def get_conversation_chain(vectorstore):
   
    retriever = vectorstore.as_retriever()

    llm = ChatGroq(model="Gemma2-9b-It")

    prompt = hub.pull("rlm/rag-prompt")

    parallel_chain = RunnableParallel({
        "context": retriever,
        "question": RunnablePassthrough()
    })
    chain = parallel_chain | prompt | llm | StrOutputParser()

    return chain