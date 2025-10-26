#  anagram_checker.py


def anagram_checker(word1: str, word2: str) -> bool:
    list1 = sorted(word1.lower().strip().replace(" ", ""))
    list2 = sorted(word2.lower().strip().replace(" ", ""))
    return True if list1 == list2 else False
