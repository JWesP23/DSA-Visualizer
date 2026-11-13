import random

import streamlit as st

from data_structures.linked_list import CircularLinkedList, DoublyLinkedList, SinglyLinkedList
from visuals import linked_list_vis

SINGLY_OPERATIONS = [
    "Insert at the head",
    "Insert at the tail",
    "Insert at an index",
    "Delete a value",
    "Search",
]

DOUBLY_OPERATIONS = [
    "Insert at the head",
    "Insert at the tail",
    "Delete the head",
    "Delete the tail",
    "Delete a value",
    "Search",
]

CIRCULAR_OPERATIONS = [
    "Insert at the head",
    "Insert at the tail",
    "Delete a value",
    "Traverse",
]

VALUE_OPERATIONS = {
    "Insert at the head",
    "Insert at the tail",
    "Insert at an index",
    "Delete a value",
    "Search",
}

SINGLY_CLOSINGS = {
    "Insert at the head": "Only the new node's next pointer and the head pointer change, so inserting at the head is O(1).",
    "Insert at the tail": "Linking the new node is one pointer update, but finding the tail walks from the head. Without a tail pointer, inserting at the tail is O(n).",
    "Insert at an index": "The walk to the insertion point looks at up to n nodes, so inserting at an index is O(n). Index 0 is the special case that only moves the head.",
    "Delete a value": "Finding the value is O(n). Unlinking it is one pointer update. The previous node has to be remembered, because there is no prev pointer.",
    "Search": "Search walks from the head until it finds the value or reaches null, so it is O(n).",
}

DOUBLY_CLOSINGS = {
    "Insert at the head": "The new node, the old head's prev pointer, and the head pointer change. Inserting at the head is O(1).",
    "Insert at the tail": "The tail pointer reaches the last node without a walk, so inserting at the tail is O(1).",
    "Delete the head": "Head moves one node forward and the new head's prev pointer is cleared. Deleting the head is O(1).",
    "Delete the tail": "Tail moves one node backward and the new tail's next pointer is cleared. Deleting the tail is O(1).",
    "Delete a value": "Finding the value is O(n). Once it is found, the prev and next pointers unlink it in O(1).",
    "Search": "Search follows next from the head, so it is O(n). The prev pointers are not needed for this walk.",
}

CIRCULAR_CLOSINGS = {
    "Insert at the head": "The new node, the tail's next pointer, and the head pointer change. Inserting at the head is O(1).",
    "Insert at the tail": "The new node, the old tail's next pointer, and the tail pointer change. Inserting at the tail is O(1).",
    "Delete a value": "Finding the value may walk the whole circle, so deleting a value is O(n). The tail pointer moves when the tail itself is the node removed.",
    "Traverse": "One lap visits each node once and stops when next returns to the head, so a traversal is O(n).",
}

SINGLY_VIEW = {"circular": False, "doubly": False, "show_tail": False}
DOUBLY_VIEW = {"circular": False, "doubly": True, "show_tail": True}
CIRCULAR_VIEW = {"circular": True, "doubly": False, "show_tail": True}


def read_demo_inputs(operation, uses_value, uses_index):
    source = st.radio(
        "How should the list start?",
        ["Random", "Custom"],
        captions=[
            "Build a short list of distinct integers",
            "Type the starting values yourself",
        ],
    )
    size = None
    raw_values = ""
    target = None
    index = None
    if source == "Random":
        size = st.slider("Number of starting nodes", 3, 7, 5)
        if uses_value and operation in ("Delete a value", "Search"):
            st.write("Random delete and search pick a value that is already in the list.")
        elif uses_value:
            st.write("Random insert picks a value from 1 to 40. It may already be in the list.")
        if uses_index:
            st.write("The index is chosen from 0 through the length of the list. The last of those inserts at the tail.")
    else:
        raw_values = st.text_input("Starting values", "8, 3, 10, 1, 6")
        if uses_value:
            target = int(st.number_input("Value", min_value=-100, max_value=100, value=4, step=1))
        if uses_index:
            index = int(st.number_input("Index", min_value=0, max_value=8, value=0, step=1))
            st.write("Index 0 inserts at the head. An index equal to the length of the list inserts at the tail.")
    speed = st.selectbox("Animation speed", [1, 2, 3, 4, 5, "Instant"])
    return {
        "source": source,
        "size": size,
        "raw_values": raw_values,
        "target": target,
        "index": index,
        "speed": speed,
    }


def resolve_demo(demo, operation, uses_value, uses_index):
    if demo["source"] == "Random":
        values = random.sample(range(1, 50), demo["size"])
        target = None
        index = None
        if uses_value:
            if operation in ("Delete a value", "Search") and values:
                target = random.choice(values)
            else:
                target = random.randint(1, 40)
        if uses_index:
            index = random.randint(0, len(values))
        return values, target, index

    values = parse_int_list(demo["raw_values"])
    if values is None:
        st.error("Enter integers separated by spaces or commas.")
        st.stop()
    if len(values) > 8:
        st.error("Use 8 values or fewer so the diagram stays readable.")
        st.stop()
    if uses_index and demo["index"] > len(values):
        st.error(
            f"Index {demo['index']} is past the end of a list of length {len(values)}. "
            f"Use an index from 0 through {len(values)}."
        )
        st.stop()
    return values, demo["target"], demo["index"]


