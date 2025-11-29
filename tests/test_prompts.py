"""
Tests for core/prompts.py
Validate prompt template generation and formatting
"""

import pytest

from core.prompts import (
    format_prompt,
    create_story_analysis_prompt,
    create_character_prompt,
    create_scene_prompt,
    create_visual_prompt,
    STORY_ANALYSIS_PROMPT,
    CHARACTER_CREATION_PROMPT,
    SCENE_WRITING_PROMPT,
    VISUAL_PROMPT_GENERATION,
    DIALOGUE_GENERATION_PROMPT,
    SYSTEM_PROMPT_CREATIVE,
    SYSTEM_PROMPT_TECHNICAL
)


class TestFormatPrompt:
    """Test format_prompt utility function"""

    def test_basic_formatting(self):
        """Test basic template formatting"""
        template = "Hello {name}, welcome to {place}!"
        result = format_prompt(template, name="Alice", place="Wonderland")

        assert result == "Hello Alice, welcome to Wonderland!"

    def test_missing_argument_raises_error(self):
        """Test that missing arguments raise ValueError"""
        template = "Hello {name}!"

        with pytest.raises(ValueError) as exc_info:
            format_prompt(template)

        assert "Missing required prompt argument" in str(exc_info.value)

    def test_extra_arguments_ignored(self):
        """Test that extra arguments are ignored"""
        template = "Hello {name}!"
        result = format_prompt(template, name="Bob", extra="ignored")

        assert result == "Hello Bob!"

    def test_multiline_template(self):
        """Test formatting multiline templates"""
        template = """
        Name: {name}
        Age: {age}
        Role: {role}
        """
        result = format_prompt(template, name="Alice", age=30, role="Detective")

        assert "Name: Alice" in result
        assert "Age: 30" in result
        assert "Role: Detective" in result


class TestStoryAnalysisPrompt:
    """Test story analysis prompt creation"""

    def test_create_story_analysis_prompt(self):
        """Test creating story analysis prompt"""
        prompt = create_story_analysis_prompt(
            prompt="A detective story",
            genre="Thriller",
            act_structure="Three-Act"
        )

        assert "A detective story" in prompt
        assert "Thriller" in prompt
        assert "Three-Act" in prompt
        assert "Main Theme" in prompt
        assert "Conflict" in prompt
        assert "Protagonist" in prompt

    def test_story_analysis_includes_all_elements(self):
        """Test that prompt includes all required elements"""
        prompt = create_story_analysis_prompt(
            prompt="A sci-fi adventure",
            genre="Sci-Fi",
            act_structure="Hero's Journey"
        )

        required_elements = [
            "Main Theme",
            "Conflict",
            "Protagonist",
            "Antagonist",
            "Setting",
            "Key Plot Points",
            "Suggested Acts"
        ]

        for element in required_elements:
            assert element in prompt

    def test_different_genres(self):
        """Test with different genres"""
        genres = ["Drama", "Comedy", "Horror", "Romance"]

        for genre in genres:
            prompt = create_story_analysis_prompt(
                prompt="Test story",
                genre=genre,
                act_structure="Three-Act"
            )
            assert genre in prompt


class TestCharacterPrompt:
    """Test character creation prompt"""

    def test_create_character_prompt(self):
        """Test creating character prompt"""
        story_analysis = '{"theme": "redemption", "protagonist": "detective"}'
        prompt = create_character_prompt(
            story_analysis=story_analysis,
            genre="Thriller"
        )

        assert story_analysis in prompt
        assert "Thriller" in prompt
        assert "character" in prompt.lower()
        assert "visual description" in prompt.lower()

    def test_character_prompt_includes_required_fields(self):
        """Test that prompt requests all required character fields"""
        prompt = create_character_prompt(
            story_analysis="Test analysis",
            genre="Drama"
        )

        required_fields = [
            "Name",
            "Age",
            "Role",
            "Description",
            "Personality Traits",
            "Visual Description",
            "Motivation",
            "Character Arc"
        ]

        for field in required_fields:
            assert field in prompt


