import random

import streamlit as st

from algorithms import trees
from visuals import tree_vis

SAMPLE_WORDS = ["cat", "car", "card", "dog", "dot", "dove"]

st.title("Tries")

st.write(
    "A trie stores strings one character at a time. Words that share a prefix share the nodes for that prefix. "
    "Insert and search both iterate through the input character by character. They start at the root, and try to find if their path exists. " \
    "Therefore, insert and search both run in O(k) for a word of length k."
)

operation = st.selectbox("Choose an operation", ["Insert", "Search"])
source = st.radio(
    "Which words go in the trie?",
    ["Random", "Custom"],
    captions=[
        "Pick several words from a small dictionary",
        "Type your own words",
    ],
)

if source == "Random":
    word_count = st.slider("Number of words", 3, len(SAMPLE_WORDS), 4)
    st.write(f"Random words are drawn from: {', '.join(SAMPLE_WORDS)}.")
else:
    raw_words = st.text_input("Words", "cat, car, card, dog")

if operation == "Search":
    target = st.text_input("Word to search for", "car")

speed = st.selectbox("Animation speed", [1, 2, 3, 4, 5, "Instant"])

match operation:
    case "Insert":
        st.write(
            "Insert walks the word from the root. If the next character is missing, the trie adds a node. "
            "The last character is marked as the end of a word, so a prefix such as \"car\" can be a word even when \"card\" continues past it."
        )
    case "Search":
        st.write(
            "Search follows the characters of the word. If an edge is missing, the word is not in the trie. "
            "If the path exists but the last node is not marked as the end of a word, the letters are only a prefix."
        )

st.write("Light green is the current node. Green nodes are on the path of the current word. Blue nodes with a double outline end a word.")

if st.button("Run"):
    if source == "Random":
        words = random.sample(SAMPLE_WORDS, word_count)
    else:
        words = [part.strip().lower() for part in raw_words.replace(",", " ").split() if part.strip()]
        if not words:
            st.error("Enter at least one word.")
            st.stop()
        if any(not word.isalpha() for word in words):
            st.error("Use letters only. Separate words with spaces or commas.")
            st.stop()
        if len(words) > 8 or any(len(word) > 10 for word in words):
            st.error("Use 8 words or fewer, with each word at most 10 letters.")
            st.stop()

    if operation == "Insert":
        st.write("Insert each word from left to right.")
        tree_vis.render_boxes(words, label="Words")
        trees.animate_trie_inserts(words, speed)
    else:
        query = target.strip().lower()
        if not query.isalpha():
            st.error("The search word should contain letters only.")
            st.stop()
        trees.animate_trie_search(words, query, speed)
