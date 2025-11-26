"""
Tests for core/agent.py
Validate FrameFlowAgent functionality
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
import os

from core.agent import FrameFlowAgent
from core.schemas import (
    StoryInput,
    ScreenplayOutput,
    StoryboardOutput,
    CharacterProfile
)


class TestFrameFlowAgentInit:
    """Test FrameFlowAgent initialization"""

    def test_agent_initialization(self):
        """Test basic agent initialization"""
        agent = FrameFlowAgent()

        assert agent.llm_client is None
        assert agent.image_client is None
        assert agent.embedding_client is None
        assert isinstance(agent.character_store, dict)
        assert len(agent.character_store) == 0

    def test_output_directory_created(self, tmp_path):
        """Test that output directory is created"""
        with patch('os.getcwd', return_value=str(tmp_path)):
            agent = FrameFlowAgent()
            output_dir = os.path.join(str(tmp_path), "outputs")
            assert os.path.exists(output_dir)


class TestStoryAnalysis:
    """Test story analysis functionality"""

    @pytest.mark.asyncio
    async def test_analyze_story(self, sample_story_input):
        """Test story analysis"""
        agent = FrameFlowAgent()

        analysis = await agent._analyze_story(sample_story_input)

        assert isinstance(analysis, dict)
        assert "main_theme" in analysis
        assert "conflict" in analysis
        assert "protagonist" in analysis
        assert "setting" in analysis
        assert "key_plot_points" in analysis

    @pytest.mark.asyncio
    async def test_analysis_includes_plot_points(self, sample_story_input):
        """Test that analysis includes plot points"""
        agent = FrameFlowAgent()

        analysis = await agent._analyze_story(sample_story_input)

        assert "key_plot_points" in analysis
        assert isinstance(analysis["key_plot_points"], list)
        assert len(analysis["key_plot_points"]) > 0


class TestCharacterCreation:
    """Test character creation functionality"""

    @pytest.mark.asyncio
    async def test_create_characters(self):
        """Test character creation"""
        agent = FrameFlowAgent()

        story_analysis = {
            "main_theme": "redemption",
            "protagonist": "detective"
        }

        characters = await agent._create_characters(story_analysis, "Thriller")

        assert isinstance(characters, list)
        assert len(characters) > 0
        assert all(isinstance(char, CharacterProfile) for char in characters)

    @pytest.mark.asyncio
    async def test_characters_stored_in_agent(self):
        """Test that characters are stored in agent's character store"""
        agent = FrameFlowAgent()

        story_analysis = {"protagonist": "detective"}
        characters = await agent._create_characters(story_analysis, "Drama")

        # Characters should be stored
        assert len(agent.character_store) > 0

        # Check that character names match
        for char in characters:
            assert char.name in agent.character_store
            assert agent.character_store[char.name] == char

    @pytest.mark.asyncio
    async def test_character_has_required_fields(self):
        """Test that created characters have all required fields"""
        agent = FrameFlowAgent()

        story_analysis = {"protagonist": "hero"}
        characters = await agent._create_characters(story_analysis, "Action")

        for char in characters:
            assert char.name is not None
            assert char.role is not None
            assert char.description is not None
            assert char.visual_description is not None
            assert isinstance(char.personality_traits, list)


class TestSceneWriting:
    """Test scene writing functionality"""

    @pytest.mark.asyncio
    async def test_write_scenes(self, sample_characters):
        """Test scene writing"""
        agent = FrameFlowAgent()

        story_analysis = {
            "key_plot_points": ["Opening", "Conflict", "Resolution"]
        }

        scenes = await agent._write_scenes(
            story_analysis=story_analysis,
            characters=sample_characters,
            act_structure="Three-Act",
            dialogue_style="Realistic",
            genre="Drama"
        )

        assert isinstance(scenes, list)
        assert len(scenes) > 0

    @pytest.mark.asyncio
    async def test_scenes_have_required_structure(self, sample_characters):
        """Test that scenes have proper structure"""
        agent = FrameFlowAgent()

        story_analysis = {"key_plot_points": ["Test"]}
        scenes = await agent._write_scenes(
            story_analysis=story_analysis,
            characters=sample_characters,
            act_structure="Three-Act",
            dialogue_style="Realistic",
            genre="Drama"
        )

        for scene in scenes:
            assert scene.scene_number is not None
            assert scene.location is not None
            assert scene.action is not None
            assert isinstance(scene.dialogue, list)


