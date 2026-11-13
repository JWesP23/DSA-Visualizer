import streamlit as st

from algorithms import linked_lists

st.title("Singly Linked Lists")

st.write(
    "A singly linked list is similar to an array in that it stores a linear collection of elements. " \
    "However, linked lists link elements together using pointers to create a chain of nodes rather than using indices to represent proximity in memory. " \
    "Each node stores a value and a pointer to the next node, the final node (the \"tail\" node) points to a null value. "
    "The list object itself is often just a pointer to the first node (the \"head\" node). "
    "In a singly linked list, there is no pointer back to the previous node, so to get to a desired element, you have to traverse the length of the list up to that element. " \
    "You cannot just use the index to jump to the element like you can with an array. " \
    "This makes some operations slower than they are for arrays, and some operations faster. " \
)

operation = st.selectbox("Choose an operation", linked_lists.SINGLY_OPERATIONS)
uses_index = operation == "Insert at an index"
demo = linked_lists.read_demo_inputs(operation, uses_value=True, uses_index=uses_index)

match operation:
    case "Insert at the head":
        st.write(
            "Inserting at the head involves pointing the new node at the former head node, and setting the head pointer to point at the new node. "
            "This happens exactly this way no matter how many nodes are in the list, so insertion at the head is O(1). "
        )
    case "Insert at the tail":
        st.write(
            "Inserting at the tail traverses the entire list until finding the tail node which points at null, " \
            "then you point the former tail at the new node. "
            "This makes the operation O(n), because you must visit every node in the list to find the tail node. " \
            "However, some implementations will keep a pointer to the tail node just as with the head. " \
            "In this case, the operation would be O(1). "
        )
    case "Insert at an index":
        st.write(
            "Insert at an index traverses to the node just before that index, points the new node at the node that comes next, "
            "and then points the previous node at the new node. In the worst case, this requires traversal of the whole list so the runtime is O(n). " \
            "Remember, linked lists don't typically store indices, the way the index is determined is just by incrementing a counter in the algorithm of the number of nodes visited. "
        )
    case "Delete a value":
        st.write(
            "Deleting traverses from the head until it finds the node containing the value to delete. " \
            "At each step, it saves the previous node. "
            "It then points the previous node to the node after the node to be removed and then deletes the node to be removed. " \
            "If there are multiple nodes in the list with the desire value to be deleted, typically only the first match gets removed. " \
            "However, you could modify the algorithm by not exiting after the first match is deleted. "
            "If the value to delete is the head, the head node is deleted and the head pointer moves to the node the prior head pointed to. " \
            "In the worst case, deleting requires traversing the whole list, so the runtime is O(n). "
        )
    case "Search":
        st.write(
            "Search starts at the head and traverses the list while checking if the value of each node matches the value being searched for. " \
            "If the value is found, the search returns the node that contains the value or returns True. " \
            "If the value is not in the list, the search will return None or Falsewhen it reaches the tail (the node that points at null). "
            "In the worst case, whether or not the value is in the list, we traverse every node in the list, so the runtime is O(n). "
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
    "The head node is marked. "
)
st.write(
    "The label under a linked value is its index, remember that linked lists don't typically store indices, they are just there to support your understanding. "
)

if st.button("Run"):
    values, target, index = linked_lists.resolve_demo(demo, operation, uses_value=True, uses_index=uses_index)
    linked_lists.animate_singly(values, operation, demo["speed"], target=target, index=index)
