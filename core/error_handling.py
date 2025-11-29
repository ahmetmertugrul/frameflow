"""
Error Handling Utilities
Enhanced error handling and user feedback for FrameFlow
"""

from typing import Optional, Callable, Any
import functools
import traceback
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("FrameFlow")


class FrameFlowError(Exception):
    """Base exception for FrameFlow errors"""
    def __init__(self, message: str, user_message: Optional[str] = None):
        self.message = message
        self.user_message = user_message or message
        super().__init__(self.message)


class APIKeyError(FrameFlowError):
    """API key is missing or invalid"""
    pass


class GenerationError(FrameFlowError):
    """Error during content generation"""
    pass


class ValidationError(FrameFlowError):
    """Input validation error"""
    pass


def handle_errors(user_friendly: bool = True):
    """
    Decorator for error handling with user-friendly messages

    Args:
        user_friendly: If True, return user-friendly error messages
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            try:
                return await func(*args, **kwargs)
            except FrameFlowError as e:
                logger.error(f"FrameFlow error in {func.__name__}: {e.message}")
                if user_friendly:
                    return None, f"❌ {e.user_message}"
                raise
            except Exception as e:
                logger.error(f"Unexpected error in {func.__name__}: {str(e)}\n{traceback.format_exc()}")
                if user_friendly:
                    return None, f"❌ An unexpected error occurred. Please try again."
                raise

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except FrameFlowError as e:
                logger.error(f"FrameFlow error in {func.__name__}: {e.message}")
                if user_friendly:
                    return None, f"❌ {e.user_message}"
                raise
            except Exception as e:
                logger.error(f"Unexpected error in {func.__name__}: {str(e)}\n{traceback.format_exc()}")
                if user_friendly:
                    return None, f"❌ An unexpected error occurred. Please try again."
                raise

        # Return appropriate wrapper based on function type
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def validate_story_input(prompt: str, min_length: int = 10) -> None:
    """
    Validate story input

    Args:
        prompt: Story prompt to validate
        min_length: Minimum prompt length

    Raises:
        ValidationError: If validation fails
    """
    if not prompt or not prompt.strip():
        raise ValidationError(
            "Empty story prompt",
            "⚠️ Lütfen bir hikaye fikri girin."
        )

    if len(prompt.strip()) < min_length:
        raise ValidationError(
            f"Prompt too short: {len(prompt)} < {min_length}",
            f"⚠️ Hikaye fikri çok kısa. En az {min_length} karakter gerekli."
        )


def format_success_message(operation: str, details: str) -> str:
    """Format success message"""
    return f"✅ {operation} başarılı! {details}"


def format_progress_message(operation: str, progress: float, details: str = "") -> str:
    """Format progress message"""
    progress_bar = "█" * int(progress * 20) + "░" * (20 - int(progress * 20))
    percentage = int(progress * 100)
    return f"⏳ {operation}... [{progress_bar}] {percentage}% {details}"


def format_error_message(error: Exception, context: str = "") -> str:
    """Format error message for user"""
    if isinstance(error, APIKeyError):
        return "❌ API anahtarı hatası. Lütfen .env dosyanızı kontrol edin."
    elif isinstance(error, GenerationError):
        return f"❌ Oluşturma hatası: {error.user_message}"
    elif isinstance(error, ValidationError):
        return f"❌ Doğrulama hatası: {error.user_message}"
    else:
        ctx = f" ({context})" if context else ""
        return f"❌ Beklenmeyen bir hata oluştu{ctx}. Lütfen tekrar deneyin."


class ProgressTracker:
    """Track progress of long-running operations"""

    def __init__(self, total_steps: int):
        self.total_steps = total_steps
        self.current_step = 0
        self.messages = []

    def update(self, step_name: str, increment: int = 1):
        """Update progress"""
        self.current_step += increment
        progress = self.current_step / self.total_steps
        message = format_progress_message(
            step_name,
            progress,
            f"({self.current_step}/{self.total_steps})"
        )
        self.messages.append(message)
        logger.info(f"Progress: {message}")
        return message

    def complete(self, final_message: str):
        """Mark as complete"""
        self.current_step = self.total_steps
        message = format_success_message("Tamamlandı", final_message)
        self.messages.append(message)
        logger.info(f"Complete: {message}")
        return message
