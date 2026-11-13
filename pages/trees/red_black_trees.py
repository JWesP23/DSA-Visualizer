import random

import streamlit as st

from algorithms import trees
from visuals import tree_vis

st.title("Red-Black Trees")

st.write(
    "A red-black tree is a binary search tree that auto-balances itself by "
    "recoloring nodes and rotating after each insert. "
    "Red-black trees follow these 4 rules:"
)
st.markdown(
    """
    1. Every node is red or black.
    2. The root is black.
    3. A red node cannot have red children (no adjacent red nodes).
    4. Every path from a node down to an empty leaf has the same number of black nodes (empty leaves count as black, and they are not drawn).
    """
)

st.write(
    "Each value is inserted as a red leaf in binary-search-tree order. "
    "If its parent is black, the tree is already valid. "
    "However, if its parent is red, what happens depends on the uncle "
    "(the parent's sibling):"
)
st.markdown(
    """
- **Uncle is red:** invert the colors of the parent, uncle, and grandparent. The parent and uncle become black, and the grandparent becomes red.
- **Uncle is black:** rotate until the red-red pair is gone.
"""
)

st.write("Inserting and searching is the same as a binary search tree, O(log n).")

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
    raw_values = st.text_input("Values", "10, 20, 30, 15, 25, 5, 1")

speed = st.selectbox("Animation speed", [1, 2, 3, 4, 5, "Instant"])

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

    st.write("The values are inserted from left to right.")
    tree_vis.render_boxes(values, label="Insertion order")
    trees.animate_red_black_inserts(values, speed)
