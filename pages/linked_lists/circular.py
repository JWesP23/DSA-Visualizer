import streamlit as st

from algorithms import linked_lists

st.title("Circular Lists")

st.write(
    "Circular lists are singly or doubly linked lists where the last node points back at the first node. " \
    "Unlike in a regular linked lists, there is no null at the end of a non-empty circular list. "
    "This page uses a singly linked circular list, meaning each node has a next pointer, no nodes have previous pointers, and the list keeps both a head and a tail pointer. "
    "The tail's next pointer is the head. A one-node list points at itself."
    "Circular lists are often used for implementing queues, since it is easy to add to the tail and remove from the head in O(1) time. "
)

operation = st.selectbox("Choose an operation", linked_lists.CIRCULAR_OPERATIONS)
uses_value = operation in linked_lists.VALUE_OPERATIONS
demo = linked_lists.read_demo_inputs(operation, uses_value=uses_value, uses_index=False)

match operation:
    case "Insert at the head":
        st.write(
            "Insert at the head points the new node at the old head, points the tail at the new node so the circle stays closed, and then moves the head pointer to the new node. "
            "The runtime for this is O(1)."
        )
    case "Insert at the tail":
        st.write(
            "Insert at the tail points the new node at the old head, points the previous tail at the new node, and then moves the tail pointer to the new node. "
            "The runtime for this is O(1)."
        )
    case "Delete a value":
        st.write(
            "Delete walks from the head and stops if it returns to the head without a match. "
            "The first match is unlinked. Removing the head or the tail also updates that pointer so the remaining nodes still form a circle. "
            "Finding the node is O(n)."
        )
    case "Traverse":
        st.write(
            "A traversal follows each next pointer until it completes one full loop around the circle. It visits the head, traverses until the next node would be the head again, and then stops. "
            "Each node is visited once, so one lap is O(n)."
        )

st.write(
    "Cyan nodes are in the list. Light green is the node the operation is on. "
)
st.write(
    "Green is a node that was just inserted or found. Red is a node that was just unlinked. "
)
st.write(
    "Solid arrows are next pointers. "
)
st.write(
    "The head and tail nodes are marked. "
)
st.write(
    "Null appears only when the list is empty."
)
st.write(
    "The label under a linked value is its index, remember that linked lists don't typically store indices, they are just there to support your understanding. "
)

if st.button("Run"):
    values, target, index = linked_lists.resolve_demo(demo, operation, uses_value=uses_value, uses_index=False)
    linked_lists.animate_circular(values, operation, demo["speed"], target=target, index=index)