def parse_int_list(raw):
    text = raw.strip()
    if not text:
        return []
    try:
        return [int(part) for part in text.replace(",", " ").split()]
    except ValueError:
        return None


def animate_singly(values, operation, speed, target=None, index=None):
    actions = {
        "Insert at the head": lambda lst, on_step: lst.insert_head(target, on_step=on_step),
        "Insert at the tail": lambda lst, on_step: lst.insert_tail(target, on_step=on_step),
        "Insert at an index": lambda lst, on_step: lst.insert_at(index, target, on_step=on_step),
        "Delete a value": lambda lst, on_step: lst.delete(target, on_step=on_step),
        "Search": lambda lst, on_step: lst.search(target, on_step=on_step),
    }
    _run(SinglyLinkedList, values, operation, target, index, speed, SINGLY_VIEW, SINGLY_CLOSINGS[operation], actions[operation])


def animate_doubly(values, operation, speed, target=None, index=None):
    actions = {
        "Insert at the head": lambda lst, on_step: lst.insert_head(target, on_step=on_step),
        "Insert at the tail": lambda lst, on_step: lst.insert_tail(target, on_step=on_step),
        "Delete the head": lambda lst, on_step: lst.delete_head(on_step=on_step),
        "Delete the tail": lambda lst, on_step: lst.delete_tail(on_step=on_step),
        "Delete a value": lambda lst, on_step: lst.delete(target, on_step=on_step),
        "Search": lambda lst, on_step: lst.search(target, on_step=on_step),
    }
    _run(DoublyLinkedList, values, operation, target, index, speed, DOUBLY_VIEW, DOUBLY_CLOSINGS[operation], actions[operation])


def animate_circular(values, operation, speed, target=None, index=None):
    actions = {
        "Insert at the head": lambda lst, on_step: lst.insert_head(target, on_step=on_step),
        "Insert at the tail": lambda lst, on_step: lst.insert_tail(target, on_step=on_step),
        "Delete a value": lambda lst, on_step: lst.delete(target, on_step=on_step),
        "Traverse": lambda lst, on_step: lst.traverse(on_step=on_step),
    }
    _run(CircularLinkedList, values, operation, target, index, speed, CIRCULAR_VIEW, CIRCULAR_CLOSINGS[operation], actions[operation])


def expected_list(values, operation, target=None, index=None):
    data = list(values)
    if operation == "Insert at the head":
        data.insert(0, target)
    elif operation == "Insert at the tail":
        data.append(target)
    elif operation == "Insert at an index":
        if index is not None and 0 <= index <= len(data):
            data.insert(index, target)
    elif operation == "Delete a value":
        if target in data:
            data.remove(target)
    elif operation == "Delete the head":
        if data:
            data.pop(0)
    elif operation == "Delete the tail":
        if data:
            data.pop()
    return data


def _run(factory, values, operation, target, index, speed, view, closing, mutate):
    lst = factory()
    for value in values:
        lst.insert_tail(value)

    shown = ", ".join(str(value) for value in values) if values else "empty"
    st.write(f"Starting values: {shown}.")
    if operation in VALUE_OPERATIONS:
        st.write(f"Value for this operation: {target}.")
    if operation == "Insert at an index":
        st.write(f"Index for this operation: {index}.")
    if values:
        st.write("Here is the list before the operation. The number under each value is that node's index.")
    else:
        st.write("The list starts empty. The head pointer is null.")
    _draw(lst, speed, view)

    def on_step(frame):
        st.write(frame["message"])
        _draw(lst, speed, view, frame)

    mutate(lst, on_step)

    actual = lst.to_values()
    expected = expected_list(values, operation, target, index)
    if actual != expected:
        raise RuntimeError(f"{operation} produced {actual}, expected {expected}.")

    result = ", ".join(str(value) for value in actual) if actual else "empty"
    st.write(f"Done. The list from the head is: {result}.")
    _draw(lst, speed, view, pause_after=False)
    st.write(closing)


def _draw(lst, speed, view, frame=None, pause_after=True):
    frame = frame or {}
    linked_list_vis.render_linked_list(
        lst.head,
        tail=lst.tail if view["show_tail"] else None,
        pending=frame.get("pending"),
        current=frame.get("current"),
        emphasis=frame.get("emphasis"),
        removed=frame.get("removed"),
        circular=view["circular"],
        doubly=view["doubly"],
        show_tail=view["show_tail"],
        speed=speed,
        pause_after=pause_after,
    )
