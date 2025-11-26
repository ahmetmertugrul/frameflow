"""
Pytest Configuration and Fixtures
"""

import pytest
import os
import sys
from unittest.mock import Mock, AsyncMock
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.schemas import (
    StoryInput,
    CharacterProfile,
    Scene,
    SceneLocation,
    DialogueLine,
    ScreenplayMetadata,
    ScreenplayOutput,
    StoryboardFrame,
    StoryboardOutput
)


@pytest.fixture
def sample_story_input():
    """Sample story input for testing"""
    return StoryInput(
        prompt="A detective discovers the killer is his future self",
        genre="Thriller",
        dialogue_style="Realistic",
        act_structure="Three-Act"
    )


@pytest.fixture
def sample_character():
    """Sample character profile"""
    return CharacterProfile(
        name="Alex Morgan",
        age=35,
        role="protagonist",
        description="A hardened detective with a troubled past",
        personality_traits=["determined", "cynical", "intelligent", "haunted"],
        visual_description="Tall, athletic build, short dark hair, piercing blue eyes, leather jacket",
        motivation="To solve the case and find redemption",
        arc="From cynical loner to team player"
    )


@pytest.fixture
def sample_characters():
    """Multiple sample characters"""
    return [
        CharacterProfile(
            name="Alex Morgan",
            age=35,
            role="protagonist",
            description="A hardened detective",
            personality_traits=["determined", "intelligent"],
            visual_description="Tall, dark hair, blue eyes",
            motivation="Solve the case",
            arc="From loner to team player"
        ),
        CharacterProfile(
            name="Dr. Sarah Chen",
            age=38,
            role="supporting",
            description="Brilliant forensic psychologist",
            personality_traits=["analytical", "empathetic"],
            visual_description="Medium height, long black hair, professional attire",
            motivation="Understand the criminal mind",
            arc="Learns to trust instincts"
        )
    ]


@pytest.fixture
def sample_scene():
    """Sample screenplay scene"""
    return Scene(
        scene_number=1,
        location=SceneLocation(
            setting="INT",
            location="DETECTIVE'S OFFICE",
            time="DAY"
        ),
        action="The office is cluttered with case files. ALEX sits at the desk, studying crime scene photos.",
        dialogue=[
            DialogueLine(
                character="ALEX",
                line="Three victims. Same signature.",
                parenthetical="to himself"
            ),
            DialogueLine(
                character="SARAH",
                line="You're seeing a pattern the others missed."
            )
        ]
    )


@pytest.fixture
def sample_screenplay_metadata():
    """Sample screenplay metadata"""
    return ScreenplayMetadata(
        title="The Time Killer",
        author="FrameFlow Agent",
        genre="Thriller",
        logline="A detective discovers the serial killer he's hunting is his future self"
    )


@pytest.fixture
def sample_screenplay(sample_screenplay_metadata, sample_characters, sample_scene):
    """Complete sample screenplay"""
    return ScreenplayOutput(
        metadata=sample_screenplay_metadata,
        characters=sample_characters,
        scenes=[sample_scene],
        page_count=2
    )


@pytest.fixture
def sample_storyboard_frame():
    """Sample storyboard frame"""
    return StoryboardFrame(
        frame_number=1,
        scene_reference=1,
        description="Detective studying case files in dimly lit office",
        camera_angle="Medium Shot",
        visual_prompt="Cinematic shot of detective at desk, film noir style, dramatic lighting",
        image_path="/tmp/frame_001.png"
    )


@pytest.fixture
def sample_storyboard(sample_storyboard_frame):
    """Sample storyboard output"""
    return StoryboardOutput(
        screenplay_title="The Time Killer",
        frames=[sample_storyboard_frame],
        visual_style="Noir"
    )


@pytest.fixture
def mock_llm_client():
    """Mock LLM client"""
    mock = AsyncMock()
    mock.generate = AsyncMock(return_value="Generated text response")
    mock.generate_structured = AsyncMock(return_value={
        "main_theme": "Time paradox",
        "conflict": "Man vs Self",
        "protagonist": "Detective Alex",
        "setting": "Noir city"
    })
    return mock


@pytest.fixture
def mock_image_client():
    """Mock image generation client"""
    mock = AsyncMock()
    mock.generate_storyboard_frame = AsyncMock(return_value=b"fake_image_data")
    mock.save_image = AsyncMock(return_value="/tmp/frame.png")
    return mock


@pytest.fixture
def mock_embedding_client():
    """Mock embedding client"""
    mock = AsyncMock()
    mock.create_embedding = AsyncMock(return_value=[0.1] * 1536)
    mock.cosine_similarity = Mock(return_value=0.95)
    return mock


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Mock environment variables"""
    monkeypatch.setenv("SAMBANOVA_API_KEY", "test_sambanova_key")
    monkeypatch.setenv("HYPERBOLIC_API_KEY", "test_hyperbolic_key")
    monkeypatch.setenv("NEBIUS_API_KEY", "test_nebius_key")
    monkeypatch.setenv("BLAXEL_API_KEY", "test_blaxel_key")


@pytest.fixture
def temp_output_dir(tmp_path):
    """Temporary output directory for tests"""
    output_dir = tmp_path / "outputs"
    output_dir.mkdir()
    return output_dir


@pytest.fixture
async def mock_frameflow_agent(mock_llm_client, mock_image_client, mock_embedding_client):
    """Mock FrameFlow agent with all clients"""
    from core.agent import FrameFlowAgent

    agent = FrameFlowAgent()
    agent.llm_client = mock_llm_client
    agent.image_client = mock_image_client
    agent.embedding_client = mock_embedding_client

    return agent


# Pytest configuration
def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "asyncio: mark test as async"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


# Async test support
@pytest.fixture
def event_loop():
    """Create event loop for async tests"""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
