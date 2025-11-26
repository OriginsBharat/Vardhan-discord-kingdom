import pinecone
from src.config import config

class UniverseClient:
    def __init__(self):
        if not config.pinecone_api_key or not config.pinecone_environment:
            raise ValueError("Pinecone API key and environment must be set.")

        pinecone.init(
            api_key=config.pinecone_api_key,
            environment=config.pinecone_environment
        )
        self.index_name = "my-ai-world"
        self._ensure_index_exists()

    def _ensure_index_exists(self):
        if self.index_name not in pinecone.list_indexes():
            # Dimension should match the embedding model's output, e.g., Mistral's is 4096
            # This should be configured based on the Ollama model used.
            pinecone.create_index(self.index_name, dimension=4096, metric="cosine")
        self.index = pinecone.Index(self.index_name)

    def store_memory(self, bot_name, memory_vector, metadata):
        """
        Stores a memory vector for a specific bot.
        'metadata' should include the text of the memory and a timestamp.
        """
        # We'll namespace vectors by bot name to keep memories separate
        vector_id = f"{bot_name}-{metadata['timestamp']}"
        self.index.upsert(vectors=[(vector_id, memory_vector, metadata)])
        print(f"Stored memory for {bot_name}.")

    def recall_memories(self, bot_name, query_vector, top_k=5):
        """
        Recalls the most relevant memories for a bot based on a query vector.
        """
        results = self.index.query(
            vector=query_vector,
            top_k=top_k,
            filter={"bot_name": bot_name} # Assuming bot_name is in metadata
        )
        return results.matches

# A single instance for the application
universe_client = UniverseClient()
