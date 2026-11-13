import random

import streamlit as st

from algorithms import trees
from visuals import tree_vis

st.title("Binary Trees")

st.write(
    "A Binary Tree is a tree whose nodes have at most two children. Binary trees can have duplicate values."
)

st.write(
    "A Binary Search Tree is a binary tree where each node follows the property that if it has a left child, that left child is strictly smaller than the node and if it has a right child, the right child is strictly larger than the node. Binary trees cannot have duplicate values."
)

traversal = st.selectbox(
    "Choose a traversal",
    ["Preorder", "Inorder", "Postorder", "Level Order"],
)
source = st.radio(
    "How should the tree be built?",
    ["Random", "Custom"],
    captions=[
        "Insert random distinct integers",
        "Insert integers you type, from left to right",
    ],
)

if source == "Random":
    size = st.slider("Number of values", 4, 10, 7)
else:
    raw_values = st.text_input("Values", "8, 3, 10, 1, 6, 14, 4")

speed = st.selectbox("Animation speed", [1, 2, 3, 4, 5, "Instant"])

match traversal:
    case "Preorder":
        st.write(
            "Preorder visits each node before recursively visiting its subtrees "
            "(left then right). That is, it traverses in this order:"
        )
        st.markdown(
            "<div style='text-align: center;'><b>node -> left subtree -> right subtree</b></div>",
            unsafe_allow_html=True,
        )
        st.write(
            "One of the uses for a preorder traversal is to generate a prefix expression (also known as \"Polish Notation\"). "
            "Every traversal looks at each node once, so the runtime is O(n)."
        )
    case "Inorder":
        st.write(
            "Inorder recursively visits each left subtree, then the node, and then recursively visits each right subtree. " \
            "That is, it traverses in this order:"
        )
        st.markdown(
            "<div style='text-align: center;'><b>left subtree -> node -> right subtree</b></div>",
            unsafe_allow_html=True,
        )
        st.write(
            "One of the uses for an inorder traversal is to generate an infix expression. "
            "Another use of inorder is to generate a sorted list of the values in a binary search tree. "
            "In a binary search tree, the left child is always smaller than its parent node and the right child is always larger, therefore inorder traversal of a binary search tree will visit nodes in the order of smallest to largest. "
            "Every traversal looks at each node once, so the runtime is O(n)."
        )
    case "Postorder":
        st.write(
            "Postorder recursively visits each left subtree, then recursively visits each right subtree, then finally visits the node. " \
            "That is, it traverses in this order:"
        )
        st.markdown(
            "<div style='text-align: center;'><b>left subtree -> right subtree -> node</b></div>",
            unsafe_allow_html=True,
        )
        st.write(
            "One of the uses for a postorder traversal is to evaluate postfix expressions (also known as \"Reverse Polish Notation\"). "
            "Another use of postorder is to delete a tree, because postorder visits all child nodes before visiting the parent. "
            "Every traversal looks at each node once, so the runtime is O(n)."
        )
    case "Level Order":
        st.write(
            "Level Order visits the node, then the left subtree, then the right subtree. " \
            "That is, it traverses in this order:"
        )
        st.markdown(
            "<div style='text-align: center;'><b>node -> left subtree -> right subtree</b></div>",
            unsafe_allow_html=True,
        )
        st.write(
            "Level Order traversal uses a queue, rather than recursion, to traverse the tree."
            "It is essentially the same as a breadth-first traversal: it starts with just the root in its queue, dequeues the node at the front of the queue to visit it, enqueues the node's children, and continues until the queue is empty. " \
            "One of the uses for a level-order traversal is to perform a breadth-first search of the tree. "
            "Every traversal looks at each node once, so the runtime is O(n)."
        )

if st.button("Run"):
    if source == "Random":
        values = random.sample(range(1, 100), size)
    else:
        try:
            values = [int(part) for part in raw_values.replace(",", " ").split()]
        except ValueError:
            st.error("Enter integers separated by spaces or commas.")
            st.stop()
        if not values:
            st.error("Enter at least one integer.")
            st.stop()
        if len(values) > 12:
            st.error("Use 12 values or fewer so the tree stays readable.")
            st.stop()

    tree, skipped = trees.build_binary_search_tree(values)
    st.write("The values were inserted from left to right.")
    tree_vis.render_boxes(values, label="Insertion order")
    if skipped:
        st.write(f"Duplicate values were skipped: {', '.join(str(value) for value in skipped)}.")
    tree_vis.render_binary_tree(tree.root, speed=speed, pause_after=True)
    trees.animate_traversal(tree.root, traversal, speed)
