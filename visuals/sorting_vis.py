import time
import streamlit as st
import matplotlib.pyplot as plt
import random

def generate_array(size):
    array = [random.randint(-100, 100) for _ in range(size)]
    return array


def render_array(array, highlight_indices= None, swap_indices= None, speed= 1, label= None):
    boxes = ""
    for i, val in enumerate(array):
        if swap_indices and i in swap_indices:
            color = "#00CC66"
        elif highlight_indices and i in highlight_indices:
            color = "#99FFCC"
        else:
            color = "#00CCCC"
        boxes += f"<div class='box' style='background-color:{color}'>{val}</div>"

    label_html = f"<div class='array-label'>{label}</div>" if label else ""

    st.markdown(
        f"""
        <style>
        .array-container {{
            white-space: nowrap;  /* keeps boxes on one line */
            overflow-x: auto;      /* allows scrolling if too wide */
            padding: 10px 0;
        }}
        .box {{
            display: inline-block;
            width: 50px;
            height: 50px;
            line-height: 50px;
            border: 2px solid #FFFFFF;
            color: #000000;
            text-align: center;
            margin: 2px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 20px;
        }}
        </style>
        {label_html}
        <div class="array-container">{boxes}</div>
        """,
        unsafe_allow_html=True
    )

    if speed != "Instant":
        time.sleep(1 / speed)

def render_array_with_pivot(array, highlight_indices= None, swap_indices= None, pivot_index= None, speed= 1, label= None):
    boxes = ""
    for i, val in enumerate(array):
        if highlight_indices and i in highlight_indices:
            color = "#99FFCC"
        elif swap_indices and i in swap_indices:
            color = "#00CC66"
        elif pivot_index is not None and i == pivot_index:
            color = "#4895EF"
        else:
            color = "#00CCCC"
        boxes += f"<div class='box' style='background-color:{color}'>{val}</div>"

    label_html = f"<div class='array-label'>{label}</div>" if label else ""

    st.markdown(
        f"""
        <style>
        .array-container {{
            white-space: nowrap;  /* keeps boxes on one line */
            overflow-x: auto;      /* allows scrolling if too wide */
            padding: 10px 0;
        }}
        .box {{
            display: inline-block;
            width: 50px;
            height: 50px;
            line-height: 50px;
            border: 2px solid #FFFFFF;
            color: #000000;
            text-align: center;
            margin: 2px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 20px;
        }}
        </style>
        {label_html}
        <div class="array-container">{boxes}</div>
        """,
        unsafe_allow_html=True
    )

    if speed != "Instant":
        time.sleep(1 / speed)

#For rendering side by side arrays, not capable of highlighting specific indexes with arrays
def render_merge_step(left, right, speed=1, separate=True, merge=False):
    #start building the DOT string
    dot = "digraph {\n"
    dot += "    rankdir=LR;\n"  # left-to-right layout

    if not separate:
        #render whole array without distinguishing left and right
        whole_array = left + right
        label = "Array | { " + " | ".join(str(v) for v in whole_array) + " }"
        dot += f'    array [label="{label}", shape=record, style=filled, fillcolor="#00CCCC"];\n'
    else:
        #distinguish left and right using colors
        dot += f'    left [label="Left | {{ {" | ".join(str(v) for v in left)} }}", shape=record, style=filled, fillcolor="#99FFCC"];\n'
        dot += f'    right [label="Right | {{ {" | ".join(str(v) for v in right)} }}", shape=record, style=filled, fillcolor="#66CCFF"];\n'

        #indicate a merge (with a label and bidirectional link) between left and right side arrays
        if merge:
            dot += '    left -> right [dir=both, label="merge", color="gray"];\n'
        #indicate a non-directional link between left and right side arrays
        else:
            dot += '    left -> right [dir=none, color="gray"];\n'

    dot += "}"  # close the digraph

    #render the DOT string with Streamlit
    st.graphviz_chart(dot)

    if speed != "Instant":
        time.sleep(1 / speed)



#similar to render_array but differentiates the heap with a dashed border for boxes and with a heap label
def render_heap(array, highlight_indices= None, swap_indices= None, speed= 1):
    boxes = ""
    for i, val in enumerate(array):
        if highlight_indices and i in highlight_indices:
            color = "#99FFCC"
        elif swap_indices and i in swap_indices:
            color = "#00CC66"
        else:
            color = "#00CCCC"
        boxes += f"<div class='heap-box' style='background-color:{color}'>{val}</div>"
    st.markdown(
        f"""
        <style>
        .heap-container {{
            white-space: nowrap;  /* keeps boxes on one line */
            overflow-x: auto;      /* allows scrolling if too wide */
            padding: 10px 0;
        }}
        .heap-box {{
            display: inline-block;
            width: 50px;
            height: 50px;
            line-height: 50px;
            border: 2px dashed #FFFFFF;
            color: #000000;
            text-align: center;
            margin: 2px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 20px;
        }}
        </style>
        <div style='background-color:##00CCCC; padding:4px; border-radius:6px; display:inline-block; font-weight:bold;'>Heap:</div>
        <div class="heap-container">{boxes}</div>
        """,
        unsafe_allow_html=True
    )

    if speed != "Instant":
        time.sleep(1 / speed)



#renders a tree from an array heap, capable of highlighting specific indices
def render_heap_tree(array, highlight_indices= None, swap_indices= None, speed= 1):
    array_length = len(array)

    #for empty arrays do not attempt to graph
    if array_length == 0:
        return

    #return appropriate color for node depending on index
    def node_color(index):
        if highlight_indices and index in highlight_indices:
            return "#99FFCC"
        elif swap_indices and index in swap_indices:
            return "#00CC66"
        return "#00CCCC"

    #start DOT string
    dot = "digraph {\n"
    dot += "    rankdir=TB;\n"  # top-to-bottom layout
    dot += "    node [style=filled, fontcolor=black];\n"

    #create nodes
    for i, val in enumerate(array):
        color = node_color(i)
        dot += f'    node_{i} [label="{val}", fillcolor="{color}"];\n'

    #create edges for parent -> children
    for parent_index in range(array_length):
        left_child = 2 * parent_index + 1
        right_child = 2 * parent_index + 2

        if left_child < array_length:
            dot += f'    node_{parent_index} -> node_{left_child};\n'
        if right_child < array_length:
            dot += f'    node_{parent_index} -> node_{right_child};\n'

    dot += "}"  #close digraph

    #render in Streamlit
    st.graphviz_chart(dot)

    if speed != "Instant":
        time.sleep(1 / speed)