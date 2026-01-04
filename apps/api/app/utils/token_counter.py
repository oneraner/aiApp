"""Token counting and validation utilities for rate limiting"""


def estimate_tokens(text: str) -> int:
    """
    Estimate token count from text.
    
    Rule of thumb:
    - English: ~4 chars = 1 token
    - Chinese: ~2-3 chars = 1 token
    
    We use conservative estimate (3 chars = 1 token) to be safe.
    """
    if not text:
        return 0
    return max(1, len(text) // 3)


def validate_input_size(content: str, max_chars: int = 300) -> tuple[bool, str]:
    """
    Validate if input is within size limits.
    
    Args:
        content: Input text to validate
        max_chars: Maximum allowed characters (default: 300)
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not content:
        return True, ""
    
    char_count = len(content)
    
    if char_count > max_chars:
        return False, f"輸入過長：{char_count} 字元（限制 {max_chars} 字元）"
    
    return True, ""
