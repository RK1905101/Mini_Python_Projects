# Leetcode 394. Decode String

# Given an encoded string, return its decoded string.

# The encoding rule is: k[encoded_string], where the encoded_string inside the square brackets is being repeated exactly k times. Note that k is guaranteed to be a positive integer.

# You may assume that the input string is always valid; No extra white spaces, square brackets are well-formed, etc.

# Furthermore, you may assume that the original data does not contain any digits and that digits are only for those repeat numbers, k. For example, there won't be input like 3a or 2[4].
# ### Examples:

# Example 1:
 
#     Input: s = "3[a]2[bc]"
#     Output: "aaabcbc"

# Example 2:

#     Input: s = "3[a2[c]]"
#     Output: "accaccacc"

# Example 3:

#     Input: s = "2[abc]3[cd]ef"
#     Output: "abcabccdcdcdef"

# Example 4:

#     Input: s = "abc3[cd]xyz"
#     Output: "abccdcdcdxyz"
# ## Constraints:

#     1 <= s.length <= 30
#     s consists of lowercase English letters, digits, and square brackets '[]'.
#     s is guaranteed to be a valid input.
#     All the integers in s are in the range [1, 300].

#### Question link : [394_decode_string](https://leetcode.com/problems/decode-string/)


def extract_digit(self, i: int, s: str):
    digit = ""
    while (s[i] != "["):
        digit += s[i]
        i += 1
    # i + 1 to skip the [
    return i + 1, digit


def decode_word(self, i: int, s: str):
    concat = ""
    while(i < len(s) and s[i] != "]"):
        if (s[i].isdigit()):
            i, digit = self.extract_digit(i, s)
            i, word = self.decode_word(i, s)
            concat += int(digit) * word
        else:
            concat += s[i]
            i += 1
    return i + 1, concat


def decodeString(self, s: str) -> str:
    i, word = self.decode_word(0, s)
    return word
