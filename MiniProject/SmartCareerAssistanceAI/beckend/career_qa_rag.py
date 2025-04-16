# career_qa_rag.py

from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

import os
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"  # Ganti dengan milikmu

def build_vectorstore(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Split teks agar optimal untuk embedding
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(documents)

    # Embed pakai OpenAI
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("faiss_index")

def load_qa_bot():
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local("faiss_index", embeddings)

    retriever = vectorstore.as_retriever()
    llm = ChatOpenAI(temperature=0.2, model_name="gpt-4")

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff"
    )
    return qa_chain

def ask_question(question):
    qa_chain = load_qa_bot()
    return qa_chain.run(question)
