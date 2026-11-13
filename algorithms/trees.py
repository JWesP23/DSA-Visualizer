from collections import deque

import streamlit as st

from data_structures.tree import (
    BinarySearchTree,
    RedBlackTree,
    Trie,
    inorder_values,
    level_order_values,
    postorder_values,
    preorder_values,
)
from visuals import tree_vis


def build_binary_search_tree(values):
    tree = BinarySearchTree()
    skipped = []
    for value in values:
        if not tree.insert(value):
            skipped.append(value)
    return tree, skipped


def animate_traversal(root, order, speed):
    visited_nodes = []

    def show(message, current):
        st.write(message)
        has_order = bool(visited_nodes)
        tree_vis.render_binary_tree(
            root,
            current=current,
            visited=set(visited_nodes),
            speed=speed,
            pause_after=not has_order,
        )
        if has_order:
            tree_vis.render_boxes(
                [node.value for node in visited_nodes],
                highlight_indices=[len(visited_nodes) - 1],
                label="Visit order",
                speed=speed,
                pause_after=True,
            )

    def record(node, message):
        visited_nodes.append(node)
        show(message, node)

    if order == "Preorder":
        st.write("Preorder trace: visit the node, then the left subtree, then the right subtree.")

        def preorder(node):
            if node is None:
                return
            record(node, f"Visit {node.value}.")
            if node.left is None:
                show(f"{node.value} has no left child.", node)
            else:
                show(f"Walk the left subtree of {node.value}.", node)
                preorder(node.left)
            if node.right is None:
                show(f"{node.value} has no right child.", node)
            else:
                show(f"Walk the right subtree of {node.value}.", node)
                preorder(node.right)

        preorder(root)
    elif order == "Inorder":
        st.write("Inorder trace: walk the left subtree, visit the node, then walk the right subtree.")

        def inorder(node):
            if node is None:
                return
            if node.left is None:
                show(f"{node.value} has no left child.", node)
            else:
                show(f"Walk the left subtree of {node.value} before visiting it.", node)
                inorder(node.left)
            record(node, f"Visit {node.value}.")
            if node.right is None:
                show(f"{node.value} has no right child.", node)
            else:
                show(f"Walk the right subtree of {node.value}.", node)
                inorder(node.right)

        inorder(root)
    elif order == "Postorder":
        st.write("Postorder trace: walk the left subtree, walk the right subtree, then visit the node.")

        def postorder(node):
            if node is None:
                return
            if node.left is None:
                show(f"{node.value} has no left child.", node)
            else:
                show(f"Walk the left subtree of {node.value}.", node)
                postorder(node.left)
            if node.right is None:
                show(f"{node.value} has no right child.", node)
            else:
                show(f"Walk the right subtree of {node.value}.", node)
                postorder(node.right)
            record(node, f"Visit {node.value}.")

        postorder(root)
    else:
        st.write("Level-order trace: visit nodes level by level. A queue holds the nodes that are waiting.")
        queue = deque([root])
        st.write("Put the root in the queue. The front of the queue is on the left.")
        tree_vis.render_binary_tree(root, current=root, visited=set(), speed=speed)
        _render_queue(queue, speed, pause_after=True)

        while queue:
            node = queue.popleft()
            visited_nodes.append(node)
            st.write(f"Dequeue {node.value} and visit it.")
            tree_vis.render_binary_tree(root, current=node, visited=set(visited_nodes), speed=speed)
            _render_queue(queue, speed, pause_after=False)
            tree_vis.render_boxes(
                [visited.value for visited in visited_nodes],
                highlight_indices=[len(visited_nodes) - 1],
                label="Visit order",
                speed=speed,
                pause_after=True,
            )

            enqueued = []
            if node.left is not None:
                queue.append(node.left)
                enqueued.append(f"left child {node.left.value}")
            if node.right is not None:
                queue.append(node.right)
                enqueued.append(f"right child {node.right.value}")

            if enqueued:
                st.write(f"Enqueue the {' and the '.join(enqueued)}.")
            else:
                st.write(f"{node.value} is a leaf, so nothing is enqueued.")
            tree_vis.render_binary_tree(root, current=node, visited=set(visited_nodes), speed=speed)
            _render_queue(queue, speed, pause_after=False)
            tree_vis.render_boxes(
                [visited.value for visited in visited_nodes],
                highlight_indices=[len(visited_nodes) - 1],
                label="Visit order",
                speed=speed,
                pause_after=True,
            )

    visit_order = [node.value for node in visited_nodes]
    expected = {
        "Preorder": preorder_values(root),
        "Inorder": inorder_values(root),
        "Postorder": postorder_values(root),
        "Level Order": level_order_values(root),
    }[order]
    if visit_order != expected:
        raise RuntimeError(f"{order} visit order {visit_order} did not match {expected}")

    st.write("Traversal finished.")
    tree_vis.render_boxes(visit_order, emphasize_indices=set(range(len(visit_order))), label="Final visit order")
    if order == "Inorder":
        st.write("That order is sorted. Inorder traversal of a binary search tree visits the values from smallest to largest.")
    elif order == "Postorder":
        st.write(f"The root {root.value} was visited last. Postorder finishes both subtrees before the node itself.")
    elif order == "Preorder":
        st.write(f"The root {root.value} was visited first. Preorder records a node before either of its subtrees.")
    else:
        st.write("Level order visits every node on a level before it moves to the next level.")


