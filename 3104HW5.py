import array
import math
import sys

# pre-order traversals of binary search trees
# Use and call tree class provided to make new trees

class Tree:
    def __init__(self, value, leftTree = None, rightTree = None):
        self.value = value # value at the node
        self.leftSubtree = leftTree
        self.rightSubtree = rightTree
    def __str__(self): # default string representation of the tree
        return "Tree(" + str(self.value) + ", " + str(self.leftSubtree) + ", " + str(self.rightSubtree) + ")" # string representation of the tree
    def __eq__(self, otherTree): # equality operator for trees
        # check if the values and subtrees are equal
        if self.value == otherTree.value and self.leftSubtree == otherTree.leftSubtree and self.rightSubtree == otherTree.rightSubtree:
            return True
        return False
    
t1 = Tree(3)
t2 = Tree(2, Tree(1), t1)
t3 = Tree(2, Tree(1), Tree(3))
print(t2 == t3) # True

# given a pre-order traversal of a binary search tree, reconstruct the tree and return the root node
# algorithm should be recursive
def preorderToTree(traversal):
    if not traversal:
        return None

    root_value = traversal[0]
    root = Tree(root_value)

    # Find the index where the right subtree starts
    right_subtree_index = len(traversal)
    for i in range(1, len(traversal)):
        if traversal[i] > root_value:
            right_subtree_index = i
            break

    # Recursively construct the left and right subtrees
    root.leftSubtree = preorderToTree(traversal[1:right_subtree_index])
    root.rightSubtree = preorderToTree(traversal[right_subtree_index:])

    return root # return the root of the tree
#raise NotImplementedError("Function not yet implemented")

# preToPost function takes preoder traversal of a BST (a list)
# and returns the postorder traversal of BST (another list) without using an intermediary tree
def preToPost(preTrav):
    if not preTrav:
        return []

    root_value = preTrav[0]

    # Find the index where the right subtree starts
    right_subtree_index = len(preTrav)
    for i in range(1, len(preTrav)):
        if preTrav[i] > root_value:
            right_subtree_index = i
            break

    # Recursively get the postorder traversals of the left and right subtrees
    left_post = preToPost(preTrav[1:right_subtree_index])
    right_post = preToPost(preTrav[right_subtree_index:])

    # Combine left and right postorders with the root value at the end
    return left_post + right_post + [root_value]
    #raise NotImplementedError("Function not yet implemented")

# Example usage:
preorder = [8, 5, 1, 7, 10, 12]
tree = preorderToTree(preorder)
print("Reconstructed Tree:", tree)  # Output: Reconstructed Tree
postorder = preToPost(preorder)
print("Postorder Traversal:", postorder)  # Output: Postorder Traversal
#----------------------------------------------
