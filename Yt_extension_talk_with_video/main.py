from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# LangChain setup
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)
prompt = PromptTemplate(
    template="""You are a helpful assistant. Answer only from the provided transcript context.
    If the context is insufficient, just say you don't know.

    {context}
    Question: {question}
    """,
    input_variables=["context", "question"]
)

class Query(BaseModel):
    video_id: str
    question: str

@app.post("/ask")
def ask_question(query: Query):
    try:
        transcriptlist = YouTubeTranscriptApi.get_transcript(query.video_id, languages=["en","hi"])
        transcript = " ".join(chunk["text"] for chunk in transcriptlist)
    except TranscriptsDisabled:
        raise HTTPException(status_code=404, detail="No captions available.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([transcript])
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_documents(chunks, embeddings)
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

    def format_docs(retrieved_docs):
        return "\n\n".join(doc.page_content for doc in retrieved_docs)

    parallel_chain = RunnableParallel({
        'context': retriever | RunnableLambda(format_docs),
        'question': RunnablePassthrough()
    })

    main_chain = parallel_chain | prompt | llm | StrOutputParser()

    try:
        result = main_chain.invoke(query.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"answer": result}
