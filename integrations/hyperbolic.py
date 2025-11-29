"""
Hyperbolic AI Integration
Image generation for storyboard frames using SDXL/Flux
"""

import os
import httpx
from typing import Optional, Dict, Any, List
import asyncio
import base64
from pathlib import Path


class HyperbolicClient:
    """Client for Hyperbolic AI image generation API"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Hyperbolic client

        Args:
            api_key: Hyperbolic API key (or use HYPERBOLIC_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("HYPERBOLIC_API_KEY")
        if not self.api_key:
            raise ValueError("Hyperbolic API key not provided")

        self.base_url = "https://api.hyperbolic.xyz/v1"
        self.timeout = 120.0  # Image generation can take longer

    async def generate_image(
        self,
        prompt: str,
        model: str = "SDXL1.0-base",
        negative_prompt: Optional[str] = None,
        width: int = 1024,
        height: int = 768,
        num_inference_steps: int = 30,
        guidance_scale: float = 7.5,
        seed: Optional[int] = None,
        **kwargs
    ) -> bytes:
        """
        Generate image from text prompt

        Args:
            prompt: Image generation prompt
            model: Model to use (SDXL1.0-base, FLUX.1-dev, etc.)
            negative_prompt: What to avoid in image
            width: Image width
            height: Image height
            num_inference_steps: Number of denoising steps
            guidance_scale: How closely to follow prompt (1-20)
            seed: Random seed for reproducibility
            **kwargs: Additional parameters

        Returns:
            Image bytes
        """
        payload = {
            "model_name": model,
            "prompt": prompt,
            "height": height,
            "width": width,
            "backend": "auto",
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
        }

        if negative_prompt:
            payload["negative_prompt"] = negative_prompt

        if seed is not None:
            payload["seed"] = seed

        # Add any additional parameters
        payload.update({k: v for k, v in kwargs.items()})

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/image/generation",
                json=payload,
                headers=headers
            )

            response.raise_for_status()
            result = response.json()

            # Image is typically returned as base64
            if "images" in result and len(result["images"]) > 0:
                image_b64 = result["images"][0]
                return base64.b64decode(image_b64)
            else:
                raise ValueError("No image returned from API")

    async def generate_storyboard_frame(
        self,
        prompt: str,
        style: str = "realistic",
        aspect_ratio: str = "16:9",
        quality: str = "high",
        **kwargs
    ) -> bytes:
        """
        Generate storyboard frame with optimized settings

        Args:
            prompt: Frame description
            style: Visual style (realistic, illustrated, noir, etc.)
            aspect_ratio: Aspect ratio (16:9, 4:3, etc.)
            quality: Quality level (draft, standard, high)
            **kwargs: Additional parameters

        Returns:
            Image bytes
        """
        # Map aspect ratios to dimensions
        aspect_ratios = {
            "16:9": (1024, 576),
            "4:3": (896, 672),
            "1:1": (768, 768),
            "2:3": (640, 960),
        }

        width, height = aspect_ratios.get(aspect_ratio, (1024, 576))

        # Map quality to inference steps
        quality_steps = {
            "draft": 20,
            "standard": 30,
            "high": 50
        }

        steps = quality_steps.get(quality, 30)

        # Style-specific negative prompts
        style_negatives = {
            "realistic": "cartoon, anime, illustration, painting, drawing, sketch, low quality, blurry",
            "illustrated": "photograph, photo-realistic, low quality, blurry",
            "noir": "color, bright, vibrant, low quality",
            "anime": "realistic, photograph, 3d render, low quality",
            "sketch": "photograph, color, detailed, finished, low quality"
        }

        negative_prompt = style_negatives.get(style.lower(), "low quality, blurry, distorted")

        # Add style modifier to prompt
        style_modifiers = {
            "realistic": "cinematic, film still, professional photography",
            "illustrated": "digital illustration, concept art, detailed artwork",
            "noir": "film noir, black and white, dramatic lighting, high contrast",
            "anime": "anime style, manga art, clean lines",
            "sketch": "pencil sketch, storyboard sketch, hand-drawn"
        }

        style_modifier = style_modifiers.get(style.lower(), "")
        full_prompt = f"{prompt}, {style_modifier}" if style_modifier else prompt

        return await self.generate_image(
            prompt=full_prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            num_inference_steps=steps,
            guidance_scale=7.5,
            **kwargs
        )

    async def save_image(
        self,
        image_bytes: bytes,
        output_path: str,
        format: str = "PNG"
    ) -> str:
        """
        Save image bytes to file

        Args:
            image_bytes: Image data
            output_path: Where to save
            format: Image format

        Returns:
            Path to saved file
        """
        from PIL import Image
        import io

        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_bytes))

        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # Save image
        image.save(output_path, format=format)

        return output_path

    async def batch_generate(
        self,
        prompts: List[str],
        output_dir: str,
        **kwargs
    ) -> List[str]:
        """
        Generate multiple images in parallel

        Args:
            prompts: List of prompts
            output_dir: Directory to save images
            **kwargs: Additional parameters

        Returns:
            List of saved file paths
        """
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        async def generate_and_save(idx: int, prompt: str):
            image_bytes = await self.generate_storyboard_frame(prompt, **kwargs)
            output_path = os.path.join(output_dir, f"frame_{idx+1:03d}.png")
            return await self.save_image(image_bytes, output_path)

        tasks = [
            generate_and_save(i, prompt)
            for i, prompt in enumerate(prompts)
        ]

        return await asyncio.gather(*tasks)

    def get_available_models(self) -> List[str]:
        """
        Get list of available models

        Returns:
            List of model names
        """
        return [
            "SDXL1.0-base",
            "FLUX.1-dev",
            "stable-diffusion-xl-base-1.0",
            "playground-v2.5",
        ]

    async def validate_api_key(self) -> bool:
        """
        Validate API key

        Returns:
            True if API key is valid
        """
        try:
            # Try a simple low-cost generation
            await self.generate_image(
                prompt="test",
                width=256,
                height=256,
                num_inference_steps=10
            )
            return True
        except Exception:
            return False


# Convenience function
async def quick_generate_image(
    prompt: str,
    output_path: str,
    api_key: Optional[str] = None,
    **kwargs
) -> str:
    """
    Quick image generation and save

    Args:
        prompt: Image prompt
        output_path: Where to save
        api_key: API key
        **kwargs: Additional parameters

    Returns:
        Path to saved image
    """
    client = HyperbolicClient(api_key=api_key)
    image_bytes = await client.generate_storyboard_frame(prompt, **kwargs)
    return await client.save_image(image_bytes, output_path)
