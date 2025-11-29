"""
FrameFlow - Main Agent Orchestration
Coordinates MCP servers and manages the screenplay generation workflow
"""

import asyncio
import os
from typing import List, Optional, Dict, Any
from datetime import datetime
import json

from core.schemas import (
    StoryInput,
    ScreenplayOutput,
    ScreenplayMetadata,
    StoryboardOutput,
    CharacterProfile,
    Scene,
    StoryboardFrame,
    SceneLocation,
    DialogueLine,
    ExportResult
)
from core.prompts import (
    create_story_analysis_prompt,
    create_character_prompt,
    create_scene_prompt,
    create_visual_prompt,
    SYSTEM_PROMPT_CREATIVE
)

# Import MCP server modules
from mcp_servers.screenplay_generator.story_analyzer import StoryStructureAnalyzer
from mcp_servers.screenplay_generator.character_creator import CharacterProfileCreator
from mcp_servers.screenplay_generator.scene_writer import ScreenplaySceneWriter
from mcp_servers.storyboard_visualizer.moment_detector import KeyMomentDetector
from mcp_servers.storyboard_visualizer.prompt_generator import VisualPromptGenerator

# Import API clients
from integrations.sambanova import SambaNovaClient
from integrations.hyperbolic import HyperbolicClient
from integrations.nebius import NebiusClient, CharacterConsistencyManager


