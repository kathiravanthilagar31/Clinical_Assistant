import os
import chromadb
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.openai import OpenAI
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.chat_engine import CondenseQuestionChatEngine
import dotenv

dotenv.load_dotenv()
# It's crucial to use an environment variable for your API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def load_data(filepath='data'):
    docs = SimpleDirectoryReader(filepath).load_data()
    parser = SentenceSplitter(chunk_size=500, chunk_overlap=20)
    chunks = parser.get_nodes_from_documents(docs)
    return chunks


def init_rag_engine():
    # ... (rest of your imports and setup)

    # Check if the database is already populated
    db = chromadb.PersistentClient(path="./db")
    chroma_collection = db.get_or_create_collection("clinical_data")

    # Only build the index if the collection is empty
    if chroma_collection.count() == 0:
        print("Indexing documents for the first time...")
        chunks = load_data('data')
        vectorstore = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vectorstore)
        index = VectorStoreIndex.from_documents(documents=chunks, storage_context=storage_context)
    else:
        print("Loading existing index...")
        vectorstore = ChromaVectorStore(chroma_collection=chroma_collection)
        index = VectorStoreIndex.from_vector_store(vectorstore)
        memory = ChatMemoryBuffer.from_defaults(token_limit=3900)
        chat_engine = CondenseQuestionChatEngine.from_defaults(
            query_engine=index.as_query_engine(), 
            memory=memory
        )
        return chat_engine