import time
import streamlit as st

def pause(speed):
    if speed != "Instant":
        time.sleep(1 / speed)

def render_boxes(values, highlight_indices=None, emphasize_indices=None, speed=1, label=None, pause_after=False):
    boxes = ""
    for index, value in enumerate(values):
        if emphasize_indices and index in emphasize_indices:
            color = "#00CC66"
        elif highlight_indices and index in highlight_indices:
            color = "#99FFCC"
        else:
            color = "#00CCCC"
        boxes += f"<div class='box' style='background-color:{color}'>{value}</div>"

    label_html = f"<div class='array-label'>{label}</div>" if label else ""

    st.markdown(
        f"""
        <style>
        .array-label {{
            font-weight: bold;
            margin-top: 8px;
        }}
        .array-container {{
            white-space: nowrap;
            overflow-x: auto;
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
        unsafe_allow_html=True,
    )

    if pause_after:
        pause(speed)


def render_binary_tree(root, current=None, visited=None, speed=1, pause_after=False):
    _render_binary(
        root,
        lambda node: _binary_color(node, current, visited),
        lambda node: "black",
        speed,
        pause_after,
    )


def render_red_black_tree(root, focus=None, speed=1, pause_after=False):
    focus = set(focus or [])

    def fill(node):
        if node.color == "red":
            return "#E63946"
        return "#1D1D1D"

    def font(node):
        return "white"

    def border(node):
        if node in focus:
            return "#FFD60A", 5
        return "#FFFFFF", 2

    _render_binary(root, fill, font, speed, pause_after, border_for=border)


def render_trie(root, current=None, path=None, speed=1, pause_after=False):
    if root is None:
        return

    path = set(path or [])
    lines = [
        "digraph {",
        "    rankdir=TB;",
        "    nodesep=0.35;",
        "    ranksep=0.55;",
        '    graph [ordering="out"];',
        "    node [style=filled, fontname=Helvetica, fontsize=16, shape=circle];",
    ]

    nodes = []
    _collect_trie(root, nodes)
    for node in nodes:
        fill, font = _trie_style(node, root, current, path)
        extra = ", peripheries=2" if node.is_end and node is not root else ""
        label = "root" if node is root else node.char
        lines.append(
            f'    {_node_id(node)} [label="{label}", fillcolor="{fill}", fontcolor="{font}"{extra}];'
        )

    _append_trie_edges(root, lines)
    lines.append("}")
    st.graphviz_chart("\n".join(lines))

    if pause_after:
        pause(speed)


def _render_binary(root, fill_for, font_for, speed, pause_after, border_for=None):
    if root is None:
        st.write("The tree is empty.")
        return

    lines = [
        "digraph {",
        "    rankdir=TB;",
        "    nodesep=0.4;",
        "    ranksep=0.55;",
        '    graph [ordering="out"];',
        "    node [style=filled, fontname=Helvetica, fontsize=16];",
    ]
    nodes = []
    _collect_binary(root, nodes)
    for node in nodes:
        if border_for is None:
            border = ""
        else:
            color, width = border_for(node)
            border = f', color="{color}", penwidth={width}'
        lines.append(
            f'    {_node_id(node)} [label="{node.value}", fillcolor="{fill_for(node)}", fontcolor="{font_for(node)}"{border}];'
        )

    null_ids = []
    _append_binary_edges(root, lines, null_ids)
    lines.append("}")
    st.graphviz_chart("\n".join(lines))

    if pause_after:
        pause(speed)


def _binary_color(node, current, visited):
    if current is not None and node is current:
        return "#99FFCC"
    if visited and node in visited:
        return "#00CC66"
    return "#00CCCC"


def _trie_style(node, root, current, path):
    if current is not None and node is current:
        return "#99FFCC", "black"
    if node in path:
        return "#00CC66", "black"
    if node.is_end and node is not root:
        return "#4CC9F0", "black"
    return "#00CCCC", "black"


def _collect_binary(node, found):
    if node is None:
        return
    found.append(node)
    _collect_binary(node.left, found)
    _collect_binary(node.right, found)


def _append_binary_edges(node, lines, null_ids):
    if node is None:
        return
    if node.left is None and node.right is None:
        return

    parent = _node_id(node)
    if node.left is not None:
        lines.append(f"    {parent} -> {_node_id(node.left)};")
    else:
        _append_invisible_child(parent, lines, null_ids)

    if node.right is not None:
        lines.append(f"    {parent} -> {_node_id(node.right)};")
    else:
        _append_invisible_child(parent, lines, null_ids)

    _append_binary_edges(node.left, lines, null_ids)
    _append_binary_edges(node.right, lines, null_ids)


def _append_invisible_child(parent, lines, null_ids):
    # Keeps a single child on the correct side of its parent.
    null_id = f"null{len(null_ids)}"
    null_ids.append(null_id)
    lines.append(f"    {null_id} [label=\"\", style=invis, width=0, height=0, fixedsize=true];")
    lines.append(f"    {parent} -> {null_id} [style=invis];")


def _collect_trie(node, found):
    found.append(node)
    for char in sorted(node.children):
        _collect_trie(node.children[char], found)


def _append_trie_edges(node, lines):
    for char in sorted(node.children):
        child = node.children[char]
        lines.append(f"    {_node_id(node)} -> {_node_id(child)};")
        _append_trie_edges(child, lines)


def _node_id(node):
    return f"n{id(node)}"
