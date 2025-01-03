from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

loader = PyPDFLoader("data/pdf/Contato-Carl-Sagan.pdf")
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_documents = text_splitter.split_documents(documents)

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
embedding_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

vectorstore = FAISS.from_documents(split_documents, embedding_model)
retriever = vectorstore.as_retriever()

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=OPENAI_API_KEY
)

qa_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "You are a knowledgeable assistant. Use the following context to answer the question accurately:\n\n"
        "Context:\n{context}\n\n"
        "Question:\n{question}\n\n"
        "Answer:"
    ),
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type_kwargs={"prompt": qa_prompt},
    return_source_documents=True
)

query = "What is the major subject of the book?"
response = qa_chain.invoke({"query": query})  
result = response["result"]