class TestScreenplayGeneration:
    """Test full screenplay generation"""

    @pytest.mark.asyncio
    async def test_generate_screenplay(self, sample_story_input):
        """Test full screenplay generation"""
        agent = FrameFlowAgent()

        screenplay = await agent.generate_screenplay(sample_story_input)

        assert isinstance(screenplay, ScreenplayOutput)
        assert screenplay.metadata is not None
        assert len(screenplay.characters) > 0
        assert len(screenplay.scenes) > 0

    @pytest.mark.asyncio
    async def test_screenplay_metadata_correct(self, sample_story_input):
        """Test that screenplay metadata is correctly set"""
        agent = FrameFlowAgent()

        screenplay = await agent.generate_screenplay(sample_story_input)

        assert screenplay.metadata.genre == sample_story_input.genre
        assert screenplay.metadata.title is not None
        assert screenplay.metadata.author == "FrameFlow Agent"

    @pytest.mark.asyncio
    async def test_page_count_estimation(self, sample_story_input):
        """Test page count estimation"""
        agent = FrameFlowAgent()

        screenplay = await agent.generate_screenplay(sample_story_input)

        assert screenplay.page_count > 0
        # Rough estimate: at least 1 page per scene
        assert screenplay.page_count >= len(screenplay.scenes)


class TestStoryboardGeneration:
    """Test storyboard generation"""

    @pytest.mark.asyncio
    async def test_identify_key_moments(self):
        """Test key moment identification"""
        agent = FrameFlowAgent()

        screenplay_text = "Test screenplay with multiple scenes."
        moments = await agent._identify_key_moments(screenplay_text, num_frames=5)

        assert isinstance(moments, list)
        assert len(moments) == 5

    @pytest.mark.asyncio
    async def test_generate_storyboard_frame(self):
        """Test individual frame generation"""
        agent = FrameFlowAgent()

        moment = {
            "scene_number": 1,
            "description": "Test moment",
            "emotional_tone": "dramatic",
            "characters": ["Alex"],
            "setting": "Office"
        }

        frame = await agent._generate_storyboard_frame(
            moment=moment,
            frame_number=1,
            visual_style="Realistic"
        )

        assert frame.frame_number == 1
        assert frame.scene_reference == 1
        assert frame.description is not None
        assert frame.camera_angle is not None

    @pytest.mark.asyncio
    async def test_generate_storyboard(self):
        """Test full storyboard generation"""
        agent = FrameFlowAgent()

        screenplay_text = "Test screenplay"
        storyboard = await agent.generate_storyboard(
            screenplay_text=screenplay_text,
            num_frames=4,
            visual_style="Noir"
        )

        assert isinstance(storyboard, StoryboardOutput)
        assert len(storyboard.frames) == 4
        assert storyboard.visual_style == "Noir"


class TestCharacterConsistency:
    """Test character consistency features"""

    def test_get_character_consistency_existing(self, sample_character):
        """Test retrieving character description"""
        agent = FrameFlowAgent()
        agent.character_store[sample_character.name] = sample_character

        description = agent.get_character_consistency(sample_character.name)

        assert description == sample_character.visual_description

    def test_get_character_consistency_not_found(self):
        """Test retrieving non-existent character"""
        agent = FrameFlowAgent()

        description = agent.get_character_consistency("Nonexistent Character")

        assert description is None

    @pytest.mark.asyncio
    async def test_character_store_populated_after_generation(self, sample_story_input):
        """Test that character store is populated after screenplay generation"""
        agent = FrameFlowAgent()

        screenplay = await agent.generate_screenplay(sample_story_input)

        # Character store should have entries
        assert len(agent.character_store) > 0

        # All screenplay characters should be in store
        for char in screenplay.characters:
            assert char.name in agent.character_store


