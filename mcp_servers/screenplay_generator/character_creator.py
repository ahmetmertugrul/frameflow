"""
Character Creator Module
Creates detailed character profiles for screenplays
"""

from typing import List, Dict, Any, Optional
import re
import random

from core.schemas import CharacterProfile
from core.prompts import create_character_prompt, SYSTEM_PROMPT_CREATIVE


class CharacterProfileCreator:
    """
    Creates detailed character profiles based on story analysis
    """

    def __init__(self, llm_client=None):
        """
        Initialize character creator

        Args:
            llm_client: LLM client for generating character profiles
        """
        self.llm_client = llm_client
        self.character_archetypes = self._load_archetypes()
        self.personality_traits = self._load_personality_traits()
        self.visual_features = self._load_visual_features()

    async def create_characters(
        self,
        story_analysis: Dict[str, Any],
        genre: str,
        num_characters: int = 3
    ) -> List[CharacterProfile]:
        """
        Create character profiles based on story analysis

        Args:
            story_analysis: Analyzed story elements
            genre: Story genre
            num_characters: Number of characters to create

        Returns:
            List of CharacterProfile objects
        """
        characters = []

        if self.llm_client:
            # Use LLM to generate characters
            characters = await self._generate_with_llm(
                story_analysis,
                genre,
                num_characters
            )
        else:
            # Fallback: generate basic characters
            characters = self._generate_basic_characters(
                story_analysis,
                genre,
                num_characters
            )

        return characters

    async def _generate_with_llm(
        self,
        story_analysis: Dict[str, Any],
        genre: str,
        num_characters: int
    ) -> List[CharacterProfile]:
        """
        Generate characters using LLM

        Args:
            story_analysis: Story analysis
            genre: Genre
            num_characters: Number of characters

        Returns:
            List of character profiles
        """
        # Convert story analysis to JSON string
        import json
        analysis_str = json.dumps(story_analysis, indent=2)

        # Create character generation prompt
        prompt = create_character_prompt(analysis_str, genre)
        prompt += f"\n\nCreate exactly {num_characters} main characters."

        # Generate characters
        response = await self.llm_client.generate(
            prompt=prompt,
            system_prompt=SYSTEM_PROMPT_CREATIVE,
            temperature=0.8,
            max_tokens=2500
        )

        # Parse the response into character profiles
        characters = self._parse_character_response(response, story_analysis)

        return characters

    def _parse_character_response(
        self,
        response: str,
        story_analysis: Dict[str, Any]
    ) -> List[CharacterProfile]:
        """
        Parse LLM response into CharacterProfile objects

        Args:
            response: LLM-generated character descriptions
            story_analysis: Original story analysis

        Returns:
            List of CharacterProfile objects
        """
        characters = []

        # Split response into individual characters
        # Look for numbered sections or character names
        char_sections = re.split(r'\n\s*(?:\d+\.|Character \d+|#{1,3})\s*', response)

        for section in char_sections:
            if len(section.strip()) < 50:  # Skip very short sections
                continue

            char_data = self._extract_character_data(section)

            if char_data.get("name"):
                # Create CharacterProfile
                character = CharacterProfile(
                    name=char_data.get("name", "Unknown"),
                    age=char_data.get("age"),
                    role=char_data.get("role", "supporting"),
                    description=char_data.get("description", ""),
                    personality_traits=char_data.get("personality_traits", []),
                    visual_description=char_data.get("visual_description", ""),
                    motivation=char_data.get("motivation"),
                    arc=char_data.get("arc")
                )

                characters.append(character)

        return characters

    def _extract_character_data(self, text: str) -> Dict[str, Any]:
        """
        Extract character data from text section

        Args:
            text: Text containing character information

        Returns:
            Dictionary with character data
        """
        data = {}

        # Extract name
        name_match = re.search(r"(?:Name|Character):\s*(.+?)(?:\n|,)", text, re.IGNORECASE)
        if name_match:
            data["name"] = name_match.group(1).strip()

        # Extract age
        age_match = re.search(r"Age:\s*(\d+)", text, re.IGNORECASE)
        if age_match:
            data["age"] = int(age_match.group(1))

        # Extract role
        role_match = re.search(r"Role:\s*(protagonist|antagonist|supporting)", text, re.IGNORECASE)
        if role_match:
            data["role"] = role_match.group(1).lower()

        # Extract description
        desc_match = re.search(r"Description:\s*(.+?)(?:\n\n|Personality|Visual)", text, re.IGNORECASE | re.DOTALL)
        if desc_match:
            data["description"] = desc_match.group(1).strip()

        # Extract personality traits
        traits_match = re.search(r"Personality Traits?:\s*(.+?)(?:\n\n|Visual|Motivation)", text, re.IGNORECASE | re.DOTALL)
        if traits_match:
            traits_text = traits_match.group(1)
            # Extract traits from comma-separated or bullet list
            traits = re.findall(r"(?:[-*•]\s*)?(\w+(?:\s+\w+)?)", traits_text)
            data["personality_traits"] = [t.strip() for t in traits if len(t.strip()) > 2][:5]

        # Extract visual description
        visual_match = re.search(r"Visual Description:\s*(.+?)(?:\n\n|Motivation|Arc)", text, re.IGNORECASE | re.DOTALL)
        if visual_match:
            data["visual_description"] = visual_match.group(1).strip()

        # Extract motivation
        motivation_match = re.search(r"Motivation:\s*(.+?)(?:\n\n|Arc|$)", text, re.IGNORECASE | re.DOTALL)
        if motivation_match:
            data["motivation"] = motivation_match.group(1).strip()

        # Extract character arc
        arc_match = re.search(r"(?:Character )?Arc:\s*(.+?)(?:\n\n|$)", text, re.IGNORECASE | re.DOTALL)
        if arc_match:
            data["arc"] = arc_match.group(1).strip()

        return data

    def _generate_basic_characters(
        self,
        story_analysis: Dict[str, Any],
        genre: str,
        num_characters: int
    ) -> List[CharacterProfile]:
        """
        Generate basic characters without LLM (fallback)

        Args:
            story_analysis: Story analysis
            genre: Genre
            num_characters: Number of characters

        Returns:
            List of character profiles
        """
        characters = []

        # Protagonist
        protagonist_name = story_analysis.get("protagonist", "Alex Morgan")
        if not any(c.isalpha() for c in protagonist_name.split()[0] if len(protagonist_name.split()) > 0):
            protagonist_name = "Alex Morgan"

        protagonist = CharacterProfile(
            name=protagonist_name.title(),
            age=random.choice([28, 32, 35, 38, 42]),
            role="protagonist",
            description=f"The determined {protagonist_name.lower()} at the center of the story",
            personality_traits=self._get_genre_traits(genre, "protagonist"),
            visual_description=self._generate_visual_description(genre, "protagonist"),
            motivation=story_analysis.get("main_theme", "To overcome the challenge"),
            arc="From doubt to confidence and understanding"
        )
        characters.append(protagonist)

        # Antagonist (if mentioned)
        if story_analysis.get("antagonist") and num_characters > 1:
            antagonist = CharacterProfile(
                name=self._generate_name(genre),
                age=random.choice([35, 40, 45, 50]),
                role="antagonist",
                description="The force opposing the protagonist",
                personality_traits=self._get_genre_traits(genre, "antagonist"),
                visual_description=self._generate_visual_description(genre, "antagonist"),
                motivation="To achieve their goal at any cost",
                arc="Escalating conflict with protagonist"
            )
            characters.append(antagonist)

        # Supporting characters
        while len(characters) < num_characters:
            support_char = CharacterProfile(
                name=self._generate_name(genre),
                age=random.choice([25, 30, 35, 40]),
                role="supporting",
                description="A key supporting character in the story",
                personality_traits=self._get_genre_traits(genre, "supporting"),
                visual_description=self._generate_visual_description(genre, "supporting"),
                motivation="To help or hinder the protagonist",
                arc="Growth through the story"
            )
            characters.append(support_char)

        return characters

    def _get_genre_traits(self, genre: str, role: str) -> List[str]:
        """Get appropriate personality traits for genre and role"""
        genre_traits = {
            "Thriller": {
                "protagonist": ["determined", "intelligent", "cautious", "resourceful"],
                "antagonist": ["cunning", "ruthless", "calculating", "mysterious"],
                "supporting": ["loyal", "skeptical", "brave", "insightful"]
            },
            "Drama": {
                "protagonist": ["complex", "emotional", "conflicted", "passionate"],
                "antagonist": ["flawed", "stubborn", "proud", "defensive"],
                "supporting": ["empathetic", "wise", "patient", "understanding"]
            },
            "Comedy": {
                "protagonist": ["optimistic", "awkward", "endearing", "witty"],
                "antagonist": ["pompous", "oblivious", "competitive", "eccentric"],
                "supporting": ["quirky", "supportive", "humorous", "lovable"]
            },
            "Sci-Fi": {
                "protagonist": ["curious", "adaptable", "logical", "visionary"],
                "antagonist": ["ambitious", "cold", "technological", "powerful"],
                "supporting": ["knowledgeable", "inventive", "analytical", "cautious"]
            },
            "Horror": {
                "protagonist": ["brave", "traumatized", "protective", "desperate"],
                "antagonist": ["terrifying", "relentless", "supernatural", "evil"],
                "supporting": ["fearful", "doubtful", "vulnerable", "resilient"]
            }
        }

        return genre_traits.get(genre, {}).get(role, ["complex", "interesting", "motivated"])

    def _generate_visual_description(self, genre: str, role: str) -> str:
        """Generate visual description based on genre and role"""
        builds = ["tall", "average height", "athletic", "slender", "stocky"]
        hair_colors = ["dark hair", "blonde hair", "red hair", "gray hair", "brown hair"]
        features = ["sharp features", "kind eyes", "strong presence", "distinctive appearance"]

        build = random.choice(builds)
        hair = random.choice(hair_colors)
        feature = random.choice(features)

        style = {
            "Thriller": "professional attire, often a leather jacket",
            "Drama": "casual but thoughtful clothing",
            "Comedy": "colorful, expressive wardrobe",
            "Sci-Fi": "practical, futuristic clothing",
            "Horror": "practical, worn clothing"
        }.get(genre, "contemporary clothing")

        return f"{build.capitalize()}, {hair}, {feature}, typically wears {style}"

    def _generate_name(self, genre: str) -> str:
        """Generate appropriate name for genre"""
        first_names = ["Alex", "Jordan", "Morgan", "Casey", "Riley", "Taylor", "Sam", "Jamie"]
        last_names = ["Chen", "Garcia", "Smith", "Johnson", "Williams", "Martinez", "Davis", "Rodriguez"]

        return f"{random.choice(first_names)} {random.choice(last_names)}"

    def _load_archetypes(self) -> Dict[str, Dict]:
        """Load character archetypes"""
        return {
            "hero": {"traits": ["brave", "determined", "moral"]},
            "mentor": {"traits": ["wise", "experienced", "patient"]},
            "ally": {"traits": ["loyal", "supportive", "skilled"]},
            "shadow": {"traits": ["dark", "conflicted", "powerful"]},
            "trickster": {"traits": ["clever", "unpredictable", "chaotic"]}
        }

    def _load_personality_traits(self) -> List[str]:
        """Load personality traits library"""
        return [
            "brave", "intelligent", "loyal", "cunning", "compassionate",
            "ambitious", "cautious", "optimistic", "cynical", "determined",
            "creative", "analytical", "empathetic", "ruthless", "patient",
            "impulsive", "methodical", "charismatic", "reserved", "passionate"
        ]

    def _load_visual_features(self) -> Dict[str, List[str]]:
        """Load visual features library"""
        return {
            "build": ["tall", "short", "athletic", "slender", "stocky", "average"],
            "hair": ["short dark hair", "long blonde hair", "curly red hair", "gray hair"],
            "eyes": ["piercing blue eyes", "warm brown eyes", "sharp green eyes"],
            "style": ["professional", "casual", "edgy", "elegant", "practical"]
        }

    def enhance_character_consistency(
        self,
        character: CharacterProfile,
        embedding_manager=None
    ) -> CharacterProfile:
        """
        Enhance character with consistency features

        Args:
            character: Character profile
            embedding_manager: Optional character consistency manager

        Returns:
            Enhanced character profile
        """
        if embedding_manager:
            # Store character embedding for consistency
            import asyncio
            embedding_id = asyncio.run(
                embedding_manager.store_character(
                    character_name=character.name,
                    visual_description=character.visual_description,
                    metadata={
                        "age": character.age,
                        "role": character.role
                    }
                )
            )
            character.embedding_id = embedding_id

        return character
