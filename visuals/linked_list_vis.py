import time

import streamlit as st


def pause(speed):
    if speed != "Instant":
        time.sleep(1 / speed)


def render_linked_list(
    head,
    tail=None,
    pending=None,
    current=None,
    emphasis=None,
    removed=None,
    circular=False,
    doubly=False,
    show_tail=False,
    speed=1,
    pause_after=False,
):
    st.graphviz_chart(
        build_linked_list_dot(
            head,
            tail=tail,
            pending=pending,
            current=current,
            emphasis=emphasis,
            removed=removed,
            circular=circular,
            doubly=doubly,
            show_tail=show_tail,
        )
    )
    if pause_after:
        pause(speed)


def build_linked_list_dot(
    head,
    tail=None,
    pending=None,
    current=None,
    emphasis=None,
    removed=None,
    circular=False,
    doubly=False,
    show_tail=False,
):
    emphasis = emphasis or set()
    removed = removed or set()
    chain = _chain(head, circular)
    chain_ids = {id(node) for node in chain}

    lines = [
        "digraph {",
        "    rankdir=LR;",
        '    bgcolor="white";',
        "    nodesep=0.45;",
        "    ranksep=0.8;",
        "    pad=0.25;",
        "    edge [color=\"#1D3557\", arrowsize=0.8];",
    ]

    for index, node in enumerate(chain):
        lines.append(
            f"    {_nid(node)} [{_node_attrs(_fill(node, current, emphasis, removed), _chain_label(node, index, head, tail, show_tail))}];"
        )

    extras = []
    if pending is not None and id(pending) not in chain_ids:
        extras.append(pending)
    for node in removed:
        if id(node) not in chain_ids and node is not pending:
            extras.append(node)

    for node in extras:
        kind = "unlinked" if node in removed else "new"
        lines.append(
            f"    {_nid(node)} [{_node_attrs(_fill(node, current, emphasis, removed), _plain_label(node.value, kind))}];"
        )

    if not chain:
        lines.append('    headptr [label="head", shape=plaintext, fontsize=16, fontcolor="#111111"];')
        lines.append('    nullnode [label="null", shape=plaintext, fontsize=16, fontcolor="#111111"];')
        lines.append("    headptr -> nullnode;")
        if show_tail:
            lines.append('    tailptr [label="tail", shape=plaintext, fontsize=16, fontcolor="#111111"];')
            lines.append("    tailptr -> nullnode;")
    else:
        for node in chain:
            _append_next(lines, node, head if circular else None, in_chain=True)
        if doubly:
            for node in chain:
                if node.prev is not None:
                    lines.append(
                        f"    {_nid(node)} -> {_nid(node.prev)} [style=dashed, color=\"#5C677D\", constraint=false];"
                    )

    for node in extras:
        _append_next(lines, node, head if circular else None, in_chain=False)
        if doubly and node.prev is not None:
            lines.append(
                f"    {_nid(node)} -> {_nid(node.prev)} [style=dashed, color=\"#5C677D\", constraint=false];"
            )

    lines.append("}")
    return "\n".join(lines)


def _chain(head, circular):
    chain = []
    seen = set()
    node = head
    while node is not None and node not in seen:
        chain.append(node)
        seen.add(node)
        if circular and node.next is head:
            break
        node = node.next
    return chain


def _append_next(lines, node, circular_head, in_chain):
    if node.next is None:
        null_id = f"null{_nid(node)}"
        lines.append(f'    {null_id} [label="null", shape=plaintext, fontsize=16, fontcolor="#111111"];')
        lines.append(f"    {_nid(node)} -> {null_id};")
        return

    attributes = []
    closes_circle = circular_head is not None and node.next is circular_head and in_chain
    if closes_circle:
        attributes.append("constraint=false")
        attributes.append('label="next"')
    attribute_text = f" [{', '.join(attributes)}]" if attributes else ""
    lines.append(f"    {_nid(node)} -> {_nid(node.next)}{attribute_text};")


def _chain_label(node, index, head, tail, show_tail):
    parts = [_escape(node.value), f"[{index}]"]
    marks = []
    if node is head:
        marks.append("head")
    if show_tail and tail is not None and node is tail:
        marks.append("tail")
    if marks:
        parts.append(", ".join(marks))
    return "\\n".join(parts)


def _plain_label(value, kind):
    return "\\n".join([_escape(value), kind])


def _node_attrs(fill, label):
    return (
        f'label="{label}", shape=box, style="filled,rounded", '
        f'fillcolor="{fill}", fontcolor="black", fontname="Helvetica", fontsize=16, '
        f'color="#13315C", penwidth=2'
    )


def _fill(node, current, emphasis, removed):
    if node in removed:
        return "#FF6666"
    if current is not None and node is current:
        return "#99FFCC"
    if node in emphasis:
        return "#00CC66"
    return "#00CCCC"


def _escape(value):
    return str(value).replace("\\", "\\\\").replace('"', '\\"')


def _nid(node):
    return f"n{id(node)}"