class TestExportFunctionality:
    """Test export functionality"""

    @pytest.mark.asyncio
    async def test_export_screenplay_pdf(self, tmp_path):
        """Test screenplay PDF export"""
        agent = FrameFlowAgent()
        agent.output_dir = str(tmp_path)

        screenplay_text = "Test screenplay text"
        pdf_path = await agent.export_screenplay_pdf(screenplay_text)

        assert pdf_path is not None
        assert pdf_path.startswith(str(tmp_path))
        assert pdf_path.endswith(".pdf")

    @pytest.mark.asyncio
    async def test_export_storyboard_pack(self, tmp_path):
        """Test storyboard ZIP export"""
        agent = FrameFlowAgent()
        agent.output_dir = str(tmp_path)

        frame_images = [("path1.png", "desc1"), ("path2.png", "desc2")]
        zip_path = await agent.export_storyboard_pack(frame_images)

        assert zip_path is not None
        assert zip_path.startswith(str(tmp_path))
        assert zip_path.endswith(".zip")


class TestUtilityMethods:
    """Test utility methods"""

    def test_estimate_page_count_empty(self):
        """Test page count with no scenes"""
        agent = FrameFlowAgent()
        page_count = agent._estimate_page_count([])

        assert page_count == 0

    def test_estimate_page_count_multiple_scenes(self, sample_scene):
        """Test page count with multiple scenes"""
        agent = FrameFlowAgent()
        scenes = [sample_scene] * 5
        page_count = agent._estimate_page_count(scenes)

        assert page_count > 0
        # Should be roughly 2 pages per scene
        assert page_count == 10

    @pytest.mark.asyncio
    async def test_generate_title(self):
        """Test title generation"""
        agent = FrameFlowAgent()

        story_analysis = {"main_theme": "revenge"}
        title = await agent._generate_title(story_analysis, "Action")

        assert isinstance(title, str)
        assert len(title) > 0


class TestErrorHandling:
    """Test error handling"""

    @pytest.mark.asyncio
    async def test_empty_story_prompt(self):
        """Test handling of empty story prompt"""
        agent = FrameFlowAgent()

        # This should be caught by Pydantic validation
        with pytest.raises(Exception):
            story_input = StoryInput(prompt="")
            await agent.generate_screenplay(story_input)

    @pytest.mark.asyncio
    async def test_invalid_genre(self):
        """Test handling of invalid inputs"""
        agent = FrameFlowAgent()

        # Should still work as genre is just a string
        story_input = StoryInput(
            prompt="A test story for validation",
            genre="InvalidGenre"
        )

        # Should not raise error
        screenplay = await agent.generate_screenplay(story_input)
        assert screenplay is not None


class TestIntegrationWorkflow:
    """Test complete workflow integration"""

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_full_workflow(self, sample_story_input, tmp_path):
        """Test complete workflow from input to export"""
        agent = FrameFlowAgent()
        agent.output_dir = str(tmp_path)

        # Step 1: Generate screenplay
        screenplay = await agent.generate_screenplay(sample_story_input)
        assert screenplay is not None

        # Step 2: Generate storyboard
        screenplay_text = screenplay.to_formatted_text()
        storyboard = await agent.generate_storyboard(
            screenplay_text=screenplay_text,
            num_frames=4,
            visual_style="Realistic"
        )
        assert len(storyboard.frames) == 4

        # Step 3: Export screenplay
        pdf_path = await agent.export_screenplay_pdf(screenplay_text)
        assert pdf_path is not None

        # Step 4: Export storyboard
        frame_images = [(f.image_path, f.description) for f in storyboard.frames]
        zip_path = await agent.export_storyboard_pack(frame_images)
        assert zip_path is not None
