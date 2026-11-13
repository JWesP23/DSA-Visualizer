import streamlit as st

st.set_page_config(page_title="DSA Visualizer", page_icon="./screenshots/DSA_Visualizer_Favicon.png")

pages = {
    "": [
        st.Page("pages/home.py", title="Home", default=True),
        st.Page("pages/1_Sorting_Algorithms.py", title="Sorting Algorithms"),
        st.Page("pages/2_Searching_Algorithms.py", title="Searching Algorithms"),
    ],
    "Linked Lists": [
        st.Page("pages/linked_lists/singly.py", title="Singly Linked Lists", url_path="singly-linked-lists"),
        st.Page("pages/linked_lists/doubly.py", title="Doubly Linked Lists", url_path="doubly-linked-lists"),
        st.Page("pages/linked_lists/circular.py", title="Circular Lists", url_path="circular-lists"),
    ],
    "Stacks and Queues": [
        st.Page("pages/stacks_and_queues/stacks.py", title="Stacks", url_path="stacks"),
        st.Page("pages/stacks_and_queues/queues.py", title="Queues", url_path="queues"),
        st.Page("pages/stacks_and_queues/priority_queues.py", title="Priority Queues", url_path="priority-queues"),
    ],
    "Trees": [
        st.Page("pages/trees/binary_trees.py", title="Binary Trees", url_path="binary-trees"),
        st.Page("pages/trees/tries.py", title="Tries", url_path="tries"),
        st.Page("pages/trees/red_black_trees.py", title="Red-Black Trees", url_path="red-black-trees"),
    ],
    "Graphs": [
        st.Page("pages/4_Graph_Algorithms.py", title="Graph Algorithms"),
    ],
}

page = st.navigation(pages)
page.run()
