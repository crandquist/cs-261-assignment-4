# Name: Cat Randquist
# OSU Email: randquic@oregonstate
# Course: CS261 - Data Structures
# Assignment: 4
# Due Date: 11/20/23
# Description: AVL Tree Implementation


import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Adds a new value to the AVL tree while maintaining its AVL property.
        """
        new_node = AVLNode(value)

        if self._root is None:
            self._root = new_node
        else:
            self._root = self._add_helper(self._root, new_node)

    def _add_helper(self, current: AVLNode, new_node: AVLNode) -> AVLNode:
        """
        Helper method to recursively add a new node while maintaining AVL property.
        """
        if current is None:
            return new_node

        if new_node.value < current.value:
            current.left = self._add_helper(current.left, new_node)
        else:
            current.right = self._add_helper(current.right, new_node)

        # Update the height of the current node
        current.height = 1 + max(self._get_height(current.left), self._get_height(current.right))

        # Rebalance the tree if necessary
        return self._rebalance(current)

    def remove(self, value: object) -> bool:
        """
        Removes a node with the given value while maintaining AVL property.
        Returns True if the value was found and removed, False otherwise.
        """
        if not self._root:
            return False  # Empty tree

        # Call helper method to remove the node
        if not self._remove_helper(self._root, None, value):
            return False  # Value not found in the tree
        else:
            return True  # Value removed successfully

    def _remove_helper(self, current: AVLNode, parent: AVLNode, value: object) -> bool:
        """
        Helper method to recursively remove a node while maintaining AVL property.
        Returns True if the value was found and removed, False otherwise.
        """
        if not current:
            return False  # Value not found

        if value < current.value:
            # Search in the left subtree
            if not self._remove_helper(current.left, current, value):
                return False
        elif value > current.value:
            # Search in the right subtree
            if not self._remove_helper(current.right, current, value):
                return False
        else:
            # Value found, perform removal
            if not current.left:
                # No left child or no children at all
                if not current.right:
                    # Leaf node case
                    if parent:
                        if parent.left == current:
                            parent.left = None
                        else:
                            parent.right = None
                    else:
                        self._root = None
                else:
                    # Only right child case
                    if parent:
                        if parent.left == current:
                            parent.left = current.right
                        else:
                            parent.right = current.right
                    else:
                        self._root = current.right
            elif not current.right:
                # Only left child case
                if parent:
                    if parent.left == current:
                        parent.left = current.left
                    else:
                        parent.right = current.left
                else:
                    self._root = current.left
            else:
                # Node with two children case
                # Call the _remove_two_subtrees method
                self._root = self._remove_two_subtrees(current, current)

            # After removal, update heights and rebalance
            if parent:
                parent.height = 1 + max(self._get_height(parent.left), self._get_height(parent.right))
                self._rebalance(parent)

            return True  # Value found and removed

        # Update the height and rebalance the current node
        current.height = 1 + max(self._get_height(current.left), self._get_height(current.right))
        self._rebalance(current)

        return True  # Value found and removed

    def _remove_two_subtrees(self, remove_parent: AVLNode, remove_node: AVLNode) -> AVLNode:
        """
        Removes a node with both left and right subtrees while maintaining AVL property.
        """
        successor = remove_node.right
        successor_parent = remove_node

        # Find the in-order successor (the leftmost node in the right subtree)
        while successor.left:
            successor_parent = successor
            successor = successor.left

        # If the in-order successor is not the right child of the node to remove
        if successor != remove_node.right:
            # Update the parent pointers and left child of the in-order successor
            successor_parent.left = successor.right
            if successor.right:
                successor.right.parent = successor_parent

            # Update the right subtree of the node to remove
            successor.right = remove_node.right
            remove_node.right.parent = successor

        # Update the left subtree of the node to remove
        successor.left = remove_node.left
        remove_node.left.parent = successor

        # Update the parent pointers for the node to remove
        if remove_parent:
            if remove_node == remove_parent.left:
                remove_parent.left = successor
            else:
                remove_parent.right = successor

        successor.parent = remove_parent

        # Return the successor as the new root after removal
        return self._rebalance(successor)

    def _balance_factor(self, node: AVLNode) -> int:
        """
        Calculates the balance factor for a given node in the AVL tree.
        """
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _get_height(self, node: AVLNode) -> int:
        """
        Returns the height of a node in the AVL tree.
        """
        if node is None:
            return -1  # Height of an empty node is -1
        else:
            return node.height

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        Performs a left rotation on the given node.
        """
        new_root = node.right
        node.right = new_root.left

        if new_root.left:
            new_root.left.parent = node

        new_root.parent = node.parent

        if not node.parent:
            self._root = new_root
        elif node == node.parent.left:
            node.parent.left = new_root
        else:
            node.parent.right = new_root

        new_root.left = node
        node.parent = new_root

        # Update heights after rotation
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        new_root.height = 1 + max(self._get_height(new_root.left), self._get_height(new_root.right))

        return new_root

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """
        Performs a right rotation on the given node.
        """
        new_root = node.left
        node.left = new_root.right

        if new_root.right:
            new_root.right.parent = node

        new_root.parent = node.parent

        if not node.parent:
            self._root = new_root
        elif node == node.parent.right:
            node.parent.right = new_root
        else:
            node.parent.left = new_root

        new_root.right = node
        node.parent = new_root

        # Update heights after rotation
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        new_root.height = 1 + max(self._get_height(new_root.left), self._get_height(new_root.right))

        return new_root
    def _update_height(self, node: AVLNode) -> None:
        def _update_height(self, node: AVLNode) -> None:
            """
            Updates the height of a node in the AVL tree.
            """
            node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

    def _rebalance(self, node: AVLNode) -> None:
        """
        Rebalances the AVL tree after insertion if necessary.
        """
        while node is not None:
            self._update_height(node)

            balance = self._balance_factor(node)

            # Left heavy
            if balance > 1:
                # Left-Right case
                if self._balance_factor(node.left) < 0:
                    self._rotate_left(node.left)
                self._rotate_right(node)
            # Right heavy
            elif balance < -1:
                # Right-Left case
                if self._balance_factor(node.right) > 0:
                    self._rotate_right(node.right)
                self._rotate_left(node)

            node = node.parent

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        tree = AVL(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
