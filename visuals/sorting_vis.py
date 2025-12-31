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
def render_merge_step(left, right, speed= 1, separate= True, merge= False):
    graph = graphviz.Digraph()
    graph.attr(rankdir='LR')

    #render whole array without distinguishing left and right
    if not separate:
        whole_array = left + right
        graph.node("array", f"Array | {{ {' | '.join(str(v) for v in whole_array)} }}", shape="record", style="filled", fillcolor="#00CCCC")
    #distinguish left and right using colors
    else:
        graph.node("left", f"Left | {{ {' | '.join(str(v) for v in left)} }}", shape= "record", style= "filled", fillcolor= "#99FFCC")
        graph.node("right", f"Right | {{ {' | '.join(str(v) for v in right)} }}", shape= "record", style= "filled", fillcolor= "#66CCFF")

    #indicate a merge (with a label and bidirectional link) between left and right side arrays
    if merge:
        graph.edge("left", "right", dir= "both", label= "merge", color= "gray")
    #indicate a non-directional link between left and right side arrays
    elif separate:
        graph.edge("left", "right", dir= "none", color= "gray")

    st.graphviz_chart(graph)

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

    #For empty arrays do not attempt to graph
    if array_length == 0:
        return

    heap = graphviz.Digraph()

    #Return appropriate color for node depending on index
    def node_color(index):
        if highlight_indices and index in highlight_indices:
            return "#99FFCC"
        elif swap_indices and index in swap_indices:
            return "#00CC66"
        return "#00CCCC"

    #Create nodes
    for i, val in enumerate(array):
        heap.node(
            name=f"node_{i}",
            label=f"{val}",
            style="filled",
            fillcolor=node_color(i),
            fontcolor="black"
        )

    #Create edges
    for parent_index in range(array_length):
        left_child = 2 * parent_index + 1
        right_child = 2 * parent_index + 2

        if left_child < array_length:
            heap.edge(f"node_{parent_index}", f"node_{left_child}")
        if right_child < array_length:
            heap.edge(f"node_{parent_index}", f"node_{right_child}")

    st.graphviz_chart(heap)

    if speed != "Instant":
        time.sleep(1 / speed)
