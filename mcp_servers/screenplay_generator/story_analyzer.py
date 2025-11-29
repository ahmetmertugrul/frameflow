"""
Story Analyzer Module
Analyzes story prompts and extracts narrative elements
"""

from typing import Dict, List, Any, Optional
import json
import re

from core.schemas import StoryInput, StoryAnalysis
from core.prompts import create_story_analysis_prompt, SYSTEM_PROMPT_CREATIVE


class StoryStructureAnalyzer:
    """
    Analyzes story structure and extracts key narrative elements
    """

    def __init__(self, llm_client=None):
        """
        Initialize story analyzer

        Args:
            llm_client: LLM client for generating analysis
        """
        self.llm_client = llm_client
        self.act_structures = {
            "Three-Act": self._three_act_structure,
            "Five-Act": self._five_act_structure,
            "Hero's Journey": self._heros_journey_structure
        }

    async def analyze(self, story_input: StoryInput) -> Dict[str, Any]:
        """
        Analyze story and extract narrative elements

        Args:
            story_input: Story input with prompt and preferences

        Returns:
            Dictionary with story analysis
        """
        # Create analysis prompt
        prompt = create_story_analysis_prompt(
            prompt=story_input.prompt,
            genre=story_input.genre,
            act_structure=story_input.act_structure
        )

        # Generate analysis using LLM
        if self.llm_client:
            analysis_text = await self.llm_client.generate(
                prompt=prompt,
                system_prompt=SYSTEM_PROMPT_CREATIVE,
                temperature=0.7,
                max_tokens=2000
            )

            # Parse the analysis
            analysis = self._parse_analysis(analysis_text)
        else:
            # Fallback: basic analysis without LLM
            analysis = self._basic_analysis(story_input)

        # Add structure-specific plot points
        structure_fn = self.act_structures.get(
            story_input.act_structure,
            self._three_act_structure
        )
        analysis["suggested_acts"] = structure_fn()
        analysis["genre"] = story_input.genre
        analysis["dialogue_style"] = story_input.dialogue_style

        # Generate logline
        analysis["logline"] = self._generate_logline(analysis, story_input)

        return analysis

    def _parse_analysis(self, analysis_text: str) -> Dict[str, Any]:
        """
        Parse LLM-generated analysis into structured format

        Args:
            analysis_text: Raw analysis text from LLM

        Returns:
            Structured analysis dictionary
        """
        analysis = {
            "main_theme": "",
            "conflict": "",
            "protagonist": "",
            "antagonist": "",
            "setting": "",
            "key_plot_points": [],
            "tone": "dramatic",
            "pacing": "moderate"
        }

        # Extract main theme
        theme_match = re.search(r"(?:Main Theme|Theme):\s*(.+?)(?:\n|$)", analysis_text, re.IGNORECASE)
        if theme_match:
            analysis["main_theme"] = theme_match.group(1).strip()

        # Extract conflict
        conflict_match = re.search(r"(?:Conflict|Central Conflict):\s*(.+?)(?:\n|$)", analysis_text, re.IGNORECASE)
        if conflict_match:
            analysis["conflict"] = conflict_match.group(1).strip()

        # Extract protagonist
        protag_match = re.search(r"Protagonist:\s*(.+?)(?:\n|$)", analysis_text, re.IGNORECASE)
        if protag_match:
            analysis["protagonist"] = protag_match.group(1).strip()

        # Extract antagonist
        antag_match = re.search(r"Antagonist:\s*(.+?)(?:\n|$)", analysis_text, re.IGNORECASE)
        if antag_match:
            analysis["antagonist"] = antag_match.group(1).strip()

        # Extract setting
        setting_match = re.search(r"Setting:\s*(.+?)(?:\n|$)", analysis_text, re.IGNORECASE)
        if setting_match:
            analysis["setting"] = setting_match.group(1).strip()

        # Extract plot points (look for numbered lists or bullet points)
        plot_points = re.findall(r"(?:^\d+\.|^[-*])\s*(.+?)(?:\n|$)", analysis_text, re.MULTILINE)
        if plot_points:
            analysis["key_plot_points"] = [point.strip() for point in plot_points]

        return analysis

    def _basic_analysis(self, story_input: StoryInput) -> Dict[str, Any]:
        """
        Perform basic analysis without LLM (fallback)

        Args:
            story_input: Story input

        Returns:
            Basic analysis dictionary
        """
        prompt = story_input.prompt.lower()

        # Simple keyword detection
        protagonist_keywords = ["detective", "hero", "protagonist", "character", "person", "woman", "man"]
        protagonist = "Main Character"
        for keyword in protagonist_keywords:
            if keyword in prompt:
                protagonist = keyword.capitalize()
                break

        return {
            "main_theme": "Personal journey and transformation",
            "conflict": "Internal and external challenges",
            "protagonist": protagonist,
            "antagonist": "Forces of opposition",
            "setting": self._infer_setting(story_input.genre),
            "key_plot_points": self._generate_basic_plot_points(story_input.act_structure),
            "tone": self._infer_tone(story_input.genre),
            "pacing": "moderate"
        }

    def _infer_setting(self, genre: str) -> str:
        """Infer setting based on genre"""
        genre_settings = {
            "Thriller": "Contemporary urban environment",
            "Sci-Fi": "Futuristic or alternate reality setting",
            "Horror": "Isolated or eerie location",
            "Romance": "Intimate contemporary setting",
            "Action": "Dynamic, multiple locations",
            "Mystery": "Atmospheric location with secrets",
            "Comedy": "Everyday relatable setting",
            "Drama": "Realistic contemporary setting"
        }
        return genre_settings.get(genre, "Contemporary setting")

    def _infer_tone(self, genre: str) -> str:
        """Infer tone based on genre"""
        genre_tones = {
            "Thriller": "tense",
            "Sci-Fi": "contemplative",
            "Horror": "dark",
            "Romance": "emotional",
            "Action": "intense",
            "Mystery": "mysterious",
            "Comedy": "lighthearted",
            "Drama": "dramatic"
        }
        return genre_tones.get(genre, "dramatic")

    def _three_act_structure(self) -> List[str]:
        """Three-act structure beats"""
        return [
            "Act 1: Setup - Introduce protagonist, world, and conflict",
            "Act 2: Confrontation - Escalate conflict, protagonist faces obstacles",
            "Act 3: Resolution - Climax and resolution of conflict"
        ]

    def _five_act_structure(self) -> List[str]:
        """Five-act structure beats"""
        return [
            "Act 1: Exposition - Introduce characters and setting",
            "Act 2: Rising Action - Conflict emerges and develops",
            "Act 3: Climax - Peak of dramatic tension",
            "Act 4: Falling Action - Consequences unfold",
            "Act 5: Denouement - Resolution and conclusion"
        ]

    def _heros_journey_structure(self) -> List[str]:
        """Hero's Journey structure beats"""
        return [
            "Ordinary World - Establish protagonist's normal life",
            "Call to Adventure - Inciting incident",
            "Refusal of the Call - Initial resistance",
            "Meeting the Mentor - Guidance received",
            "Crossing the Threshold - Commit to journey",
            "Tests, Allies, Enemies - Face challenges",
            "Approach to Inmost Cave - Prepare for ordeal",
            "Ordeal - Face greatest fear",
            "Reward - Gain something from ordeal",
            "The Road Back - Return journey begins",
            "Resurrection - Final test",
            "Return with Elixir - Transformed return"
        ]

    def _generate_basic_plot_points(self, act_structure: str) -> List[str]:
        """Generate basic plot points based on structure"""
        if act_structure == "Three-Act":
            return [
                "Opening - Introduce protagonist and world",
                "Inciting Incident - Event that starts the story",
                "First Plot Point - Protagonist commits to journey",
                "Midpoint - Major revelation or reversal",
                "Low Point - All seems lost",
                "Climax - Final confrontation",
                "Resolution - Tie up loose ends"
            ]
        elif act_structure == "Five-Act":
            return [
                "Exposition - Setup",
                "Complication - Conflict emerges",
                "Climax - Peak tension",
                "Reversal - Consequences",
                "Denouement - Resolution"
            ]
        else:  # Hero's Journey
            return [
                "Call to Adventure",
                "Crossing Threshold",
                "Tests and Trials",
                "Ordeal",
                "Return Transformed"
            ]

    def _generate_logline(self, analysis: Dict[str, Any], story_input: StoryInput) -> str:
        """
        Generate a logline for the story

        Args:
            analysis: Story analysis
            story_input: Original story input

        Returns:
            Logline string
        """
        protagonist = analysis.get("protagonist", "A character")
        conflict = analysis.get("conflict", "faces challenges")
        theme = analysis.get("main_theme", "transformation")

        # Simple template-based logline
        logline = f"{protagonist} must overcome {conflict} in a story about {theme}."

        return logline

    def identify_key_scenes(
        self,
        analysis: Dict[str, Any],
        num_scenes: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Identify key scenes based on story analysis

        Args:
            analysis: Story analysis
            num_scenes: Number of scenes to identify

        Returns:
            List of scene outlines
        """
        scenes = []
        act_structure = analysis.get("suggested_acts", self._three_act_structure())
        plot_points = analysis.get("key_plot_points", [])

        # Distribute scenes across acts
        scenes_per_act = num_scenes // len(act_structure)

        scene_number = 1
        for act_idx, act in enumerate(act_structure):
            act_name = f"Act {act_idx + 1}"

            for i in range(scenes_per_act):
                # Get corresponding plot point if available
                plot_point_idx = act_idx * scenes_per_act + i
                purpose = plot_points[plot_point_idx] if plot_point_idx < len(plot_points) else f"Develop {act_name}"

                scene = {
                    "scene_number": scene_number,
                    "act": act_name,
                    "purpose": purpose,
                    "setting": analysis.get("setting", "Location"),
                    "tone": analysis.get("tone", "dramatic")
                }

                scenes.append(scene)
                scene_number += 1

        return scenes[:num_scenes]

    def suggest_opening_scene(self, analysis: Dict[str, Any]) -> Dict[str, str]:
        """
        Suggest opening scene based on analysis

        Args:
            analysis: Story analysis

        Returns:
            Opening scene suggestion
        """
        return {
            "location": "INT. " + analysis.get("setting", "LOCATION").upper(),
            "time": "DAY",
            "purpose": "Introduce protagonist and establish normal world",
            "tone": analysis.get("tone", "dramatic"),
            "key_elements": [
                f"Introduce {analysis.get('protagonist', 'protagonist')}",
                "Establish setting and atmosphere",
                "Hint at conflict to come"
            ]
        }
