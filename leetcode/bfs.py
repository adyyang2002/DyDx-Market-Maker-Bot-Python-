## Create a tree
"""
            1
          |   |
        2       3
      |   |
    4       5

"""

"""

DFS - HW.

preorder
inorder
postorder

Be able to write recursively too.
"""

class BinaryNode:

    def __init__(self, value, left = None, right = None):
        self.value = value
        self.left = left
        self.right = right
    

    def iterationBFS(self):
        """
        Prints a BFS using a queue using iteration.
        """
        queue = [self]
        while queue:
            curr = queue.pop(0)
            if curr.value:
                print(curr.value)
            if curr.left:
                queue.append(curr.left)
            if curr.right:
                queue.append(curr.right)

        return

    def iterativePostOrderDFS(self):
        """
        Prints a post order DFS using a stack using iteration.
        """
        # post_order = []
        stack = [self]
        visited = {self}
        while stack:
            top = stack[-1]
            no_next = True
            # If the right child has not been visited, add to stack
            if top.right and top.right not in visited:
                stack.append(top.right)
                visited.add(top.right)
                no_next = False
            # If the left child has not been visited, add to stack
            if top.left and top.left not in visited:
                stack.append(top.left)
                visited.add(top.left)
                no_next = False
            # If leaf, print
            if no_next:
                print(top.value)
                stack.pop()
        # return post_order

    def iterativeInOrderDFS(self):
        """
        Prints an in order DFS using stack using iteration
        """

        # stack = [self]
        # visited = set()
        stack = []
        curr = self
        while True:
            while curr:
                stack.append(curr)
                curr = curr.left
            if not stack:
                return
            node = stack.pop()
            if node:
                print(node.value)
            curr = node.right

    def recursiveInOrderDFS(self):
        """In order DFS using recursion"""
        node = self
        if self:
            node.left.rec



leaf_4 = BinaryNode(4)
leaf_5 = BinaryNode(5)
node_2 = BinaryNode(2, leaf_4, leaf_5)
leaf_3 = BinaryNode(3)
root = BinaryNode(1, node_2, leaf_3)

print("BFS with iteration: ")
root.iterationBFS()

print("Post order DFS with iteration: ")
root.iterativePostOrderDFS()

print(f'In order DFS with iteration: ')
root.iterativeInOrderDFS()

print(f'In order DFS with recursion: ')
root.recursiveInOrderDFS()