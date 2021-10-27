# Leetcode 124. Binary Tree Maximum Path Sum

# Given an integer n, return the number of prime numbers that are strictly less than n.
# A path in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. A node can only appear in the sequence at most once. Note that the path does not need to pass through the root.

# The path sum of a path is the sum of the node's values in the path.

# Given the root of a binary tree, return the maximum path sum of any path.

# ### Examples:

# Example 1:

#     Input: n = 10
#     Output: 4
#     Explanation: There are 4 prime numbers less than 10, they are 2, 3, 5, 7.

#     Input: root = [1,2,3]
#     Output: 6
#     Explanation: The optimal path is 2 -> 1 -> 3 with a path sum of 2 + 1 + 3 = 6.

# Example 2:

#     Input: n = 0
#     Output: 0

# Example 3:

#     Input: n = 1
#     Output: 0

#     Input: root = [-10,9,20,null,null,15,7]
#     Output: 42
#     Explanation: The optimal path is 15 -> 20 -> 7 with a path sum of 15 + 20 + 7 = 42.


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    
    def getMaxPath(self, node: TreeNode) -> int:
        if node is None:
            return 0
        
        left = self.getMaxPath(node.left)
        right = self.getMaxPath(node.right)
        
        
        currentMax = node.val
        if left > 0 and right > 0:
            currentMax = left + node.val + right
        elif left > 0:
            currentMax = left + node.val
        elif right > 0:
            currentMax = node.val + right
        
        self.maxSeen = max(currentMax, self.maxSeen)
        
        # we only care about positive gains so just return 0 if our gains are negative
        if left > right:
            return max(left + node.val, 0)
        else:
            return max(right + node.val, 0)
    
    def maxPathSum(self, root: TreeNode) -> int:
        if root is None:
            return 0
        
        
        self.maxSeen = root.val
        
        left = self.getMaxPath(root.left)
        right = self.getMaxPath(root.right)
        
        
        currentMax = root.val 
        if left > 0 and right > 0:
            currentMax = left + root.val + right
        elif left > 0:
            currentMax = left + root.val
        elif right > 0:
            currentMax = root.val + right
            
        
        return max(currentMax, self.maxSeen)
