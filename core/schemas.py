"""
FrameFlow - Data Models and Schemas
Pydantic models for type safety and validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


class Genre(str, Enum):
    """Available genres for screenplay"""
    DRAMA = "Drama"
    COMEDY = "Comedy"
    THRILLER = "Thriller"
    SCI_FI = "Sci-Fi"
    HORROR = "Horror"
    ROMANCE = "Romance"
    ACTION = "Action"
    MYSTERY = "Mystery"


class DialogueStyle(str, Enum):
    """Available dialogue styles"""
    REALISTIC = "Realistic"
    STYLIZED = "Stylized"
    PERIOD_SPECIFIC = "Period-Specific"
    WITTY = "Witty"
    MINIMAL = "Minimal"


class ActStructure(str, Enum):
    """Story structure templates"""
    THREE_ACT = "Three-Act"
    FIVE_ACT = "Five-Act"
    HEROS_JOURNEY = "Hero's Journey"


class VisualStyle(str, Enum):
    """Visual styles for storyboard"""
    REALISTIC = "Realistic"
    ILLUSTRATED = "Illustrated"
    NOIR = "Noir"
    ANIME = "Anime"
    SKETCH = "Sketch"


class CameraAngle(str, Enum):
    """Camera angles for storyboard frames"""
    WIDE_SHOT = "Wide Shot"
    MEDIUM_SHOT = "Medium Shot"
    CLOSE_UP = "Close-Up"
    EXTREME_CLOSE_UP = "Extreme Close-Up"
    POV = "POV (Point of View)"
    OVER_SHOULDER = "Over the Shoulder"
    BIRDS_EYE = "Bird's Eye View"
    LOW_ANGLE = "Low Angle"
    HIGH_ANGLE = "High Angle"


# Input Models

class StoryInput(BaseModel):
    """User input for story generation"""
    prompt: str = Field(..., min_length=10, description="Story idea or prompt")
    genre: str = Field(default="Drama", description="Story genre")
    dialogue_style: str = Field(default="Realistic", description="Dialogue style")
    act_structure: str = Field(default="Three-Act", description="Story structure")


# Character Models

class CharacterProfile(BaseModel):
    """Character profile with personality and visual traits"""
    name: str
    age: Optional[int] = None
    role: str  # protagonist, antagonist, supporting
    description: str
    personality_traits: List[str] = []
    visual_description: str  # For image generation
    motivation: Optional[str] = None
    arc: Optional[str] = None
    embedding_id: Optional[str] = None  # For consistency tracking


# Scene Models

class SceneLocation(BaseModel):
    """Scene location details"""
    setting: str  # INT/EXT
    location: str
    time: str  # DAY/NIGHT


class DialogueLine(BaseModel):
    """Single line of dialogue"""
    character: str
    line: str
    parenthetical: Optional[str] = None  # (angry), (whispers), etc.


class Scene(BaseModel):
    """Single screenplay scene"""
    scene_number: int
    location: SceneLocation
    action: str  # Scene description and action
    dialogue: List[DialogueLine] = []
    page_number: Optional[int] = None


# Screenplay Models

class ScreenplayMetadata(BaseModel):
    """Screenplay metadata"""
    title: str
    author: str = "FrameFlow Agent"
    draft: str = "First Draft"
    created_at: datetime = Field(default_factory=datetime.now)
    genre: str
    logline: Optional[str] = None


class ScreenplayOutput(BaseModel):
    """Complete screenplay output"""
    metadata: ScreenplayMetadata
    characters: List[CharacterProfile]
    scenes: List[Scene]
    page_count: int = 0

    def to_formatted_text(self) -> str:
        """Convert screenplay to industry-standard formatted text"""
        lines = []

        # Title page
        lines.append(f"{self.metadata.title.upper()}")
        lines.append(f"\nby {self.metadata.author}")
        lines.append(f"\n{self.metadata.draft}")
        lines.append(f"\n{self.metadata.created_at.strftime('%B %d, %Y')}")
        lines.append("\n" + "="*60 + "\n")

        # Characters
        if self.characters:
            lines.append("\nCHARACTERS:\n")
            for char in self.characters:
                age_str = f", {char.age}" if char.age else ""
                lines.append(f"  {char.name.upper()}{age_str} - {char.description}")
            lines.append("\n" + "="*60 + "\n")

        # Scenes
        for scene in self.scenes:
            # Scene heading
            heading = f"{scene.scene_number}. {scene.location.setting}. {scene.location.location} - {scene.location.time}"
            lines.append(f"\n{heading.upper()}\n")

            # Action
            if scene.action:
                lines.append(f"{scene.action}\n")

            # Dialogue
            for dialogue in scene.dialogue:
                lines.append(f"\n{' ' * 20}{dialogue.character.upper()}")
                if dialogue.parenthetical:
                    lines.append(f"{' ' * 15}({dialogue.parenthetical})")
                lines.append(f"{' ' * 10}{dialogue.line}\n")

        return "\n".join(lines)


# Storyboard Models

class StoryboardFrame(BaseModel):
    """Single storyboard frame"""
    frame_number: int
    scene_reference: int  # References scene number
    description: str
    camera_angle: str
    visual_prompt: str  # Detailed prompt for image generation
    image_path: Optional[str] = None
    image_url: Optional[str] = None


class StoryboardOutput(BaseModel):
    """Complete storyboard output"""
    screenplay_title: str
    frames: List[StoryboardFrame]
    visual_style: str
    created_at: datetime = Field(default_factory=datetime.now)


# MCP Tool Schemas

class StoryAnalysis(BaseModel):
    """Output from story analysis tool"""
    main_theme: str
    conflict: str
    protagonist: str
    antagonist: Optional[str] = None
    setting: str
    suggested_acts: List[str]
    key_plot_points: List[str]


class VisualPromptOutput(BaseModel):
    """Output from visual prompt generation"""
    base_prompt: str
    character_descriptions: List[str]
    lighting: str
    composition: str
    mood: str
    style_modifiers: List[str]


# Export Models

class ExportOptions(BaseModel):
    """Options for export"""
    format: str  # pdf, docx, zip
    include_metadata: bool = True
    page_numbers: bool = True
    watermark: Optional[str] = None


class ExportResult(BaseModel):
    """Result of export operation"""
    success: bool
    file_path: Optional[str] = None
    error_message: Optional[str] = None
    file_size_bytes: Optional[int] = None
