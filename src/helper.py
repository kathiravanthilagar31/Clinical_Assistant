import os
import chromadb
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.openai import OpenAI
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.chat_engine import ContextChatEngine
import dotenv

dotenv.load_dotenv()
# It's crucial to use an environment variable for your API key
# Ensure this is set in your environment, not hardcoded.
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def load_data(filepath='data'):
    docs = SimpleDirectoryReader(filepath).load_data()
    parser = SentenceSplitter(chunk_size=500, chunk_overlap=20)
    chunks = parser.get_nodes_from_documents(docs)
    return chunks

def init_rag_engine():
    # Set up LLM and Embedding models globally within this function's scope
    # This ensures they are configured before index creation/loading
    llm_model = OpenAI(
        model="gpt-3.5-turbo",
        api_key=os.environ["OPENAI_API_KEY"],
        temperature=0,
        system_prompt="You are a helpful and professional clinical assistant. Your sole purpose is to provide accurate and concise answers to health and medical questions based on the retrieved data. Use ONLY the information provided in the given context. If the context does not contain the information needed to answer the question, politely state that you cannot answer based on the provided data but dont expliciltly say that your context does not have them."
    )
    Settings.llm = llm_model

    embed_model = OpenAIEmbedding(api_key=os.environ["OPENAI_API_KEY"])
    Settings.embed_model = embed_model

    # Check if the database is already populated
    db = chromadb.PersistentClient(path="./db")
    chroma_collection = db.get_or_create_collection("clinical_data")

    current_index = None # Initialize current_index to None

    # Only build the index if the collection is empty
    if chroma_collection.count() == 0:
        print("No data found in ChromaDB. Indexing documents for the first time...")
        chunks = load_data('data')
        vectorstore = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vectorstore)
        current_index = VectorStoreIndex.from_documents(documents=chunks, storage_context=storage_context)
        print("Indexing complete!")
    else:
        print("Loading existing index...")
        vectorstore = ChromaVectorStore(chroma_collection=chroma_collection)
        current_index = VectorStoreIndex.from_vector_store(vectorstore)
    
    # Initialize ChatMemoryBuffer and CondenseQuestionChatEngine outside the if/else
    # This ensures it's always created and returned.
    memory = ChatMemoryBuffer.from_defaults(token_limit=3900)
    chat_engine = ContextChatEngine.from_defaults(
        retriever=current_index.as_retriever(similarity_top_k=3),
        memory=memory
    )
    return chat_engine