def animate_red_black_inserts(values, speed):
    tree = RedBlackTree()
    skipped = []

    def on_step(current_tree, message, focus):
        st.write(message)
        tree_vis.render_red_black_tree(current_tree.root, focus=focus, speed=speed, pause_after=True)

    for value in values:
        if not tree.insert(value, on_step=on_step):
            skipped.append(value)
            st.write(f"{value} is already in the tree, so it is skipped.")
            tree_vis.render_red_black_tree(tree.root, focus=[], speed=speed, pause_after=True)

    st.write("Insertion finished.")
    tree_vis.render_boxes(inorder_values(tree.root), label="Inorder (sorted order)")
    st.write("Notice that this is a binary search tree. As for the balance, even if it doesn't look balanced, notice how the red nodes are distributed. The black height is the same for every path from the root to a leaf.")
    return tree, skipped


def animate_trie_inserts(words, speed):
    trie = Trie()

    for word in words:
        path = []

        def on_step(message, node, index, status, word=word, path=path):
            if status == "start":
                path.clear()
            elif node is not trie.root and node not in path:
                path.append(node)
            done = status == "end"
            st.write(f'Insert "{word}": {message}')
            _render_word(word, index, done=done)
            tree_vis.render_trie(trie.root, current=node, path=set(path), speed=speed, pause_after=True)

        trie.insert(word, on_step=on_step)

    st.write("Every word is in the trie. Shared prefixes use the same nodes.")
    tree_vis.render_trie(trie.root, pause_after=True, speed=speed)
    return trie


def animate_trie_search(words, target, speed):
    trie = Trie()
    for word in words:
        trie.insert(word)

    st.write("The trie is built from the dictionary. Search walks one character at a time.")
    tree_vis.render_boxes(words, label="Dictionary")
    tree_vis.render_trie(trie.root, speed=speed, pause_after=True)

    path = []

    def on_step(message, node, index, status):
        if status == "start":
            path.clear()
        elif node is not trie.root and node not in path:
            path.append(node)
        done = status == "found"
        st.write(message)
        _render_word(word=target, index=index, done=done, missing=status == "missing")
        tree_vis.render_trie(trie.root, current=node, path=set(path), speed=speed, pause_after=True)

    found = trie.search(target, on_step=on_step)
    if found:
        st.write(f'"{target}" was found.')
    else:
        st.write(f'"{target}" was not found.')
    return found


def _render_queue(queue, speed, pause_after):
    if queue:
        tree_vis.render_boxes(
            [node.value for node in queue],
            highlight_indices=[0],
            label="Queue (front is on the left)",
            speed=speed,
            pause_after=pause_after,
        )
    else:
        st.write("The queue is empty.")
        if pause_after:
            tree_vis.pause(speed)


def _render_word(word, index, done=False, missing=False):
    emphasize = set(range(len(word))) if done else None
    highlight = None
    if not done and 0 <= index < len(word):
        highlight = [index]
    label = "Word"
    if missing:
        label = "Word (missing character highlighted)"
    tree_vis.render_boxes(list(word), highlight_indices=highlight, emphasize_indices=emphasize, label=label)
