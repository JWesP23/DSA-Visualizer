import streamlit as st

from algorithms import linked_lists

st.title("Doubly Linked Lists")

st.write(
    "Doubly linked lists give every node two pointers, one pointing ahead of it and one pointing behind it. "
    "They also tend to keep a tail pointer alongside the head pointer, so either end can change without traversing the whole length of the list. "
    "You can traverse a doubly linked list in either direction (head to tail or tail to head)."
    "The head's previous pointer and the tail's next pointer are null."
)

operation = st.selectbox("Choose an operation", linked_lists.DOUBLY_OPERATIONS)
uses_value = operation in linked_lists.VALUE_OPERATIONS
demo = linked_lists.read_demo_inputs(operation, uses_value=uses_value, uses_index=False)

match operation:
    case "Insert at the head":
        st.write(
            "Inserting at the head involves pointing the new node's next pointer at the former head node, the former head node's previous pointer at the new node, "
            "and setting the head pointer to point at the new node. "
            "This happens exactly this way no matter how many nodes are in the list, so insertion at the head is O(1). "
        )
    case "Insert at the tail":
        st.write(
            "Inserting at the tail involves pointing the new node's previous pointer at the former tail node, the former tail node's next pointer at the new node, "
            "and setting the tail pointer to point at the new node. "
            "This happens exactly this way no matter how many nodes are in the list, so insertion at the tail is O(1). "
        )
    case "Delete the head":
        st.write(
            "Deleting the head moves the head pointer to the next node and clears that node's prev pointer. " \
            "You then delete the former head node. "
            "If the list only has one node, tail becomes null too. The runtime is O(1)."
        )
    case "Delete the tail":
        st.write(
            "Deleting the tail moves the tail pointer to the current tail'sprevious node and clearing that node's next pointer. "
            "You then delete the former tail node. "
            "The tail pointer is what makes the end of the list reachable in O(1) just like the head."
        )
    case "Delete a value":
        st.write(
            "Deleting involves traversing from the head until it finding the first match. "
            "Each node points at its own previous and next nodes, so you don't need to track the previous node like you do with a singly linked list ." \
            "You can just point the previous node at the next node and the next node at the previous node, then delete the current node. "
            "The search runs in O(n), and the pointer swapping is O(1)."
        )
    case "Search":
        st.write(
            "Search traverses node-by-node from the head. In the worst case (the value is not in the list or is at the end), " \
            "we traverse the whole list. So the runtime is O(n)."
        )

st.write(
    "Cyan nodes are in the list. Light green is the node the operation is on. "
)
st.write(
    "Green is a node that was just inserted or found. Red is a node that was just unlinked. "
)
st.write(
    "Solid arrows are next pointers and dashed arrows are previous pointers. "
)
st.write(
    "The head and tail nodes are marked. "
)
st.write(
    "The label under a linked value is its index, remember that linked lists don't typically store indices, they are just there to support your understanding. "
)

if st.button("Run"):
    values, target, index = linked_lists.resolve_demo(demo, operation, uses_value=uses_value, uses_index=False)
    linked_lists.animate_doubly(values, operation, demo["speed"], target=target, index=index)
