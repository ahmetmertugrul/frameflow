"""
SambaNova AI Integration
Fast LLM inference for screenplay generation
"""

import os
import httpx
from typing import Optional, Dict, Any, List
import asyncio


class SambaNovaClient:
    """Client for SambaNova AI API"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize SambaNova client

        Args:
            api_key: SambaNova API key (or use SAMBANOVA_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("SAMBANOVA_API_KEY")
        if not self.api_key:
            raise ValueError("SambaNova API key not provided")

        self.base_url = "https://api.sambanova.ai/v1"
        self.default_model = "Meta-Llama-3.1-70B-Instruct"
        self.timeout = 60.0

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> str:
        """
        Generate text using SambaNova LLM

        Args:
            prompt: User prompt
            system_prompt: System prompt for context
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional API parameters

        Returns:
            Generated text
        """
        messages = []

        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })

        messages.append({
            "role": "user",
            "content": prompt
        })

        payload = {
            "model": kwargs.get("model", self.default_model),
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **{k: v for k, v in kwargs.items() if k != "model"}
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers
            )

            response.raise_for_status()
            result = response.json()

            return result["choices"][0]["message"]["content"]

    async def generate_structured(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        schema: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate structured output (JSON)

        Args:
            prompt: User prompt
            system_prompt: System prompt
            schema: JSON schema for structured output
            **kwargs: Additional parameters

        Returns:
            Parsed JSON response
        """
        import json

        # Add JSON instructions to system prompt
        json_instruction = "\n\nRespond ONLY with valid JSON matching the requested structure. No other text."
        full_system_prompt = (system_prompt or "") + json_instruction

        response_text = await self.generate(
            prompt=prompt,
            system_prompt=full_system_prompt,
            temperature=kwargs.get("temperature", 0.5),  # Lower temp for structured output
            **kwargs
        )

        # Extract JSON from response
        try:
            # Try to find JSON in response
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1

            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # Try parsing entire response
                return json.loads(response_text)

        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON response: {e}\nResponse: {response_text}")

    async def batch_generate(
        self,
        prompts: List[str],
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> List[str]:
        """
        Generate multiple completions in parallel

        Args:
            prompts: List of prompts
            system_prompt: System prompt for all requests
            **kwargs: Additional parameters

        Returns:
            List of generated texts
        """
        tasks = [
            self.generate(prompt, system_prompt, **kwargs)
            for prompt in prompts
        ]

        return await asyncio.gather(*tasks)

    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count for text

        Args:
            text: Input text

        Returns:
            Estimated token count (rough approximation)
        """
        # Rough estimate: ~4 characters per token
        return len(text) // 4

    def validate_api_key(self) -> bool:
        """
        Validate API key

        Returns:
            True if API key is valid
        """
        try:
            # Try a simple completion
            import asyncio
            asyncio.run(self.generate("Hello", max_tokens=5))
            return True
        except Exception:
            return False


# Convenience function for quick usage
async def quick_generate(
    prompt: str,
    system_prompt: Optional[str] = None,
    api_key: Optional[str] = None,
    **kwargs
) -> str:
    """
    Quick generation function without creating client instance

    Args:
        prompt: User prompt
        system_prompt: System prompt
        api_key: API key
        **kwargs: Additional parameters

    Returns:
        Generated text
    """
    client = SambaNovaClient(api_key=api_key)
    return await client.generate(prompt, system_prompt, **kwargs)
