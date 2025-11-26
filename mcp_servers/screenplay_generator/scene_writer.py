"""
Scene Writer Module
Writes screenplay scenes with proper formatting, action lines, and dialogue
"""

from typing import List, Dict, Any, Optional
import re

from core.schemas import Scene, SceneLocation, DialogueLine, CharacterProfile
from core.prompts import (
    create_scene_prompt,
    DIALOGUE_GENERATION_PROMPT,
    format_prompt,
    SYSTEM_PROMPT_CREATIVE
)


class ScreenplaySceneWriter:
    """
    Writes formatted screenplay scenes with action and dialogue
    """

    def __init__(self, llm_client=None):
        """
        Initialize scene writer

        Args:
            llm_client: LLM client for generating scenes
        """
        self.llm_client = llm_client
        self.scene_types = self._load_scene_types()
        self.location_prefixes = ["INT", "EXT", "INT/EXT"]
        self.time_codes = ["DAY", "NIGHT", "DAWN", "DUSK", "CONTINUOUS"]

    async def write_scene(
        self,
        scene_outline: Dict[str, Any],
        characters: List[CharacterProfile],
        dialogue_style: str = "Realistic",
        genre: str = "Drama"
    ) -> Scene:
        """
        Write a complete screenplay scene

        Args:
            scene_outline: Scene outline with purpose, setting, etc.
            characters: List of character profiles
            dialogue_style: Style of dialogue
            genre: Genre for context

        Returns:
            Scene object with action and dialogue
        """
        scene_number = scene_outline.get("scene_number", 1)
        location = self._parse_location(scene_outline.get("location", "INT. LOCATION - DAY"))

        if self.llm_client:
            # Generate scene using LLM
            scene = await self._generate_with_llm(
                scene_outline,
                characters,
                dialogue_style,
                genre
            )
        else:
            # Fallback: basic scene generation
            scene = self._generate_basic_scene(
                scene_outline,
                characters,
                location
            )

        return scene

    async def _generate_with_llm(
        self,
        scene_outline: Dict[str, Any],
        characters: List[CharacterProfile],
        dialogue_style: str,
        genre: str
    ) -> Scene:
        """
        Generate scene using LLM

        Args:
            scene_outline: Scene outline
            characters: Character profiles
            dialogue_style: Dialogue style
            genre: Genre

        Returns:
            Generated Scene object
        """
        # Prepare character information
        chars_json = self._format_characters_for_prompt(characters)

        # Create scene prompt
        location_str = scene_outline.get("location", "INT. LOCATION - DAY")
        parsed_location = self._parse_location(location_str)

        prompt = create_scene_prompt(
            scene_number=scene_outline.get("scene_number", 1),
            act=scene_outline.get("act", "Act 1"),
            location=location_str,
            time=parsed_location.time,
            purpose=scene_outline.get("purpose", "Advance the story"),
            characters=chars_json,
            context=scene_outline.get("context", scene_outline.get("purpose", "")),
            dialogue_style=dialogue_style,
            genre=genre
        )

        # Generate scene text
        scene_text = await self.llm_client.generate(
            prompt=prompt,
            system_prompt=SYSTEM_PROMPT_CREATIVE,
            temperature=0.75,
            max_tokens=2000
        )

        # Parse the generated scene
        scene = self._parse_scene_text(
            scene_text,
            scene_outline.get("scene_number", 1),
            parsed_location
        )

        return scene

    def _parse_scene_text(
        self,
        scene_text: str,
        scene_number: int,
        location: SceneLocation
    ) -> Scene:
        """
        Parse LLM-generated scene text into Scene object

        Args:
            scene_text: Generated scene text
            scene_number: Scene number
            location: Scene location

        Returns:
            Parsed Scene object
        """
        # Extract action (text that's not dialogue or scene headings)
        action_lines = []
        dialogue_list = []

        lines = scene_text.split('\n')
        current_action = []
        current_character = None
        current_parenthetical = None

        for line in lines:
            stripped = line.strip()

            # Skip empty lines and scene headings
            if not stripped or self._is_scene_heading(stripped):
                continue

            # Check if it's a character name (all caps, centered)
            if stripped.isupper() and len(stripped.split()) <= 3 and len(stripped) < 30:
                # Save any accumulated action
                if current_action:
                    action_lines.append(' '.join(current_action))
                    current_action = []

                current_character = stripped
                current_parenthetical = None
                continue

            # Check if it's a parenthetical
            if stripped.startswith('(') and stripped.endswith(')'):
                current_parenthetical = stripped[1:-1]
                continue

            # If we have a current character, this is dialogue
            if current_character:
                dialogue_list.append(DialogueLine(
                    character=current_character,
                    line=stripped,
                    parenthetical=current_parenthetical
                ))
                current_character = None
                current_parenthetical = None
            else:
                # It's action
                current_action.append(stripped)

        # Add any remaining action
        if current_action:
            action_lines.append(' '.join(current_action))

        action_text = '\n\n'.join(action_lines)

        return Scene(
            scene_number=scene_number,
            location=location,
            action=action_text,
            dialogue=dialogue_list
        )

    def _generate_basic_scene(
        self,
        scene_outline: Dict[str, Any],
        characters: List[CharacterProfile],
        location: SceneLocation
    ) -> Scene:
        """
        Generate basic scene without LLM (fallback)

        Args:
            scene_outline: Scene outline
            characters: Characters
            location: Location

        Returns:
            Basic Scene object
        """
        purpose = scene_outline.get("purpose", "Scene action")

        # Basic action description
        action = f"The scene takes place in {location.location.lower()}. {purpose}"

        # Basic dialogue
        dialogue = []
        if len(characters) >= 2:
            dialogue.append(DialogueLine(
                character=characters[0].name.upper(),
                line=f"We need to discuss what happens next."
            ))
            dialogue.append(DialogueLine(
                character=characters[1].name.upper(),
                line="I understand. What do you propose?"
            ))

        return Scene(
            scene_number=scene_outline.get("scene_number", 1),
            location=location,
            action=action,
            dialogue=dialogue
        )

    async def generate_dialogue(
        self,
        context: str,
        characters: List[CharacterProfile],
        style: str = "Realistic",
        tone: str = "neutral",
        num_exchanges: int = 5
    ) -> List[DialogueLine]:
        """
        Generate dialogue for characters

        Args:
            context: Scene context
            characters: Characters in conversation
            style: Dialogue style
            tone: Emotional tone
            num_exchanges: Number of exchanges

        Returns:
            List of dialogue lines
        """
        if not self.llm_client:
            return self._generate_basic_dialogue(characters, num_exchanges)

        # Format characters for prompt
        chars_str = self._format_characters_for_prompt(characters)

        # Create dialogue prompt
        prompt = format_prompt(
            DIALOGUE_GENERATION_PROMPT,
            characters=chars_str,
            context=context,
            dialogue_style=style,
            genre="Drama",  # Could be passed as parameter
            tone=tone
        )

        prompt += f"\n\nGenerate approximately {num_exchanges} exchanges."

        # Generate dialogue
        dialogue_text = await self.llm_client.generate(
            prompt=prompt,
            system_prompt=SYSTEM_PROMPT_CREATIVE,
            temperature=0.85,
            max_tokens=1500
        )

        # Parse dialogue
        dialogue_lines = self._parse_dialogue_text(dialogue_text)

        return dialogue_lines

    def _parse_dialogue_text(self, dialogue_text: str) -> List[DialogueLine]:
        """
        Parse dialogue text into DialogueLine objects

        Args:
            dialogue_text: Generated dialogue text

        Returns:
            List of DialogueLine objects
        """
        dialogue_lines = []
        lines = dialogue_text.split('\n')

        current_character = None
        current_parenthetical = None

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            # Character name (all caps)
            if stripped.isupper() and len(stripped.split()) <= 3:
                current_character = stripped
                current_parenthetical = None
                continue

            # Parenthetical
            if stripped.startswith('(') and stripped.endswith(')'):
                current_parenthetical = stripped[1:-1]
                continue

            # Dialogue line
            if current_character:
                dialogue_lines.append(DialogueLine(
                    character=current_character,
                    line=stripped,
                    parenthetical=current_parenthetical
                ))
                current_parenthetical = None

        return dialogue_lines

    def _generate_basic_dialogue(
        self,
        characters: List[CharacterProfile],
        num_exchanges: int
    ) -> List[DialogueLine]:
        """Generate basic dialogue without LLM"""
        dialogue = []
        templates = [
            "What do you think we should do?",
            "I'm not sure that's the right approach.",
            "We need to consider all our options.",
            "Time is running out.",
            "I have an idea that might work."
        ]

        for i in range(min(num_exchanges, len(templates))):
            char = characters[i % len(characters)]
            dialogue.append(DialogueLine(
                character=char.name.upper(),
                line=templates[i]
            ))

        return dialogue

    def _parse_location(self, location_str: str) -> SceneLocation:
        """
        Parse location string into SceneLocation object

        Args:
            location_str: Location string (e.g., "INT. OFFICE - DAY")

        Returns:
            SceneLocation object
        """
        # Default values
        setting = "INT"
        location = "LOCATION"
        time = "DAY"

        # Parse the location string
        match = re.match(r'(INT|EXT|INT/EXT)\.?\s*(.+?)\s*-\s*(DAY|NIGHT|DAWN|DUSK|CONTINUOUS)', location_str, re.IGNORECASE)

        if match:
            setting = match.group(1).upper()
            location = match.group(2).strip().upper()
            time = match.group(3).upper()
        else:
            # Try simpler parse
            parts = location_str.split('-')
            if len(parts) >= 2:
                time = parts[-1].strip().upper()
                loc_part = parts[0].strip()

                if loc_part.startswith(('INT', 'EXT')):
                    prefix_match = re.match(r'(INT|EXT|INT/EXT)\.?\s*(.+)', loc_part, re.IGNORECASE)
                    if prefix_match:
                        setting = prefix_match.group(1).upper()
                        location = prefix_match.group(2).strip().upper()

        return SceneLocation(
            setting=setting,
            location=location,
            time=time
        )

    def _is_scene_heading(self, line: str) -> bool:
        """Check if line is a scene heading"""
        return bool(re.match(r'(INT|EXT|INT/EXT)\.?\s+.+\s+-\s+(DAY|NIGHT|DAWN|DUSK|CONTINUOUS)', line, re.IGNORECASE))

    def _format_characters_for_prompt(self, characters: List[CharacterProfile]) -> str:
        """Format characters for inclusion in prompts"""
        char_strings = []
        for char in characters:
            char_str = f"{char.name}: {char.description}"
            if char.personality_traits:
                traits = ", ".join(char.personality_traits[:3])
                char_str += f" ({traits})"
            char_strings.append(char_str)

        return "\n".join(char_strings)

    def _load_scene_types(self) -> Dict[str, Dict[str, Any]]:
        """Load scene type templates"""
        return {
            "opening": {
                "purpose": "Establish world and protagonist",
                "elements": ["setting", "protagonist intro", "normal world"]
            },
            "inciting_incident": {
                "purpose": "Event that starts the story",
                "elements": ["disruption", "call to action", "stakes"]
            },
            "confrontation": {
                "purpose": "Protagonist faces obstacle",
                "elements": ["conflict", "tension", "character growth"]
            },
            "revelation": {
                "purpose": "Important information revealed",
                "elements": ["discovery", "reaction", "decision"]
            },
            "climax": {
                "purpose": "Peak of story tension",
                "elements": ["showdown", "resolution", "transformation"]
            }
        }

    def format_scene_for_screenplay(self, scene: Scene) -> str:
        """
        Format scene for screenplay output

        Args:
            scene: Scene object

        Returns:
            Formatted screenplay text
        """
        lines = []

        # Scene heading
        heading = f"{scene.scene_number}. {scene.location.setting}. {scene.location.location} - {scene.location.time}"
        lines.append(heading.upper())
        lines.append("")

        # Action
        if scene.action:
            lines.append(scene.action)
            lines.append("")

        # Dialogue
        for dialogue in scene.dialogue:
            lines.append(" " * 20 + dialogue.character.upper())

            if dialogue.parenthetical:
                lines.append(" " * 15 + f"({dialogue.parenthetical})")

            # Wrap dialogue text
            dialogue_lines = self._wrap_dialogue(dialogue.line)
            for dl in dialogue_lines:
                lines.append(" " * 10 + dl)

            lines.append("")

        return "\n".join(lines)

    def _wrap_dialogue(self, text: str, max_width: int = 60) -> List[str]:
        """Wrap dialogue text to maximum width"""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0

        for word in words:
            word_length = len(word) + 1  # +1 for space

            if current_length + word_length > max_width and current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_length = len(word)
            else:
                current_line.append(word)
                current_length += word_length

        if current_line:
            lines.append(" ".join(current_line))

        return lines
