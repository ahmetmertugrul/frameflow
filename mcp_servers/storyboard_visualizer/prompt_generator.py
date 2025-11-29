"""
Visual Prompt Generator Module
Generates detailed image generation prompts for storyboard frames
"""

from typing import Dict, Any, List, Optional

from core.prompts import create_visual_prompt


class VisualPromptGenerator:
    """
    Generates optimized prompts for image generation
    """

    def __init__(self, llm_client=None):
        """
        Initialize prompt generator

        Args:
            llm_client: Optional LLM client for enhanced prompts
        """
        self.llm_client = llm_client
        self.style_modifiers = self._load_style_modifiers()
        self.lighting_presets = self._load_lighting_presets()
        self.composition_rules = self._load_composition_rules()

    def generate_visual_prompt(
        self,
        moment: Dict[str, Any],
        visual_style: str = "Realistic",
        camera_angle: str = "Medium Shot",
        characters: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Generate detailed visual prompt for image generation

        Args:
            moment: Key moment description
            visual_style: Visual style (Realistic, Noir, etc.)
            camera_angle: Camera angle
            characters: Character visual descriptions

        Returns:
            Detailed image generation prompt
        """
        # Base description
        scene_description = moment.get("description", "A scene from the story")
        setting = moment.get("setting", "location")
        tone = moment.get("emotional_tone", "dramatic")

        # Character descriptions
        char_descriptions = self._format_character_descriptions(
            moment.get("characters", []),
            characters
        )

        # Get lighting and composition
        lighting = self._select_lighting(tone, visual_style)
        composition = self._select_composition(camera_angle)

        # Build comprehensive prompt
        if self.llm_client:
            # Use LLM for enhanced prompt
            prompt = create_visual_prompt(
                scene_description=scene_description,
                characters=char_descriptions,
                camera_angle=camera_angle,
                visual_style=visual_style,
                mood=tone
            )
        else:
            # Build structured prompt
            prompt = self._build_structured_prompt(
                scene_description=scene_description,
                setting=setting,
                characters=char_descriptions,
                camera_angle=camera_angle,
                visual_style=visual_style,
                tone=tone,
                lighting=lighting,
                composition=composition
            )

        return prompt

    def _build_structured_prompt(
        self,
        scene_description: str,
        setting: str,
        characters: str,
        camera_angle: str,
        visual_style: str,
        tone: str,
        lighting: str,
        composition: str
    ) -> str:
        """
        Build structured image generation prompt

        Args:
            scene_description: Main scene description
            setting: Location/setting
            characters: Character descriptions
            camera_angle: Camera angle
            visual_style: Visual style
            tone: Emotional tone
            lighting: Lighting description
            composition: Composition rules

        Returns:
            Complete prompt
        """
        prompt_parts = []

        # Style prefix
        style_mod = self.style_modifiers.get(visual_style, {})
        if style_mod.get("prefix"):
            prompt_parts.append(style_mod["prefix"])

        # Main subject and action
        prompt_parts.append(scene_description)

        # Setting
        prompt_parts.append(f"in {setting}")

        # Characters (if any)
        if characters:
            prompt_parts.append(f"featuring {characters}")

        # Camera angle
        prompt_parts.append(f"{camera_angle.lower()}")

        # Lighting
        prompt_parts.append(lighting)

        # Composition
        prompt_parts.append(composition)

        # Style-specific modifiers
        if style_mod.get("quality"):
            prompt_parts.append(style_mod["quality"])

        # Tone/mood
        mood_descriptor = self._tone_to_descriptor(tone)
        if mood_descriptor:
            prompt_parts.append(mood_descriptor)

        # Technical quality
        prompt_parts.append("highly detailed, professional quality")

        # Join parts
        prompt = ", ".join(prompt_parts)

        # Add negative prompt elements
        negative = style_mod.get("negative", "")
        if negative:
            prompt += f" | Negative: {negative}"

        return prompt

    def _format_character_descriptions(
        self,
        character_names: List[str],
        character_data: Optional[List[Dict[str, str]]]
    ) -> str:
        """
        Format character descriptions for prompt

        Args:
            character_names: List of character names
            character_data: Optional character visual data

        Returns:
            Formatted character descriptions
        """
        if not character_names:
            return ""

        descriptions = []

        if character_data:
            # Use provided character data
            for name in character_names:
                for char in character_data:
                    if char.get("name", "").upper() == name.upper():
                        desc = char.get("visual_description", name)
                        descriptions.append(desc)
                        break
                else:
                    descriptions.append(f"character {name}")
        else:
            # Generic descriptions
            descriptions = [f"character {name}" for name in character_names]

        if len(descriptions) == 1:
            return descriptions[0]
        elif len(descriptions) == 2:
            return f"{descriptions[0]} and {descriptions[1]}"
        else:
            return ", ".join(descriptions[:-1]) + f", and {descriptions[-1]}"

    def _select_lighting(self, tone: str, style: str) -> str:
        """
        Select appropriate lighting based on tone and style

        Args:
            tone: Emotional tone
            style: Visual style

        Returns:
            Lighting description
        """
        # Check for style-specific lighting
        style_lighting = self.style_modifiers.get(style, {}).get("lighting")
        if style_lighting:
            return style_lighting

        # Default lighting based on tone
        return self.lighting_presets.get(tone, "natural lighting")

    def _select_composition(self, camera_angle: str) -> str:
        """
        Select composition rules based on camera angle

        Args:
            camera_angle: Camera angle

        Returns:
            Composition description
        """
        return self.composition_rules.get(camera_angle, "balanced composition")

    def _tone_to_descriptor(self, tone: str) -> str:
        """Convert tone to visual descriptor"""
        tone_descriptors = {
            "tense": "tense atmosphere, high contrast",
            "dramatic": "dramatic mood, cinematic",
            "mysterious": "mysterious ambiance, shadows",
            "romantic": "warm and intimate atmosphere",
            "action": "dynamic energy, motion blur",
            "peaceful": "calm and serene mood",
            "dark": "dark and moody atmosphere",
            "lighthearted": "bright and cheerful mood"
        }

        return tone_descriptors.get(tone, "cinematic atmosphere")

    def _load_style_modifiers(self) -> Dict[str, Dict[str, str]]:
        """Load visual style modifiers"""
        return {
            "Realistic": {
                "prefix": "Cinematic photograph",
                "quality": "photorealistic, film still, 4k quality",
                "lighting": "natural cinematic lighting",
                "negative": "cartoon, anime, illustration, painting, drawing"
            },
            "Noir": {
                "prefix": "Film noir style",
                "quality": "black and white, high contrast, dramatic shadows",
                "lighting": "dramatic chiaroscuro lighting, venetian blind shadows",
                "negative": "color, bright, cheerful, soft lighting"
            },
            "Illustrated": {
                "prefix": "Digital illustration",
                "quality": "concept art style, detailed artwork",
                "lighting": "painterly lighting",
                "negative": "photograph, photorealistic, 3d render"
            },
            "Anime": {
                "prefix": "Anime style illustration",
                "quality": "anime art, cel-shaded, vibrant colors",
                "lighting": "anime lighting style",
                "negative": "photograph, realistic, western art style"
            },
            "Sketch": {
                "prefix": "Storyboard sketch",
                "quality": "pencil drawing, loose sketch, storyboard art",
                "lighting": "sketch shading",
                "negative": "photograph, colored, finished artwork"
            }
        }

    def _load_lighting_presets(self) -> Dict[str, str]:
        """Load lighting presets for different tones"""
        return {
            "tense": "harsh lighting, deep shadows, high contrast",
            "dramatic": "dramatic three-point lighting, rim lighting",
            "mysterious": "low-key lighting, shadows, dim ambiance",
            "romantic": "soft warm lighting, golden hour glow",
            "action": "dynamic lighting, motion-enhanced",
            "peaceful": "soft natural lighting, gentle diffusion",
            "dark": "low-key lighting, minimal fill light",
            "lighthearted": "bright even lighting, cheerful ambiance"
        }

    def _load_composition_rules(self) -> Dict[str, str]:
        """Load composition rules for camera angles"""
        return {
            "Wide Shot": "rule of thirds, environmental context, establishing shot composition",
            "Medium Shot": "centered framing, balanced composition, waist-up framing",
            "Close-Up": "tight framing, facial focus, shallow depth of field",
            "Extreme Close-Up": "extreme detail focus, macro composition",
            "POV (Point of View)": "subjective camera angle, first-person perspective",
            "Over the Shoulder": "over-shoulder framing, conversational composition",
            "Bird's Eye View": "top-down perspective, overhead angle",
            "Low Angle": "upward camera angle, dramatic power composition",
            "High Angle": "downward camera angle, vulnerable framing"
        }

    def optimize_for_model(self, prompt: str, model: str = "SDXL") -> str:
        """
        Optimize prompt for specific image generation model

        Args:
            prompt: Base prompt
            model: Image generation model (SDXL, Flux, etc.)

        Returns:
            Optimized prompt
        """
        if model == "SDXL":
            # SDXL works well with detailed, structured prompts
            # Already optimized
            return prompt

        elif model == "Flux":
            # Flux prefers natural language
            # Remove some technical terms
            prompt = prompt.replace(" | Negative:", "")
            return prompt

        elif model == "Stable Diffusion":
            # Add quality boosters
            if "masterpiece" not in prompt.lower():
                prompt = f"masterpiece, {prompt}"

        return prompt

    def add_character_consistency(
        self,
        prompt: str,
        character_embedding_desc: str
    ) -> str:
        """
        Add character consistency information to prompt

        Args:
            prompt: Base prompt
            character_embedding_desc: Consistent character description

        Returns:
            Enhanced prompt with consistency
        """
        # Replace generic character description with consistent one
        if "character" in prompt.lower():
            # Insert consistent description
            prompt = f"{character_embedding_desc}, {prompt}"

        return prompt
