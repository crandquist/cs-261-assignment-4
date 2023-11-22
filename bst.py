# Name: Cat Randquist
# OSU Email: randquic@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4
# Due Date: 11/20/23
# Description:


import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value  # to store node's data
        self.left = None  # pointer to root of left subtree
        self.right = None  # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.

        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Adds a new node to the tree.
        """

        # Create a new node with the given value.
        new_node = BSTNode(value)

        # If the tree is empty, set the new node as the root.
        if self._root is None:
            self._root = new_node

        # Otherwise, traverse the tree and add the new node in the correct position.
        else:
            current = self._root
            while True:

                # If the value is less than the current node's value, go left.
                if value < current.value:

                    # If the current node's left child is None, set the new node as the left child.
                    if current.left is None:
                        current.left = new_node
                        # Break out of the loop, new node added.
                        break
                    else:
                        # Otherwise, set the current node to the left child and continue traversing.
                        current = current.left

                # If the value is greater than the current node's value, go right.
                else:
                    if current.right is None:
                        current.right = new_node

                        # Break out of the loop, new node added.
                        break

                    # Otherwise, set the current node to the right child and continue traversing.
                    else:
                        current = current.right

    def remove(self, value):
        """
        Removes the node with the given value from the tree.
        """

        # If the tree is empty, return False.
        if self._root is None:
            return False  # If tree is empty, return False

        # Find the node to remove and its parent.
        parent, node = self._find_node(value)

        if node is None:
            return False  # If value doesn't exist in the tree, return False

        num_children = sum(1 for child in (node.left, node.right) if child)

        # Remove the node based on the number of children.
        if num_children == 0:
            self._remove_no_subtrees(parent, node)
        elif num_children == 1:
            self._remove_one_subtree(parent, node)
        else:
            self._remove_two_subtrees(parent, node)

        return True  # Return True indicating successful removal

    def _find_node(self, value):
        """
        Finds the node with the given value and returns the parent and node.
        """
        parent = None
        current = self._root

        # Traverse the tree until the value is found or the end of the tree is reached.
        while current and current.value != value:
            parent = current
            if value < current.value:
                current = current.left
            else:
                current = current.right

        # Return the parent and node.
        return parent, current

    def _remove_no_subtrees(self, remove_parent, remove_node):
        """
        Removes a node that has no subtrees.
        """
        # Remove node that has no subtrees (no left or right nodes)
        if remove_parent is None:
            self._root = None
        elif remove_parent.left == remove_node:
            remove_parent.left = None
        else:
            remove_parent.right = None

    def _remove_one_subtree(self, remove_parent, remove_node):
        """
        Removes a node that has one subtree.
        """

        # Determine the existing subtree (left or right)
        if remove_node.left:
            subtree = remove_node.left
        else:
            subtree = remove_node.right

        # Adjust the parent's pointer to the subtree
        if remove_parent is None:
            self._root = subtree
        elif remove_parent.left == remove_node:
            remove_parent.left = subtree
        else:
            remove_parent.right = subtree

    def _remove_two_subtrees(self, remove_parent, remove_node):
        """
        Removes a node that has two subtrees.
        """
        successor_parent = remove_node
        successor = remove_node.right

        # Find the successor node
        while successor.left:
            successor_parent = successor
            successor = successor.left

        # Replace the node's value with the successor's value
        remove_node.value = successor.value

        # Remove the successor node
        if successor_parent.left == successor:
            successor_parent.left = successor.right
        else:
            successor_parent.right = successor.right

    def contains(self, value: object) -> bool:
        """
        Returns True if the value is in the tree, otherwise False.
        """

        # If the tree is empty, return False.
        if self._root is None:
            return False

        # Start traversal from the root
        current = self._root

        # Traverse the tree to find the value
        while current:
            if current.value == value:
                # Value found, return True
                return True

            # Move to the left subtree if value is smaller
            elif value < current.value:
                current = current.left
            # Move to the right subtree if value is larger
            else:
                current = current.right

        # Value not found, return False
        return False

    def inorder_traversal(self) -> 'Queue':
        """
        Performs an iterative inorder traversal of the tree and returns a Queue with visited node values.
        """
        result_queue = Queue()
        stack = Stack()

        current = self._root

        while current or not stack.is_empty():
            # Go to the leftmost node and add nodes to stack
            while current:
                stack.push(current)
                current = current.left

            # Process nodes in stack (in-order)
            current = stack.pop()
            # Add node value to the queue
            result_queue.enqueue(current.value)

            # Move to the right subtree
            current = current.right

        return result_queue

    def find_min(self) -> object:
        """
        Returns the lowest value in the tree.
        """
        if self._root is None:
            # If tree is empty, return None
            return None

        current = self._root

        # Traverse to the leftmost node (the node with the minimum value)
        while current.left:
            current = current.left

        return current.value

    def find_max(self) -> object:
        """
        Returns the highest value in the tree.
        """
        if self._root is None:
            # If tree is empty, return None
            return None

        current = self._root

        # Traverse to the rightmost node (the node with the maximum value)
        while current.right:
            current = current.right

        return current.value

    def is_empty(self) -> bool:
        """
        Returns True if the tree is empty, otherwise False.
        """
        return self._root is None

    def make_empty(self) -> None:
        """
        Removes all nodes from the tree by setting the root to None.
        """
        self._root = None



# ------------------- BASIC TESTING -----------------------------------------

if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
