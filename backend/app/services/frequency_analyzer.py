from collections import Counter
from typing import List, Tuple

def count_questions(questions: List[str]) -> Counter:
    """
    Count how many times each question appears.

    Args:
        questions (List[str]): List of questions

    Returns:
        Counter: Frequencies
    """
    return Counter(questions)

def rank_questions(counter: Counter) -> List[Tuple[str, int]]:
    """
    Sort questions by frequency in descending order.

    Args:
        counter (Counter): Counter of questions

    Returns:
        List of (question, count) tuples
    """
    return counter.most_common()
