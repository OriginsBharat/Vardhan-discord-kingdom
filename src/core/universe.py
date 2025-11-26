"""
Universe Client - Updated for Pinecone v3+ API
Long-term memory storage for all bots
"""
from pinecone import Pinecone, ServerlessSpec
from src.config import config

class UniverseClient:
    def __init__(self):
        if not config.pinecone_api_key:
            print("Warning: Pinecone API key not set. Memory system disabled.")
            self.enabled = False
            return

        self.enabled = True
        self.pc = Pinecone(api_key=config.pinecone_api_key)
        self.index_name = "my-ai-world"
        self._ensure_index_exists()
        self.index = self.pc.Index(self.index_name)
        print("UniverseClient initialized with Pinecone v3 API.")

    def _ensure_index_exists(self):
        existing_indexes = [idx.name for idx in self.pc.list_indexes()]

        if self.index_name not in existing_indexes:
            # Create serverless index (free tier compatible)
            self.pc.create_index(
                name=self.index_name,
                dimension=4096,  # Match your embedding model
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"  # Free tier region
                )
            )
            print(f"Created new Pinecone index: {self.index_name}")

    def store_memory(self, bot_name: str, memory_id: str, memory_vector: list, metadata: dict):
        """
        Stores a memory vector for a specific bot.

        Args:
            bot_name: Name of the bot this memory belongs to
            memory_id: Unique identifier for this memory
            memory_vector: The embedding vector (list of floats)
            metadata: Additional data (text, timestamp, etc.)
        """
        if not self.enabled:
            return

        # Add bot_name to metadata for filtering
        metadata["bot_name"] = bot_name

        self.index.upsert(
            vectors=[{
                "id": f"{bot_name}-{memory_id}",
                "values": memory_vector,
                "metadata": metadata
            }]
        )
        print(f"Stored memory for {bot_name}: {memory_id[:20]}...")

    def recall_memories(self, bot_name: str, query_vector: list, top_k: int = 5):
        """
        Recalls the most relevant memories for a bot based on a query vector.

        Args:
            bot_name: Filter memories to this bot only
            query_vector: The query embedding to match against
            top_k: Number of results to return

        Returns:
            List of matching memories with scores
        """
        if not self.enabled:
            return []

        results = self.index.query(
            vector=query_vector,
            top_k=top_k,
            filter={"bot_name": {"$eq": bot_name}},
            include_metadata=True
        )
        return results.matches

    def delete_memory(self, bot_name: str, memory_id: str):
        """Deletes a specific memory."""
        if not self.enabled:
            return

        self.index.delete(ids=[f"{bot_name}-{memory_id}"])

    def clear_bot_memories(self, bot_name: str):
        """Clears all memories for a specific bot."""
        if not self.enabled:
            return

        # Delete by metadata filter
        self.index.delete(filter={"bot_name": {"$eq": bot_name}})
        print(f"Cleared all memories for {bot_name}")


# Singleton instance - will initialize on import
try:
    universe_client = UniverseClient()
except Exception as e:
    print(f"Failed to initialize UniverseClient: {e}")
    universe_client = None
