def is_safe_input(description):
    """Return False if input contains banned/inappropriate words."""
    blocked_keywords = [
        "xxx", "nude", "sex", "kill", "porn", "wtf", "fck", "suck", "ass", "dark web"
    ]
    description = description.lower()
    return not any(word in description for word in blocked_keywords)
