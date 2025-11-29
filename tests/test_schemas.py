"""
Tests for core/schemas.py
Validate Pydantic models and data structures
"""

import pytest
from datetime import datetime
from pydantic import ValidationError

from core.schemas import (
    StoryInput,
    CharacterProfile,
    Scene,
    SceneLocation,
    DialogueLine,
    ScreenplayMetadata,
    ScreenplayOutput,
    StoryboardFrame,
    StoryboardOutput,
    Genre,
    DialogueStyle,
    ActStructure,
    VisualStyle,
    CameraAngle
)


class TestStoryInput:
    """Test StoryInput model"""

    def test_valid_story_input(self):
        """Test creating valid story input"""
        story = StoryInput(
            prompt="A detective story",
            genre="Thriller",
            dialogue_style="Realistic",
            act_structure="Three-Act"
        )

        assert story.prompt == "A detective story"
        assert story.genre == "Thriller"
        assert story.dialogue_style == "Realistic"
        assert story.act_structure == "Three-Act"

    def test_story_input_defaults(self):
        """Test default values"""
        story = StoryInput(prompt="A simple story")

        assert story.genre == "Drama"
        assert story.dialogue_style == "Realistic"
        assert story.act_structure == "Three-Act"

    def test_story_input_validation_too_short(self):
        """Test prompt length validation"""
        with pytest.raises(ValidationError) as exc_info:
            StoryInput(prompt="Short")

        assert "at least 10 characters" in str(exc_info.value)


class TestCharacterProfile:
    """Test CharacterProfile model"""

    def test_valid_character(self, sample_character):
        """Test creating valid character"""
        assert sample_character.name == "Alex Morgan"
        assert sample_character.age == 35
        assert sample_character.role == "protagonist"
        assert len(sample_character.personality_traits) == 4

    def test_character_without_optional_fields(self):
        """Test character with minimal required fields"""
        char = CharacterProfile(
            name="John Doe",
            role="supporting",
            description="A mysterious figure",
            visual_description="Tall and slim"
        )

        assert char.name == "John Doe"
        assert char.age is None
        assert char.motivation is None
        assert char.embedding_id is None


class TestScene:
    """Test Scene model"""

    def test_valid_scene(self, sample_scene):
        """Test creating valid scene"""
        assert sample_scene.scene_number == 1
        assert sample_scene.location.setting == "INT"
        assert sample_scene.location.location == "DETECTIVE'S OFFICE"
        assert len(sample_scene.dialogue) == 2

    def test_scene_location(self):
        """Test scene location"""
        location = SceneLocation(
            setting="EXT",
            location="CITY STREET",
            time="NIGHT"
        )

        assert location.setting == "EXT"
        assert location.location == "CITY STREET"
        assert location.time == "NIGHT"

    def test_dialogue_line(self):
        """Test dialogue line"""
        dialogue = DialogueLine(
            character="ALEX",
            line="This is a test.",
            parenthetical="whispering"
        )

        assert dialogue.character == "ALEX"
        assert dialogue.line == "This is a test."
        assert dialogue.parenthetical == "whispering"

    def test_dialogue_without_parenthetical(self):
        """Test dialogue without parenthetical"""
        dialogue = DialogueLine(
            character="ALEX",
            line="This is a test."
        )

        assert dialogue.parenthetical is None


class TestScreenplayOutput:
    """Test ScreenplayOutput model"""

    def test_valid_screenplay(self, sample_screenplay):
        """Test creating valid screenplay"""
        assert sample_screenplay.metadata.title == "The Time Killer"
        assert len(sample_screenplay.characters) == 2
        assert len(sample_screenplay.scenes) == 1
        assert sample_screenplay.page_count == 2

    def test_screenplay_to_formatted_text(self, sample_screenplay):
        """Test screenplay formatting"""
        formatted = sample_screenplay.to_formatted_text()

        assert "THE TIME KILLER" in formatted
        assert "FrameFlow Agent" in formatted
        assert "CHARACTERS:" in formatted
        assert "INT. DETECTIVE'S OFFICE - DAY" in formatted
        assert "ALEX" in formatted

    def test_screenplay_metadata(self, sample_screenplay_metadata):
        """Test screenplay metadata"""
        assert sample_screenplay_metadata.title == "The Time Killer"
        assert sample_screenplay_metadata.author == "FrameFlow Agent"
        assert sample_screenplay_metadata.genre == "Thriller"
        assert isinstance(sample_screenplay_metadata.created_at, datetime)


class TestStoryboardOutput:
    """Test StoryboardOutput model"""

    def test_valid_storyboard(self, sample_storyboard):
        """Test creating valid storyboard"""
        assert sample_storyboard.screenplay_title == "The Time Killer"
        assert len(sample_storyboard.frames) == 1
        assert sample_storyboard.visual_style == "Noir"

    def test_storyboard_frame(self, sample_storyboard_frame):
        """Test storyboard frame"""
        assert sample_storyboard_frame.frame_number == 1
        assert sample_storyboard_frame.scene_reference == 1
        assert sample_storyboard_frame.camera_angle == "Medium Shot"
        assert sample_storyboard_frame.image_path == "/tmp/frame_001.png"


