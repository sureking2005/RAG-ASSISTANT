from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import RetrievalQA
from dotenv import load_dotenv
import os

load_dotenv()

def create_rag_chain():

    loader = TextLoader("data/data.txt")
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vectorstore = Chroma.from_documents(
        splits,
        embedding=embeddings
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3
    )

    custom_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are Surendar's AI assistant.

You must answer ONLY using the provided context.

IMPORTANT RULES:
- Respond in plain text only.
- Do NOT use markdown.
- Do NOT use bullet points.
- Do NOT use *, **, or special formatting.
- Write clean continuous readable sentences.

If the answer is not found in the context, say:
"I don't know based on the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": custom_prompt}
    )

    return qa