class TestScenePrompt:
    """Test scene writing prompt"""

    def test_create_scene_prompt(self):
        """Test creating scene prompt"""
        prompt = create_scene_prompt(
            scene_number=1,
            act="Act 1",
            location="INT. OFFICE",
            time="DAY",
            purpose="Introduce protagonist",
            characters='[{"name": "Alex"}]',
            context="Opening scene",
            dialogue_style="Realistic",
            genre="Drama"
        )

        assert "1" in prompt or "Scene 1" in prompt
        assert "Act 1" in prompt
        assert "INT. OFFICE" in prompt
        assert "DAY" in prompt
        assert "Realistic" in prompt
        assert "Drama" in prompt

    def test_scene_prompt_formatting_instructions(self):
        """Test that prompt includes formatting instructions"""
        prompt = create_scene_prompt(
            scene_number=5,
            act="Act 2",
            location="EXT. STREET",
            time="NIGHT",
            purpose="Chase scene",
            characters='[]',
            context="Test",
            dialogue_style="Witty",
            genre="Action"
        )

        assert "INT/EXT" in prompt or "scene heading" in prompt.lower()
        assert "dialogue" in prompt.lower()
        assert "action" in prompt.lower()


class TestVisualPrompt:
    """Test visual prompt generation"""

    def test_create_visual_prompt(self):
        """Test creating visual prompt for image generation"""
        prompt = create_visual_prompt(
            scene_description="Detective at desk",
            characters="Alex Morgan - tall, dark hair",
            camera_angle="Medium Shot",
            visual_style="Noir",
            mood="Mysterious"
        )

        assert "Detective at desk" in prompt
        assert "Alex Morgan" in prompt
        assert "Medium Shot" in prompt
        assert "Noir" in prompt
        assert "Mysterious" in prompt

    def test_visual_prompt_includes_image_elements(self):
        """Test that visual prompt includes key image generation elements"""
        prompt = create_visual_prompt(
            scene_description="Test scene",
            characters="Test character",
            camera_angle="Wide Shot",
            visual_style="Realistic",
            mood="Dramatic"
        )

        image_elements = [
            "Subject" or "subject",
            "Character" or "character",
            "Setting" or "setting",
            "Lighting" or "lighting",
            "Camera" or "camera",
            "Composition" or "composition"
        ]

        # At least some of these should be present
        found = sum(1 for elem in image_elements if elem.lower() in prompt.lower())
        assert found >= 3

    def test_visual_styles(self):
        """Test different visual styles"""
        styles = ["Realistic", "Noir", "Anime", "Illustrated"]

        for style in styles:
            prompt = create_visual_prompt(
                scene_description="Test",
                characters="Test",
                camera_angle="Close-Up",
                visual_style=style,
                mood="Test"
            )
            assert style in prompt


class TestSystemPrompts:
    """Test system prompts"""

    def test_creative_system_prompt(self):
        """Test creative system prompt"""
        assert len(SYSTEM_PROMPT_CREATIVE) > 0
        assert "screenplay" in SYSTEM_PROMPT_CREATIVE.lower()
        assert "FrameFlow" in SYSTEM_PROMPT_CREATIVE

    def test_technical_system_prompt(self):
        """Test technical system prompt"""
        assert len(SYSTEM_PROMPT_TECHNICAL) > 0
        assert "technical" in SYSTEM_PROMPT_TECHNICAL.lower()
        assert "FrameFlow" in SYSTEM_PROMPT_TECHNICAL