class TestEnums:
    """Test enum types"""

    def test_genre_enum(self):
        """Test Genre enum"""
        assert Genre.DRAMA == "Drama"
        assert Genre.THRILLER == "Thriller"
        assert Genre.SCI_FI == "Sci-Fi"

    def test_dialogue_style_enum(self):
        """Test DialogueStyle enum"""
        assert DialogueStyle.REALISTIC == "Realistic"
        assert DialogueStyle.STYLIZED == "Stylized"
        assert DialogueStyle.WITTY == "Witty"

    def test_act_structure_enum(self):
        """Test ActStructure enum"""
        assert ActStructure.THREE_ACT == "Three-Act"
        assert ActStructure.FIVE_ACT == "Five-Act"
        assert ActStructure.HEROS_JOURNEY == "Hero's Journey"

    def test_visual_style_enum(self):
        """Test VisualStyle enum"""
        assert VisualStyle.REALISTIC == "Realistic"
        assert VisualStyle.NOIR == "Noir"
        assert VisualStyle.ANIME == "Anime"

    def test_camera_angle_enum(self):
        """Test CameraAngle enum"""
        assert CameraAngle.WIDE_SHOT == "Wide Shot"
        assert CameraAngle.CLOSE_UP == "Close-Up"
        assert CameraAngle.POV == "POV (Point of View)"


class TestDataValidation:
    """Test data validation and edge cases"""

    def test_empty_dialogue_list(self):
        """Test scene with empty dialogue"""
        scene = Scene(
            scene_number=1,
            location=SceneLocation(
                setting="INT",
                location="ROOM",
                time="DAY"
            ),
            action="Empty room.",
            dialogue=[]
        )

        assert len(scene.dialogue) == 0

    def test_multiple_characters(self):
        """Test screenplay with multiple characters"""
        chars = [
            CharacterProfile(
                name=f"Character {i}",
                role="supporting",
                description=f"Description {i}",
                visual_description=f"Visual {i}"
            )
            for i in range(5)
        ]

        assert len(chars) == 5
        assert chars[0].name == "Character 0"
        assert chars[4].name == "Character 4"

    def test_screenplay_with_no_scenes(self):
        """Test screenplay with empty scene list"""
        screenplay = ScreenplayOutput(
            metadata=ScreenplayMetadata(
                title="Empty",
                genre="Drama"
            ),
            characters=[],
            scenes=[],
            page_count=0
        )

        assert len(screenplay.scenes) == 0
        assert screenplay.page_count == 0

    def test_character_traits_list(self):
        """Test character with various traits"""
        char = CharacterProfile(
            name="Test Character",
            role="protagonist",
            description="Test",
            visual_description="Test visual",
            personality_traits=["brave", "intelligent", "kind", "determined", "loyal"]
        )

        assert len(char.personality_traits) == 5
        assert "brave" in char.personality_traits


class TestFormattedOutput:
    """Test formatted output generation"""

    def test_screenplay_formatting_with_multiple_scenes(self, sample_character):
        """Test formatting with multiple scenes"""
        scenes = [
            Scene(
                scene_number=i,
                location=SceneLocation(
                    setting="INT" if i % 2 == 0 else "EXT",
                    location=f"LOCATION {i}",
                    time="DAY" if i % 2 == 0 else "NIGHT"
                ),
                action=f"Action for scene {i}",
                dialogue=[]
            )
            for i in range(1, 4)
        ]

        screenplay = ScreenplayOutput(
            metadata=ScreenplayMetadata(
                title="Test Screenplay",
                genre="Drama"
            ),
            characters=[sample_character],
            scenes=scenes,
            page_count=3
        )

        formatted = screenplay.to_formatted_text()

        assert "1. INT. LOCATION 1 - DAY" in formatted
        assert "2. EXT. LOCATION 2 - NIGHT" in formatted
        assert "3. INT. LOCATION 3 - DAY" in formatted

    def test_dialogue_formatting_in_screenplay(self):
        """Test dialogue formatting"""
        dialogue = DialogueLine(
            character="SARAH",
            line="What's going on here?",
            parenthetical="confused"
        )

        scene = Scene(
            scene_number=1,
            location=SceneLocation(
                setting="INT",
                location="ROOM",
                time="DAY"
            ),
            action="Characters talk.",
            dialogue=[dialogue]
        )

        screenplay = ScreenplayOutput(
            metadata=ScreenplayMetadata(title="Test", genre="Drama"),
            characters=[],
            scenes=[scene],
            page_count=1
        )

        formatted = screenplay.to_formatted_text()

        assert "SARAH" in formatted
        assert "(confused)" in formatted
        assert "What's going on here?" in formatted
