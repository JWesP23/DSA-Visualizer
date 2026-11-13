from collections import deque


class BinaryTreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:

    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = BinaryTreeNode(value)
            return True

        current = self.root
        while True:
            if value == current.value:
                return False
            if value < current.value:
                if current.left is None:
                    current.left = BinaryTreeNode(value)
                    return True
                current = current.left
            else:
                if current.right is None:
                    current.right = BinaryTreeNode(value)
                    return True
                current = current.right


class TrieNode:
    def __init__(self, char=""):
        self.char = char
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, on_step=None):
        node = self.root
        if on_step:
            on_step("Start at the root.", node, -1, "start")

        for index, char in enumerate(word):
            created = char not in node.children
            if created:
                node.children[char] = TrieNode(char)
            node = node.children[char]
            if on_step:
                action = "Add" if created else "Follow"
                on_step(f"{action} '{char}'.", node, index, "create" if created else "follow")

        node.is_end = True
        if on_step:
            on_step(f'Mark the end of "{word}".', node, len(word) - 1, "end")
        return node

    def contains(self, word):
        node = self._walk(word)
        return node is not None and node.is_end

    def search(self, word, on_step=None):
        node = self.root
        if on_step:
            on_step(f'Search for "{word}", starting at the root.', node, -1, "start")

        for index, char in enumerate(word):
            if char not in node.children:
                if on_step:
                    on_step(
                        f"There is no edge for '{char}', so \"{word}\" is not in the trie.",
                        node,
                        index,
                        "missing",
                    )
                return False
            node = node.children[char]
            if on_step:
                on_step(f"Follow '{char}'.", node, index, "follow")

        if node.is_end:
            if on_step:
                on_step(f'"{word}" is in the trie.', node, len(word) - 1, "found")
            return True

        if on_step:
            on_step(
                f'The letters of "{word}" are a prefix in the trie, but no word ends here.',
                node,
                len(word) - 1,
                "prefix",
            )
        return False

    def _walk(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return None
            node = node.children[char]
        return node


class RBNode:
    def __init__(self, value):
        self.value = value
        self.color = "red"
        self.left = None
        self.right = None
        self.parent = None


class RedBlackTree:

    def __init__(self):
        self.root = None

    def insert(self, value, on_step=None):
        node = RBNode(value)
        parent = None
        current = self.root

        while current is not None:
            parent = current
            if value == current.value:
                return False
            if value < current.value:
                current = current.left
            else:
                current = current.right

        node.parent = parent
        if parent is None:
            self.root = node
        elif value < parent.value:
            parent.left = node
        else:
            parent.right = node

        if on_step:
            on_step(
                self,
                f"Insert {value} where a binary search tree would put it, and color it red.",
                [node],
            )

        self._fixup(node, on_step)
        return True

    def _fixup(self, inserted, on_step):
        node = inserted

        while node.parent is not None and node.parent.color == "red":
            parent = node.parent
            grandparent = parent.parent
            if parent is grandparent.left:
                uncle = grandparent.right
                if uncle is not None and uncle.color == "red":
                    parent.color = "black"
                    uncle.color = "black"
                    grandparent.color = "red"
                    if on_step:
                        on_step(
                            self,
                            f"The uncle of {node.value} is red. Recolor the parent and uncle black, and the grandparent red.",
                            [node, parent, uncle, grandparent],
                        )
                    node = grandparent
                else:
                    if node is parent.right:
                        self._rotate_left(parent)
                        node = parent
                        parent = node.parent
                        grandparent = parent.parent
                        if on_step:
                            on_step(
                                self,
                                f"Rotated left so {node.value} is the left child of {parent.value}.",
                                [node, parent],
                            )
                    parent.color = "black"
                    grandparent.color = "red"
                    self._rotate_right(grandparent)
                    if on_step:
                        on_step(
                            self,
                            f"Colored {parent.value} black and {grandparent.value} red, then rotated right around {grandparent.value}.",
                            [node, parent, grandparent],
                        )
            else:
                uncle = grandparent.left
                if uncle is not None and uncle.color == "red":
                    parent.color = "black"
                    uncle.color = "black"
                    grandparent.color = "red"
                    if on_step:
                        on_step(
                            self,
                            f"The uncle of {node.value} is red. Recolor the parent and uncle black, and the grandparent red.",
                            [node, parent, uncle, grandparent],
                        )
                    node = grandparent
                else:
                    if node is parent.left:
                        self._rotate_right(parent)
                        node = parent
                        parent = node.parent
                        grandparent = parent.parent
                        if on_step:
                            on_step(
                                self,
                                f"Rotated right so {node.value} is the right child of {parent.value}.",
                                [node, parent],
                            )
                    parent.color = "black"
                    grandparent.color = "red"
                    self._rotate_left(grandparent)
                    if on_step:
                        on_step(
                            self,
                            f"Colored {parent.value} black and {grandparent.value} red, then rotated left around {grandparent.value}.",
                            [node, parent, grandparent],
                        )

        if self.root.color == "red":
            self.root.color = "black"
            if on_step:
                on_step(
                    self,
                    "Color the root black. The root of a red-black tree is always black.",
                    [self.root],
                )
        elif on_step:
            on_step(
                self,
                f"Inserting {inserted.value} is complete, and the red-black properties hold.",
                [inserted],
            )

    def _rotate_left(self, pivot):
        child = pivot.right
        pivot.right = child.left
        if child.left is not None:
            child.left.parent = pivot

        child.parent = pivot.parent
        if pivot.parent is None:
            self.root = child
        elif pivot is pivot.parent.left:
            pivot.parent.left = child
        else:
            pivot.parent.right = child

        child.left = pivot
        pivot.parent = child

    def _rotate_right(self, pivot):
        child = pivot.left
        pivot.left = child.right
        if child.right is not None:
            child.right.parent = pivot

        child.parent = pivot.parent
        if pivot.parent is None:
            self.root = child
        elif pivot is pivot.parent.right:
            pivot.parent.right = child
        else:
            pivot.parent.left = child

        child.right = pivot
        pivot.parent = child


def inorder_values(node, values=None):
    if values is None:
        values = []
    if node is None:
        return values
    inorder_values(node.left, values)
    values.append(node.value)
    inorder_values(node.right, values)
    return values


def preorder_values(node, values=None):
    if values is None:
        values = []
    if node is None:
        return values
    values.append(node.value)
    preorder_values(node.left, values)
    preorder_values(node.right, values)
    return values


def postorder_values(node, values=None):
    if values is None:
        values = []
    if node is None:
        return values
    postorder_values(node.left, values)
    postorder_values(node.right, values)
    values.append(node.value)
    return values


def level_order_values(root):
    if root is None:
        return []
    values = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        values.append(node.value)
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)
    return values
