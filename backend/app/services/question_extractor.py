import re
from typing import List

def extract_questions(text: str) -> List[str]:
    """
    Extracts questions from a block of text.
    Looks for sentences ending with '?' or starting with question keywords.

    Args:
        text (str): Input text

    Returns:
        List[str]: List of extracted questions
    """
    # Pattern 1: Sentences ending with '?'
    qm_questions = re.findall(r'([A-Z][^?]*\?)', text)

    # Pattern 2: Sentences starting with question words (no '?')
    keyword_pattern = r'\b(?:What|Why|How|When|Where|Who|Which)[^?.!\n]*[.!\n]'
    keyword_questions = re.findall(keyword_pattern, text, re.IGNORECASE)

    # Combine, strip whitespace, remove duplicates
    all_questions = set(q.strip() for q in qm_questions + keyword_questions)
    return list(all_questions)
