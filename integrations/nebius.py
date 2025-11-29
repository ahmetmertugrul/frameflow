"""
Nebius AI Integration
Embeddings and vector storage for character consistency
"""

import os
import httpx
from typing import Optional, Dict, Any, List, Tuple
import numpy as np
import asyncio
import json


class NebiusClient:
    """Client for Nebius AI embeddings and LLM API"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Nebius client

        Args:
            api_key: Nebius API key (or use NEBIUS_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("NEBIUS_API_KEY")
        if not self.api_key:
            raise ValueError("Nebius API key not provided")

        self.base_url = "https://api.studio.nebius.ai/v1"
        self.embedding_model = "text-embedding-ada-002"
        self.timeout = 60.0

    async def create_embedding(
        self,
        text: str,
        model: Optional[str] = None,
        **kwargs
    ) -> List[float]:
        """
        Create embedding vector for text

        Args:
            text: Input text
            model: Embedding model to use
            **kwargs: Additional parameters

        Returns:
            Embedding vector
        """
        model = model or self.embedding_model

        payload = {
            "model": model,
            "input": text,
            **kwargs
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/embeddings",
                json=payload,
                headers=headers
            )

            response.raise_for_status()
            result = response.json()

            return result["data"][0]["embedding"]

    async def batch_create_embeddings(
        self,
        texts: List[str],
        model: Optional[str] = None,
        **kwargs
    ) -> List[List[float]]:
        """
        Create embeddings for multiple texts

        Args:
            texts: List of texts
            model: Embedding model
            **kwargs: Additional parameters

        Returns:
            List of embedding vectors
        """
        tasks = [
            self.create_embedding(text, model, **kwargs)
            for text in texts
        ]

        return await asyncio.gather(*tasks)

    def cosine_similarity(
        self,
        embedding1: List[float],
        embedding2: List[float]
    ) -> float:
        """
        Calculate cosine similarity between two embeddings

        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector

        Returns:
            Similarity score (0-1)
        """
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)

        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(dot_product / (norm1 * norm2))

    async def find_most_similar(
        self,
        query_text: str,
        candidate_texts: List[str],
        top_k: int = 5
    ) -> List[Tuple[int, str, float]]:
        """
        Find most similar texts to query

        Args:
            query_text: Query text
            candidate_texts: List of candidate texts
            top_k: Number of top results to return

        Returns:
            List of (index, text, similarity_score) tuples
        """
        # Create embeddings
        query_embedding = await self.create_embedding(query_text)
        candidate_embeddings = await self.batch_create_embeddings(candidate_texts)

        # Calculate similarities
        similarities = [
            (i, text, self.cosine_similarity(query_embedding, emb))
            for i, (text, emb) in enumerate(zip(candidate_texts, candidate_embeddings))
        ]

        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[2], reverse=True)

        return similarities[:top_k]


class CharacterConsistencyManager:
    """
    Manages character visual consistency using embeddings
    """

    def __init__(self, nebius_client: NebiusClient):
        """
        Initialize character consistency manager

        Args:
            nebius_client: Nebius client instance
        """
        self.client = nebius_client
        self.character_embeddings: Dict[str, Dict[str, Any]] = {}
        self.storage_path = "outputs/character_embeddings.json"

    async def store_character(
        self,
        character_name: str,
        visual_description: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Store character visual embedding

        Args:
            character_name: Character's name
            visual_description: Detailed visual description
            metadata: Additional character metadata

        Returns:
            Character embedding ID
        """
        # Create embedding
        embedding = await self.client.create_embedding(visual_description)

        # Store character data
        character_id = f"{character_name.lower().replace(' ', '_')}"

        self.character_embeddings[character_id] = {
            "name": character_name,
            "visual_description": visual_description,
            "embedding": embedding,
            "metadata": metadata or {},
            "frame_count": 0,
            "last_updated": None
        }

        # Save to disk
        await self._save_embeddings()

        return character_id

    async def get_character_description(
        self,
        character_name: str,
        context: Optional[str] = None
    ) -> str:
        """
        Get consistent character description

        Args:
            character_name: Character's name
            context: Optional context (scene description, etc.)

        Returns:
            Visual description for image generation
        """
        character_id = character_name.lower().replace(' ', '_')

        if character_id not in self.character_embeddings:
            raise ValueError(f"Character {character_name} not found")

        char_data = self.character_embeddings[character_id]
        base_description = char_data["visual_description"]

        # If context provided, can adapt description slightly while maintaining consistency
        if context:
            # TODO: Use LLM to adapt description based on context
            # For now, just return base description
            pass

        # Update usage count
        char_data["frame_count"] += 1

        return base_description

    async def validate_consistency(
        self,
        character_name: str,
        new_description: str,
        threshold: float = 0.85
    ) -> Tuple[bool, float]:
        """
        Validate if new description is consistent with stored character

        Args:
            character_name: Character's name
            new_description: New description to validate
            threshold: Minimum similarity threshold (0-1)

        Returns:
            (is_consistent, similarity_score)
        """
        character_id = character_name.lower().replace(' ', '_')

        if character_id not in self.character_embeddings:
            return False, 0.0

        # Get stored embedding
        stored_embedding = self.character_embeddings[character_id]["embedding"]

        # Create embedding for new description
        new_embedding = await self.client.create_embedding(new_description)

        # Calculate similarity
        similarity = self.client.cosine_similarity(stored_embedding, new_embedding)

        is_consistent = similarity >= threshold

        return is_consistent, similarity

    async def get_all_characters(self) -> List[str]:
        """
        Get list of all stored characters

        Returns:
            List of character names
        """
        return [
            data["name"]
            for data in self.character_embeddings.values()
        ]

    async def _save_embeddings(self):
        """Save embeddings to disk"""
        # Create output directory if needed
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)

        # Convert to serializable format (embeddings as lists)
        save_data = {
            char_id: {
                **data,
                "embedding": data["embedding"]  # Already a list
            }
            for char_id, data in self.character_embeddings.items()
        }

        with open(self.storage_path, 'w') as f:
            json.dump(save_data, f, indent=2)

    async def load_embeddings(self):
        """Load embeddings from disk"""
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                self.character_embeddings = json.load(f)


# Convenience function
async def create_character_embedding(
    character_name: str,
    visual_description: str,
    api_key: Optional[str] = None
) -> str:
    """
    Quick character embedding creation

    Args:
        character_name: Character's name
        visual_description: Visual description
        api_key: API key

    Returns:
        Character ID
    """
    client = NebiusClient(api_key=api_key)
    manager = CharacterConsistencyManager(client)

    return await manager.store_character(character_name, visual_description)
