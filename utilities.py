def escape_braces(text: str) -> str:
    return text.replace('{', '{{').replace('}', '}}')