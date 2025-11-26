"""
Moment Detector Module
Identifies key moments in screenplay for storyboard frames
"""

from typing import List, Dict, Any
import re


class KeyMomentDetector:
    """
    Detects visually important moments in screenplay
    """

    def __init__(self, llm_client=None):
        """
        Initialize moment detector

        Args:
            llm_client: Optional LLM client for analysis
        """
        self.llm_client = llm_client
        self.visual_keywords = self._load_visual_keywords()

    def identify_key_moments(
        self,
        screenplay_text: str,
        num_frames: int = 8
    ) -> List[Dict[str, Any]]:
        """
        Identify key moments for storyboard frames

        Args:
            screenplay_text: Full screenplay text
            num_frames: Number of frames to identify

        Returns:
            List of moment descriptions
        """
        # Parse screenplay into scenes
        scenes = self._parse_scenes(screenplay_text)

        # Score each scene for visual importance
        scored_scenes = self._score_scenes(scenes)

        # Select top scenes
        selected_scenes = sorted(scored_scenes, key=lambda x: x["score"], reverse=True)[:num_frames]

        # Sort by scene number to maintain narrative order
        selected_scenes = sorted(selected_scenes, key=lambda x: x["scene_number"])

        # Create moment descriptions
        moments = []
        for idx, scene_data in enumerate(selected_scenes):
            moment = {
                "frame_number": idx + 1,
                "scene_number": scene_data["scene_number"],
                "description": scene_data["description"],
                "emotional_tone": scene_data["tone"],
                "characters": scene_data.get("characters", []),
                "setting": scene_data.get("setting", ""),
                "importance": scene_data["score"]
            }
            moments.append(moment)

        return moments

    def _parse_scenes(self, screenplay_text: str) -> List[Dict[str, Any]]:
        """
        Parse screenplay into individual scenes

        Args:
            screenplay_text: Full screenplay

        Returns:
            List of scene data
        """
        scenes = []

        # Split by scene headings
        scene_pattern = r'(\d+\.?\s*(?:INT|EXT|INT/EXT)\.?\s+.+?\s+-\s+(?:DAY|NIGHT|DAWN|DUSK|CONTINUOUS))'
        parts = re.split(scene_pattern, screenplay_text, flags=re.IGNORECASE)

        scene_number = 1
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                heading = parts[i]
                content = parts[i + 1]

                scene_data = {
                    "scene_number": scene_number,
                    "heading": heading,
                    "content": content,
                    "description": self._extract_description(content),
                    "tone": self._infer_tone(content),
                    "characters": self._extract_characters(content),
                    "setting": self._extract_setting(heading),
                    "score": 0.0
                }

                scenes.append(scene_data)
                scene_number += 1

        return scenes

    def _score_scenes(self, scenes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Score scenes based on visual importance

        Args:
            scenes: List of scene data

        Returns:
            Scenes with scores
        """
        for scene in scenes:
            score = 0.0

            content = scene["content"].lower()
            description = scene["description"].lower()

            # Visual action keywords (higher weight)
            for keyword, weight in self.visual_keywords["action"].items():
                if keyword in content:
                    score += weight

            # Emotional keywords (medium weight)
            for keyword, weight in self.visual_keywords["emotional"].items():
                if keyword in content:
                    score += weight * 0.7

            # Character interaction (medium weight)
            num_characters = len(scene["characters"])
            if num_characters >= 2:
                score += 1.5

            # Scene position (opening and ending are important)
            total_scenes = len(scenes)
            scene_num = scene["scene_number"]
            if scene_num == 1:
                score += 2.0  # Opening scene
            elif scene_num == total_scenes:
                score += 2.5  # Climax/ending
            elif scene_num <= total_scenes * 0.25:
                score += 1.0  # Act 1
            elif scene_num >= total_scenes * 0.75:
                score += 1.5  # Act 3

            # Length (longer scenes might be more important)
            content_length = len(content)
            if content_length > 500:
                score += 1.0

            scene["score"] = score

        return scenes

    def _extract_description(self, content: str) -> str:
        """Extract main action description from scene content"""
        # Get first action line (before dialogue)
        lines = content.strip().split('\n')

        action_lines = []
        for line in lines:
            stripped = line.strip()

            # Skip empty lines
            if not stripped:
                continue

            # Stop at character name (all caps)
            if stripped.isupper() and len(stripped.split()) <= 3:
                break

            # Add action line
            action_lines.append(stripped)

            # Limit to first few lines
            if len(action_lines) >= 3:
                break

        description = ' '.join(action_lines)

        # Truncate if too long
        if len(description) > 200:
            description = description[:197] + "..."

        return description or "Scene action"

    def _infer_tone(self, content: str) -> str:
        """Infer emotional tone from scene content"""
        content_lower = content.lower()

        tone_keywords = {
            "tense": ["danger", "threat", "chase", "fight", "urgent", "panic"],
            "dramatic": ["confrontation", "revelation", "tears", "shout", "argument"],
            "mysterious": ["shadow", "dark", "hidden", "secret", "whisper"],
            "romantic": ["kiss", "embrace", "love", "tender", "gentle"],
            "action": ["explosion", "crash", "run", "leap", "strike"],
            "peaceful": ["calm", "quiet", "serene", "gentle", "soft"]
        }

        scores = {tone: 0 for tone in tone_keywords}

        for tone, keywords in tone_keywords.items():
            for keyword in keywords:
                if keyword in content_lower:
                    scores[tone] += 1

        # Return tone with highest score
        max_tone = max(scores, key=scores.get)
        return max_tone if scores[max_tone] > 0 else "dramatic"

    def _extract_characters(self, content: str) -> List[str]:
        """Extract character names from scene"""
        characters = []
        lines = content.split('\n')

        for line in lines:
            stripped = line.strip()

            # Character names are all caps and short
            if stripped.isupper() and 2 <= len(stripped) <= 30 and len(stripped.split()) <= 3:
                # Exclude common all-caps words
                if stripped not in ["INT", "EXT", "DAY", "NIGHT", "CONTINUOUS", "CUT TO", "FADE IN"]:
                    if stripped not in characters:
                        characters.append(stripped)

        return characters

    def _extract_setting(self, heading: str) -> str:
        """Extract setting from scene heading"""
        # Remove scene number and INT/EXT prefix
        match = re.search(r'(?:INT|EXT|INT/EXT)\.?\s+(.+?)\s+-\s+(?:DAY|NIGHT|DAWN|DUSK|CONTINUOUS)', heading, re.IGNORECASE)

        if match:
            return match.group(1).strip()

        return "LOCATION"

    def _load_visual_keywords(self) -> Dict[str, Dict[str, float]]:
        """Load visual importance keywords with weights"""
        return {
            "action": {
                "fight": 3.0,
                "chase": 2.5,
                "explosion": 2.5,
                "crash": 2.0,
                "runs": 1.5,
                "enters": 1.0,
                "reveals": 2.0,
                "discovers": 2.0,
                "opens": 1.5,
                "looks": 1.0,
                "watches": 1.0,
                "fire": 2.0,
                "blood": 2.0,
                "kiss": 2.0
            },
            "emotional": {
                "tears": 1.5,
                "screams": 1.5,
                "laughs": 1.0,
                "cries": 1.5,
                "shouts": 1.0,
                "whispers": 1.0,
                "smiles": 0.5,
                "frowns": 0.5
            },
            "cinematic": {
                "darkness": 1.0,
                "light": 1.0,
                "shadow": 1.5,
                "rain": 1.0,
                "storm": 1.5,
                "sunset": 1.0,
                "dawn": 1.0
            }
        }

    def suggest_camera_angles(self, moment: Dict[str, Any]) -> str:
        """
        Suggest appropriate camera angle for moment

        Args:
            moment: Moment description

        Returns:
            Suggested camera angle
        """
        tone = moment.get("emotional_tone", "dramatic")
        num_characters = len(moment.get("characters", []))
        description = moment.get("description", "").lower()

        # Action scenes - wide shots
        if any(word in description for word in ["fight", "chase", "runs", "explosion"]):
            return "Wide Shot"

        # Emotional moments - close-ups
        if any(word in description for word in ["tears", "whispers", "kiss", "cries"]):
            return "Close-Up"

        # Discovery/revelation - medium shot
        if any(word in description for word in ["discovers", "reveals", "realizes"]):
            return "Medium Shot"

        # Multiple characters - over shoulder or medium
        if num_characters >= 2:
            return "Medium Shot" if num_characters > 2 else "Over the Shoulder"

        # Default
        return "Medium Shot"