class TestPromptTemplates:
    """Test that all prompt templates are well-formed"""

    def test_story_analysis_template(self):
        """Test story analysis template structure"""
        assert "{prompt}" in STORY_ANALYSIS_PROMPT
        assert "{genre}" in STORY_ANALYSIS_PROMPT
        assert "{act_structure}" in STORY_ANALYSIS_PROMPT

    def test_character_creation_template(self):
        """Test character creation template structure"""
        assert "{story_analysis}" in CHARACTER_CREATION_PROMPT
        assert "{genre}" in CHARACTER_CREATION_PROMPT

    def test_scene_writing_template(self):
        """Test scene writing template structure"""
        required_placeholders = [
            "{scene_number}",
            "{act}",
            "{location}",
            "{time}",
            "{purpose}",
            "{characters}",
            "{context}",
            "{dialogue_style}",
            "{genre}"
        ]

        for placeholder in required_placeholders:
            assert placeholder in SCENE_WRITING_PROMPT

    def test_visual_prompt_template(self):
        """Test visual prompt template structure"""
        required_placeholders = [
            "{scene_description}",
            "{characters}",
            "{camera_angle}",
            "{visual_style}",
            "{mood}"
        ]

        for placeholder in required_placeholders:
            assert placeholder in VISUAL_PROMPT_GENERATION

    def test_dialogue_generation_template(self):
        """Test dialogue generation template structure"""
        assert "{characters}" in DIALOGUE_GENERATION_PROMPT
        assert "{context}" in DIALOGUE_GENERATION_PROMPT
        assert "{dialogue_style}" in DIALOGUE_GENERATION_PROMPT
        assert "{genre}" in DIALOGUE_GENERATION_PROMPT
        assert "{tone}" in DIALOGUE_GENERATION_PROMPT


class TestPromptQuality:
    """Test prompt quality and completeness"""

    def test_prompts_are_not_empty(self):
        """Test that all prompts have substantial content"""
        prompts = [
            STORY_ANALYSIS_PROMPT,
            CHARACTER_CREATION_PROMPT,
            SCENE_WRITING_PROMPT,
            VISUAL_PROMPT_GENERATION,
            DIALOGUE_GENERATION_PROMPT
        ]

        for prompt in prompts:
            assert len(prompt) > 100, "Prompt should have substantial content"

    def test_prompts_have_instructions(self):
        """Test that prompts contain clear instructions"""
        prompts = [
            STORY_ANALYSIS_PROMPT,
            CHARACTER_CREATION_PROMPT,
            SCENE_WRITING_PROMPT
        ]

        for prompt in prompts:
            # Check for instruction indicators
            has_instructions = (
                "provide" in prompt.lower() or
                "create" in prompt.lower() or
                "generate" in prompt.lower() or
                "write" in prompt.lower()
            )
            assert has_instructions, "Prompt should contain clear instructions"

    def test_prompts_avoid_ambiguity(self):
        """Test that prompts are specific"""
        # Story analysis should ask for specific elements
        assert "main theme" in STORY_ANALYSIS_PROMPT.lower()
        assert "conflict" in STORY_ANALYSIS_PROMPT.lower()

        # Character creation should specify what to include
        assert "personality" in CHARACTER_CREATION_PROMPT.lower()
        assert "visual" in CHARACTER_CREATION_PROMPT.lower()


class TestEdgeCases:
    """Test edge cases in prompt generation"""

    def test_empty_string_values(self):
        """Test handling of empty string values"""
        prompt = create_visual_prompt(
            scene_description="",
            characters="",
            camera_angle="Close-Up",
            visual_style="Realistic",
            mood=""
        )

        # Should still generate a prompt
        assert len(prompt) > 0
        assert "Close-Up" in prompt

    def test_special_characters_in_prompt(self):
        """Test handling of special characters"""
        special_story = "A story with \"quotes\" and 'apostrophes' & symbols!"

        prompt = create_story_analysis_prompt(
            prompt=special_story,
            genre="Drama",
            act_structure="Three-Act"
        )

        assert special_story in prompt

    def test_very_long_input(self):
        """Test handling of very long inputs"""
        long_description = "A very long scene description. " * 100

        prompt = create_visual_prompt(
            scene_description=long_description,
            characters="Test",
            camera_angle="Wide Shot",
            visual_style="Realistic",
            mood="Test"
        )

        assert long_description in prompt
