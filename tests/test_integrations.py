"""
Tests for integrations/
Test API client integrations (SambaNova, Hyperbolic, Nebius)
Note: These are mostly unit tests with mocked responses.
Mark with @pytest.mark.integration for actual API calls (requires API keys)
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import httpx
import json

from integrations.sambanova import SambaNovaClient, quick_generate
from integrations.hyperbolic import HyperbolicClient, quick_generate_image
from integrations.nebius import NebiusClient, CharacterConsistencyManager


class TestSambaNovaClient:
    """Test SambaNova client"""

    def test_client_initialization(self, mock_env_vars):
        """Test client initialization with API key"""
        client = SambaNovaClient()
        assert client.api_key == "test_sambanova_key"
        assert client.base_url == "https://api.sambanova.ai/v1"

    def test_client_initialization_without_key(self):
        """Test that client raises error without API key"""
        with pytest.raises(ValueError) as exc_info:
            SambaNovaClient()

        assert "API key not provided" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_generate_text(self, mock_env_vars):
        """Test text generation"""
        client = SambaNovaClient()

        # Mock the HTTP client
        mock_response = {
            "choices": [
                {
                    "message": {
                        "content": "Generated text response"
                    }
                }
            ]
        }

        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                return_value=Mock(
                    json=Mock(return_value=mock_response),
                    raise_for_status=Mock()
                )
            )

            result = await client.generate(
                prompt="Test prompt",
                system_prompt="Test system",
                temperature=0.7
            )

            assert result == "Generated text response"

    @pytest.mark.asyncio
    async def test_generate_structured(self, mock_env_vars):
        """Test structured JSON generation"""
        client = SambaNovaClient()

        mock_json_response = '{"key": "value", "number": 42}'
        mock_response = {
            "choices": [
                {
                    "message": {
                        "content": mock_json_response
                    }
                }
            ]
        }

        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                return_value=Mock(
                    json=Mock(return_value=mock_response),
                    raise_for_status=Mock()
                )
            )

            result = await client.generate_structured(
                prompt="Generate JSON"
            )

            assert isinstance(result, dict)
            assert result["key"] == "value"
            assert result["number"] == 42

    @pytest.mark.asyncio
    async def test_batch_generate(self, mock_env_vars):
        """Test batch generation"""
        client = SambaNovaClient()

        prompts = ["Prompt 1", "Prompt 2", "Prompt 3"]

        with patch.object(client, 'generate', new=AsyncMock(side_effect=lambda p, **kw: f"Response to {p}")):
            results = await client.batch_generate(prompts)

            assert len(results) == 3
            assert results[0] == "Response to Prompt 1"
            assert results[2] == "Response to Prompt 3"

    def test_estimate_tokens(self, mock_env_vars):
        """Test token estimation"""
        client = SambaNovaClient()

        text = "This is a test sentence with multiple words."
        tokens = client.estimate_tokens(text)

        # Rough estimate: ~4 chars per token
        expected = len(text) // 4
        assert tokens == expected


class TestHyperbolicClient:
    """Test Hyperbolic client"""

    def test_client_initialization(self, mock_env_vars):
        """Test client initialization"""
        client = HyperbolicClient()
        assert client.api_key == "test_hyperbolic_key"
        assert client.base_url == "https://api.hyperbolic.xyz/v1"

    def test_client_initialization_without_key(self):
        """Test that client raises error without API key"""
        with pytest.raises(ValueError):
            HyperbolicClient()

    @pytest.mark.asyncio
    async def test_generate_image(self, mock_env_vars):
        """Test image generation"""
        client = HyperbolicClient()

        import base64
        fake_image = b"fake_image_data"
        fake_b64 = base64.b64encode(fake_image).decode()

        mock_response = {
            "images": [fake_b64]
        }

        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                return_value=Mock(
                    json=Mock(return_value=mock_response),
                    raise_for_status=Mock()
                )
            )

            result = await client.generate_image(
                prompt="A beautiful landscape",
                width=1024,
                height=768
            )

            assert result == fake_image

    @pytest.mark.asyncio
    async def test_generate_storyboard_frame(self, mock_env_vars):
        """Test storyboard frame generation"""
        client = HyperbolicClient()

        import base64
        fake_image = b"fake_storyboard_image"
        fake_b64 = base64.b64encode(fake_image).decode()

        mock_response = {
            "images": [fake_b64]
        }

        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                return_value=Mock(
                    json=Mock(return_value=mock_response),
                    raise_for_status=Mock()
                )
            )

            result = await client.generate_storyboard_frame(
                prompt="Detective at desk",
                style="noir",
                aspect_ratio="16:9"
            )

            assert result == fake_image

    @pytest.mark.asyncio
    async def test_save_image(self, mock_env_vars, tmp_path):
        """Test saving image to file"""
        client = HyperbolicClient()

        # Create a simple test image
        from PIL import Image
        import io

        img = Image.new('RGB', (100, 100), color='red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        image_data = img_bytes.getvalue()

        output_path = tmp_path / "test_image.png"

        saved_path = await client.save_image(
            image_bytes=image_data,
            output_path=str(output_path)
        )

        assert saved_path == str(output_path)
        assert output_path.exists()

    def test_get_available_models(self, mock_env_vars):
        """Test getting available models"""
        client = HyperbolicClient()
        models = client.get_available_models()

        assert isinstance(models, list)
        assert len(models) > 0
        assert "SDXL1.0-base" in models


class TestNebiusClient:
    """Test Nebius client"""

    def test_client_initialization(self, mock_env_vars):
        """Test client initialization"""
        client = NebiusClient()
        assert client.api_key == "test_nebius_key"
        assert client.base_url == "https://api.studio.nebius.ai/v1"

    def test_client_initialization_without_key(self):
        """Test that client raises error without API key"""
        with pytest.raises(ValueError):
            NebiusClient()

    @pytest.mark.asyncio
    async def test_create_embedding(self, mock_env_vars):
        """Test embedding creation"""
        client = NebiusClient()

        fake_embedding = [0.1] * 1536

        mock_response = {
            "data": [
                {
                    "embedding": fake_embedding
                }
            ]
        }

        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                return_value=Mock(
                    json=Mock(return_value=mock_response),
                    raise_for_status=Mock()
                )
            )

            result = await client.create_embedding("Test text")

            assert result == fake_embedding
            assert len(result) == 1536

    @pytest.mark.asyncio
    async def test_batch_create_embeddings(self, mock_env_vars):
        """Test batch embedding creation"""
        client = NebiusClient()

        texts = ["Text 1", "Text 2", "Text 3"]

        with patch.object(client, 'create_embedding', new=AsyncMock(return_value=[0.1] * 1536)):
            results = await client.batch_create_embeddings(texts)

            assert len(results) == 3
            assert all(len(emb) == 1536 for emb in results)

    def test_cosine_similarity(self, mock_env_vars):
        """Test cosine similarity calculation"""
        client = NebiusClient()

        # Identical vectors should have similarity of 1.0
        vec1 = [1, 2, 3, 4, 5]
        vec2 = [1, 2, 3, 4, 5]

        similarity = client.cosine_similarity(vec1, vec2)
        assert abs(similarity - 1.0) < 0.01

        # Orthogonal vectors should have similarity of 0.0
        vec3 = [1, 0]
        vec4 = [0, 1]

        similarity = client.cosine_similarity(vec3, vec4)
        assert abs(similarity - 0.0) < 0.01

    @pytest.mark.asyncio
    async def test_find_most_similar(self, mock_env_vars):
        """Test finding most similar texts"""
        client = NebiusClient()

        query = "detective story"
        candidates = ["crime fiction", "romance novel", "detective thriller"]

        # Mock embeddings that reflect similarity
        def mock_embedding(text):
            if "detective" in text or "crime" in text:
                return [1.0, 0.5, 0.0]
            else:
                return [0.0, 0.5, 1.0]

        with patch.object(client, 'create_embedding', new=AsyncMock(side_effect=mock_embedding)):
            with patch.object(client, 'batch_create_embeddings', new=AsyncMock(
                side_effect=lambda texts: [mock_embedding(t) for t in texts]
            )):
                results = await client.find_most_similar(query, candidates, top_k=2)

                assert len(results) == 2
                # First result should be most similar
                assert results[0][2] > results[1][2]


class TestCharacterConsistencyManager:
    """Test Character Consistency Manager"""

    @pytest.mark.asyncio
    async def test_store_character(self, mock_env_vars, tmp_path):
        """Test storing character"""
        client = NebiusClient()
        manager = CharacterConsistencyManager(client)
        manager.storage_path = str(tmp_path / "characters.json")

        with patch.object(client, 'create_embedding', new=AsyncMock(return_value=[0.1] * 1536)):
            char_id = await manager.store_character(
                character_name="Alex Morgan",
                visual_description="Tall, dark hair, blue eyes",
                metadata={"age": 35}
            )

            assert char_id == "alex_morgan"
            assert char_id in manager.character_embeddings

    @pytest.mark.asyncio
    async def test_get_character_description(self, mock_env_vars):
        """Test getting character description"""
        client = NebiusClient()
        manager = CharacterConsistencyManager(client)

        # Manually add character
        manager.character_embeddings["alex_morgan"] = {
            "name": "Alex Morgan",
            "visual_description": "Tall, dark hair",
            "embedding": [0.1] * 1536,
            "metadata": {},
            "frame_count": 0
        }

        description = await manager.get_character_description("Alex Morgan")

        assert description == "Tall, dark hair"
        # Frame count should increment
        assert manager.character_embeddings["alex_morgan"]["frame_count"] == 1

    @pytest.mark.asyncio
    async def test_validate_consistency(self, mock_env_vars):
        """Test validating character consistency"""
        client = NebiusClient()
        manager = CharacterConsistencyManager(client)

        # Add character
        manager.character_embeddings["alex_morgan"] = {
            "name": "Alex Morgan",
            "visual_description": "Tall, dark hair",
            "embedding": [1.0, 0.5, 0.0],
            "metadata": {},
            "frame_count": 0
        }

        # Similar description should pass
        with patch.object(client, 'create_embedding', new=AsyncMock(return_value=[0.95, 0.5, 0.05])):
            is_consistent, score = await manager.validate_consistency(
                "Alex Morgan",
                "Tall with dark hair"
            )

            assert score > 0.8

    @pytest.mark.asyncio
    async def test_get_all_characters(self, mock_env_vars):
        """Test getting all stored characters"""
        client = NebiusClient()
        manager = CharacterConsistencyManager(client)

        manager.character_embeddings = {
            "alex_morgan": {"name": "Alex Morgan"},
            "sarah_chen": {"name": "Sarah Chen"}
        }

        characters = await manager.get_all_characters()

        assert len(characters) == 2
        assert "Alex Morgan" in characters
        assert "Sarah Chen" in characters


class TestQuickHelpers:
    """Test quick helper functions"""

    @pytest.mark.asyncio
    async def test_quick_generate(self, mock_env_vars):
        """Test quick_generate helper"""
        mock_response = {
            "choices": [{"message": {"content": "Quick response"}}]
        }

        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                return_value=Mock(
                    json=Mock(return_value=mock_response),
                    raise_for_status=Mock()
                )
            )

            result = await quick_generate(
                prompt="Test",
                api_key="test_key"
            )

            assert result == "Quick response"

    @pytest.mark.asyncio
    async def test_quick_generate_image(self, mock_env_vars, tmp_path):
        """Test quick_generate_image helper"""
        import base64
        from PIL import Image
        import io

        # Create fake image
        img = Image.new('RGB', (100, 100), color='blue')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        fake_image = img_bytes.getvalue()
        fake_b64 = base64.b64encode(fake_image).decode()

        mock_response = {"images": [fake_b64]}

        output_path = tmp_path / "quick_image.png"

        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                return_value=Mock(
                    json=Mock(return_value=mock_response),
                    raise_for_status=Mock()
                )
            )

            result = await quick_generate_image(
                prompt="Test image",
                output_path=str(output_path),
                api_key="test_key"
            )

            assert result == str(output_path)


@pytest.mark.integration
class TestIntegrationWithRealAPIs:
    """
    Integration tests with real APIs
    These tests require actual API keys and are skipped by default
    Run with: pytest -m integration
    """

    @pytest.mark.asyncio
    async def test_real_sambanova_generation(self):
        """Test real SambaNova API call"""
        # Skip if no API key
        import os
        if not os.getenv("SAMBANOVA_API_KEY"):
            pytest.skip("SAMBANOVA_API_KEY not set")

        client = SambaNovaClient()
        result = await client.generate(
            prompt="Say hello",
            max_tokens=10
        )

        assert isinstance(result, str)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_real_hyperbolic_generation(self):
        """Test real Hyperbolic API call"""
        import os
        if not os.getenv("HYPERBOLIC_API_KEY"):
            pytest.skip("HYPERBOLIC_API_KEY not set")

        client = HyperbolicClient()
        result = await client.generate_image(
            prompt="A red circle",
            width=256,
            height=256,
            num_inference_steps=10
        )

        assert isinstance(result, bytes)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_real_nebius_embedding(self):
        """Test real Nebius API call"""
        import os
        if not os.getenv("NEBIUS_API_KEY"):
            pytest.skip("NEBIUS_API_KEY not set")

        client = NebiusClient()
        result = await client.create_embedding("Test text")

        assert isinstance(result, list)
        assert len(result) > 0