class FrameFlowAgent:
    """
    Main FrameFlow agent that orchestrates the screenplay and storyboard generation process
    """

    def __init__(self):
        """Initialize the FrameFlow agent with necessary clients"""
        self.character_store: Dict[str, CharacterProfile] = {}
        self.output_dir = os.path.join(os.getcwd(), "outputs")
        os.makedirs(self.output_dir, exist_ok=True)

        # Initialize API clients
        self.llm_client = None
        self.image_client = None
        self.embedding_client = None

        # Initialize MCP modules
        self.story_analyzer = None
        self.character_creator = None
        self.scene_writer = None
        self.moment_detector = None
        self.prompt_generator = None
        self.consistency_manager = None

        # Initialize clients on first use
        self._clients_initialized = False

    def _initialize_clients(self):
        """Initialize API clients and MCP modules"""
        if self._clients_initialized:
            return

        try:
            # Initialize LLM client (SambaNova)
            self.llm_client = SambaNovaClient()
            print("✓ SambaNova LLM client initialized")
        except Exception as e:
            print(f"⚠ SambaNova client unavailable: {e}")

        try:
            # Initialize image client (Hyperbolic)
            self.image_client = HyperbolicClient()
            print("✓ Hyperbolic image client initialized")
        except Exception as e:
            print(f"⚠ Hyperbolic client unavailable: {e}")

        try:
            # Initialize embedding client (Nebius)
            self.embedding_client = NebiusClient()
            self.consistency_manager = CharacterConsistencyManager(self.embedding_client)
            print("✓ Nebius embedding client initialized")
        except Exception as e:
            print(f"⚠ Nebius client unavailable: {e}")

        # Initialize MCP modules
        self.story_analyzer = StoryStructureAnalyzer(self.llm_client)
        self.character_creator = CharacterProfileCreator(self.llm_client)
        self.scene_writer = ScreenplaySceneWriter(self.llm_client)
        self.moment_detector = KeyMomentDetector(self.llm_client)
        self.prompt_generator = VisualPromptGenerator(self.llm_client)

        self._clients_initialized = True
        print("✓ All MCP modules initialized")

    async def generate_screenplay(self, story_input: StoryInput) -> ScreenplayOutput:
        """
        Generate a complete screenplay from story input

        Args:
            story_input: User's story prompt and preferences

        Returns:
            ScreenplayOutput with complete screenplay
        """
        # Initialize clients if not already done
        self._initialize_clients()

        print(f"🎬 Starting screenplay generation for {story_input.genre} story...")

        # Step 1: Analyze story
        print("📊 Analyzing story structure...")
        story_analysis = await self._analyze_story(story_input)

        # Step 2: Create characters
        print("👥 Creating character profiles...")
        characters = await self._create_characters(story_analysis, story_input.genre)

        # Step 3: Generate title and metadata
        print("📝 Generating metadata...")
        title = await self._generate_title(story_analysis, story_input.genre)
        metadata = ScreenplayMetadata(
            title=title,
            genre=story_input.genre,
            logline=story_analysis.get("logline", "")
        )

        # Step 4: Write scenes
        print("🎞️ Writing scenes...")
        scenes = await self._write_scenes(
            story_analysis=story_analysis,
            characters=characters,
            act_structure=story_input.act_structure,
            dialogue_style=story_input.dialogue_style,
            genre=story_input.genre
        )

        # Create screenplay output
        screenplay = ScreenplayOutput(
            metadata=metadata,
            characters=characters,
            scenes=scenes,
            page_count=self._estimate_page_count(scenes)
        )

        print(f"✅ Screenplay complete! {len(scenes)} scenes, {len(characters)} characters")
        return screenplay

    async def generate_storyboard(
        self,
        screenplay_text: str,
        num_frames: int = 8,
        visual_style: str = "Realistic"
    ) -> StoryboardOutput:
        """
        Generate storyboard frames from screenplay

        Args:
            screenplay_text: Generated screenplay text
            num_frames: Number of frames to generate
            visual_style: Visual style for frames

        Returns:
            StoryboardOutput with generated frames
        """
        # Initialize clients if not already done
        self._initialize_clients()

        print(f"🎨 Starting storyboard generation ({num_frames} frames)...")

        # Step 1: Identify key moments
        print("🔍 Identifying key moments...")
        key_moments = await self._identify_key_moments(screenplay_text, num_frames)

        # Step 2: Generate frames
        print("🖼️ Generating storyboard frames...")
        frames = []
        for i, moment in enumerate(key_moments):
            print(f"  Frame {i+1}/{num_frames}...")
            frame = await self._generate_storyboard_frame(
                moment=moment,
                frame_number=i + 1,
                visual_style=visual_style
            )
            frames.append(frame)

        storyboard = StoryboardOutput(
            screenplay_title="Generated Screenplay",
            frames=frames,
            visual_style=visual_style
        )

        print(f"✅ Storyboard complete! {len(frames)} frames generated")
        return storyboard

    async def _analyze_story(self, story_input: StoryInput) -> Dict[str, Any]:
        """
        Analyze story prompt and extract key elements using story analyzer

        Returns a dictionary with story analysis
        """
        if self.story_analyzer:
            # Use MCP story analyzer module
            return await self.story_analyzer.analyze(story_input)
        else:
            # Fallback implementation
            return {
                "main_theme": "Personal growth and redemption",
                "conflict": "Internal and external obstacles",
                "protagonist": "A determined individual",
                "antagonist": "Forces of opposition",
                "setting": "Contemporary urban setting",
                "key_plot_points": [
                    "Inciting incident",
                    "First turning point",
                    "Midpoint reversal",
                    "Dark night of the soul",
                    "Climax",
                    "Resolution"
                ],
                "suggested_acts": ["Setup", "Confrontation", "Resolution"],
                "logline": f"A {story_input.genre.lower()} story about {story_input.prompt[:100]}..."
            }

    async def _create_characters(
        self,
        story_analysis: Dict[str, Any],
        genre: str
    ) -> List[CharacterProfile]:
        """
        Create character profiles using character creator module

        Returns list of CharacterProfile objects
        """
        if self.character_creator:
            # Use MCP character creator module
            characters = await self.character_creator.create_characters(
                story_analysis=story_analysis,
                genre=genre,
                num_characters=3
            )
        else:
            # Fallback implementation
            characters = [
                CharacterProfile(
                    name="Alex Morgan",
                    age=32,
                    role="protagonist",
                    description="A resourceful detective with a troubled past",
                    personality_traits=["determined", "intelligent", "haunted", "compassionate"],
                    visual_description="Tall, athletic build, short dark hair, piercing blue eyes, typically wears a leather jacket and jeans",
                    motivation="To find redemption by solving this case",
                    arc="From cynical loner to team player who learns to trust"
                )
            ]

        # Store characters for consistency
        for char in characters:
            self.character_store[char.name] = char

            # Store in consistency manager if available
            if self.consistency_manager:
                try:
                    await self.consistency_manager.store_character(
                        character_name=char.name,
                        visual_description=char.visual_description,
                        metadata={"age": char.age, "role": char.role}
                    )
                except:
                    pass  # Continue even if embedding storage fails

        return characters

    async def _generate_title(self, story_analysis: Dict[str, Any], genre: str) -> str:
        """Generate screenplay title"""
        # Placeholder - would use LLM in real implementation
        return f"Untitled {genre} Project"

    async def _write_scenes(
        self,
        story_analysis: Dict[str, Any],
        characters: List[CharacterProfile],
        act_structure: str,
        dialogue_style: str,
        genre: str
    ) -> List[Scene]:
        """
        Write screenplay scenes using scene writer module

        Returns list of Scene objects
        """
        scenes = []

        if self.story_analyzer and self.scene_writer:
            # Identify key scenes from story analysis
            scene_outlines = self.story_analyzer.identify_key_scenes(
                story_analysis,
                num_scenes=8  # Generate 8 scenes for a short screenplay
            )

            # Write each scene
            for outline in scene_outlines:
                scene = await self.scene_writer.write_scene(
                    scene_outline=outline,
                    characters=characters,
                    dialogue_style=dialogue_style,
                    genre=genre
                )
                scenes.append(scene)
        else:
            # Fallback: create basic scenes
            scenes = [
                Scene(
                    scene_number=1,
                    location=SceneLocation(
                        setting="INT",
                        location="LOCATION",
                        time="DAY"
                    ),
                    action=f"The story begins in {story_analysis.get('setting', 'a location')}.",
                    dialogue=[]
                )
            ]

        return scenes

    async def _identify_key_moments(
        self,
        screenplay_text: str,
        num_frames: int
    ) -> List[Dict[str, Any]]:
        """
        Identify key moments using moment detector module

        Returns list of moment descriptions
        """
        if self.moment_detector:
            # Use MCP moment detector module
            return self.moment_detector.identify_key_moments(
                screenplay_text,
                num_frames
            )
        else:
            # Fallback implementation
            moments = []
            for i in range(num_frames):
                moments.append({
                    "scene_number": i + 1,
                    "description": f"Key moment {i + 1} from the screenplay",
                    "emotional_tone": "dramatic",
                    "characters": [],
                    "setting": "Location"
                })
            return moments

    async def _generate_storyboard_frame(
        self,
        moment: Dict[str, Any],
        frame_number: int,
        visual_style: str
    ) -> StoryboardFrame:
        """
        Generate a single storyboard frame with image

        Returns StoryboardFrame object
        """
        # Get camera angle suggestion
        camera_angle = "Medium Shot"
        if self.moment_detector:
            camera_angle = self.moment_detector.suggest_camera_angles(moment)

        # Generate visual prompt
        visual_prompt = f"{visual_style} style storyboard frame: {moment['description']}"
        if self.prompt_generator:
            # Get character data for consistency
            char_data = [
                {"name": name, "visual_description": self.get_character_consistency(name) or f"character {name}"}
                for name in moment.get("characters", [])
            ]

            visual_prompt = self.prompt_generator.generate_visual_prompt(
                moment=moment,
                visual_style=visual_style,
                camera_angle=camera_angle,
                characters=char_data if char_data else None
            )

        # Generate image
        image_path = None
        if self.image_client:
            try:
                # Generate image
                image_bytes = await self.image_client.generate_storyboard_frame(
                    prompt=visual_prompt,
                    style=visual_style.lower(),
                    aspect_ratio="16:9",
                    quality="standard"
                )

                # Save image
                frame_filename = f"frame_{frame_number:03d}.png"
                image_path = os.path.join(self.output_dir, frame_filename)
                await self.image_client.save_image(image_bytes, image_path)

                print(f"  ✓ Generated image: {image_path}")
            except Exception as e:
                print(f"  ⚠ Image generation failed: {e}")

        frame = StoryboardFrame(
            frame_number=frame_number,
            scene_reference=moment.get("scene_number", frame_number),
            description=moment.get("description", "Scene description"),
            camera_angle=camera_angle,
            visual_prompt=visual_prompt,
            image_path=image_path,
            image_url=None
        )

        return frame

    def _estimate_page_count(self, scenes: List[Scene]) -> int:
        """Estimate screenplay page count (1 page ≈ 1 minute of screen time)"""
        # Rough estimate: each scene averages 2-3 pages
        return len(scenes) * 2

    async def export_screenplay_pdf(self, screenplay_text: str) -> str:
        """
        Export screenplay as PDF

        Args:
            screenplay_text: Formatted screenplay text

        Returns:
            Path to generated PDF
        """
        # Placeholder implementation
        # In real implementation, this would use document-exporter MCP server
        output_path = os.path.join(self.output_dir, f"screenplay_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")

        print(f"📄 Exporting screenplay to PDF: {output_path}")

        # This would use ReportLab or similar to create proper PDF
        # For now, just create a placeholder file
        with open(output_path, "w") as f:
            f.write("PDF Export - To be implemented")

        return output_path

    async def export_storyboard_pack(self, frame_images: List) -> str:
        """
        Export storyboard frames as ZIP

        Args:
            frame_images: List of frame images

        Returns:
            Path to generated ZIP file
        """
        # Placeholder implementation
        output_path = os.path.join(self.output_dir, f"storyboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip")

        print(f"📦 Exporting storyboard to ZIP: {output_path}")

        # This would create actual ZIP with images
        # For now, just create a placeholder file
        with open(output_path, "w") as f:
            f.write("ZIP Export - To be implemented")

        return output_path

    def get_character_consistency(self, character_name: str) -> Optional[str]:
        """
        Get consistent visual description for a character

        Args:
            character_name: Name of the character

        Returns:
            Visual description or None if character not found
        """
        character = self.character_store.get(character_name)
        if character:
            return character.visual_description
        return None
