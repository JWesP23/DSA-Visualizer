import sys

sys.path.insert(0, ".")
from algorithms.linked_lists import expected_list
from data_structures.linked_list import CircularLinkedList, DoublyLinkedList, SinglyLinkedList
from visuals.linked_list_vis import build_linked_list_dot


def check(actual, expected, label):
    if actual != expected:
        raise SystemExit(f"{label}: {actual} != {expected}")


def prevs(lst):
    return [(node.value, None if node.prev is None else node.prev.value) for node in lst.nodes()]


def nexts(lst):
    return [(node.value, None if node.next is None else node.next.value) for node in lst.nodes()]


s = SinglyLinkedList()
check(s.to_values(), [], "empty singly")
s.insert_head(1)
s.insert_head(2)
check(s.to_values(), [2, 1], "s head")
s.insert_tail(3)
check(s.to_values(), [2, 1, 3], "s tail")
s.insert_at(1, 9)
check(s.to_values(), [2, 9, 1, 3], "s index")
s.insert_at(4, 8)
check(s.to_values(), [2, 9, 1, 3, 8], "s index end")
s.insert_at(0, 7)
check(s.to_values(), [7, 2, 9, 1, 3, 8], "s index 0")
assert s.insert_at(9, 5) is False
check(s.to_values(), [7, 2, 9, 1, 3, 8], "s bad index")
assert s.delete(9) is True
check(s.to_values(), [7, 2, 1, 3, 8], "s del mid")
assert s.delete(7) is True
check(s.to_values(), [2, 1, 3, 8], "s del head")
assert s.delete(8) is True
check(s.to_values(), [2, 1, 3], "s del tail")
assert s.delete(4) is False
check(s.to_values(), [2, 1, 3], "s del miss")
assert s.search(1) is True
assert s.search(4) is False
s2 = SinglyLinkedList()
s2.insert_tail(4)
assert s2.delete(4) is True
check(s2.to_values(), [], "s del only")
s3 = SinglyLinkedList()
s3.insert_tail(1)
s3.insert_tail(1)
assert s3.delete(1) is True
check(s3.to_values(), [1], "s del first dup")

d = DoublyLinkedList()
for v in [1, 2, 3]:
    d.insert_tail(v)
check(d.to_values(), [1, 2, 3], "d build")
check(prevs(d), [(1, None), (2, 1), (3, 2)], "d prev")
check(nexts(d), [(1, 2), (2, 3), (3, None)], "d next")
assert d.head.value == 1 and d.tail.value == 3
d.insert_head(0)
check(d.to_values(), [0, 1, 2, 3], "d head")
check(prevs(d), [(0, None), (1, 0), (2, 1), (3, 2)], "d prev after head")
assert d.tail.value == 3
d.delete_head()
check(d.to_values(), [1, 2, 3], "d del head")
check(prevs(d)[0], (1, None), "d new head prev")
d.delete_tail()
check(d.to_values(), [1, 2], "d del tail")
assert d.tail.value == 2 and d.tail.next is None
d.delete(1)
check(d.to_values(), [2], "d del value head")
assert d.head is d.tail and d.head.prev is None and d.head.next is None
d.insert_tail(5)
d.insert_tail(6)
d.delete(5)
check(d.to_values(), [2, 6], "d del mid")
check(prevs(d), [(2, None), (6, 2)], "d prev after mid del")
check(nexts(d), [(2, 6), (6, None)], "d next after mid del")
assert d.delete(9) is False
d2 = DoublyLinkedList()
assert d2.delete_head() is False and d2.delete_tail() is False
d2.insert_head(4)
d2.delete_tail()
check(d2.to_values(), [], "d del only via tail")
assert d2.head is None and d2.tail is None


def circle_ok(lst, values):
    check(lst.to_values(), values, f"c values {values}")
    if not values:
        assert lst.head is None and lst.tail is None
        return
    assert lst.head.value == values[0]
    assert lst.tail.value == values[-1]
    assert lst.tail.next is lst.head
    nodes = list(lst.nodes())
    for i, node in enumerate(nodes):
        nxt = nodes[(i + 1) % len(nodes)]
        assert node.next is nxt, (node.value, None if node.next is None else node.next.value, nxt.value)


c = CircularLinkedList()
for v in [1, 2, 3]:
    c.insert_tail(v)
circle_ok(c, [1, 2, 3])
c.insert_head(9)
circle_ok(c, [9, 1, 2, 3])
c.insert_tail(8)
circle_ok(c, [9, 1, 2, 3, 8])
assert c.delete(1) is True
circle_ok(c, [9, 2, 3, 8])
assert c.delete(9) is True
circle_ok(c, [2, 3, 8])
assert c.delete(8) is True
circle_ok(c, [2, 3])
assert c.delete(3) is True
circle_ok(c, [2])
assert c.delete(2) is True
circle_ok(c, [])
c = CircularLinkedList()
c.insert_head(1)
c.insert_head(2)
circle_ok(c, [2, 1])
assert c.delete(4) is False
circle_ok(c, [2, 1])
c.traverse()
circle_ok(c, [2, 1])
CircularLinkedList().traverse()

base = [8, 3, 10, 1]
cases = [
    ("singly", SinglyLinkedList, ["Insert at the head", "Insert at the tail", "Insert at an index", "Delete a value", "Search"]),
    ("doubly", DoublyLinkedList, ["Insert at the head", "Insert at the tail", "Delete the head", "Delete the tail", "Delete a value", "Search"]),
    ("circular", CircularLinkedList, ["Insert at the head", "Insert at the tail", "Delete a value", "Traverse"]),
]
for name, cls, operations in cases:
    for operation in operations:
        for target in (8, 4, 1, 99):
            indexes = [0, 2, 4, 5] if operation == "Insert at an index" else [None]
            for index in indexes:
                lst = cls()
                for value in base:
                    lst.insert_tail(value)
                if operation == "Insert at the head":
                    lst.insert_head(target)
                elif operation == "Insert at the tail":
                    lst.insert_tail(target)
                elif operation == "Insert at an index":
                    lst.insert_at(index, target)
                elif operation == "Delete a value":
                    lst.delete(target)
                elif operation == "Delete the head":
                    lst.delete_head()
                elif operation == "Delete the tail":
                    lst.delete_tail()
                elif operation == "Search":
                    lst.search(target)
                elif operation == "Traverse":
                    lst.traverse()
                check(lst.to_values(), expected_list(base, operation, target, index), f"{name} {operation} t={target} i={index}")
                if name == "doubly" and lst.head is not None:
                    assert lst.head.prev is None
                    assert lst.tail.next is None
                    nodes = list(lst.nodes())
                    assert nodes[0] is lst.head and nodes[-1] is lst.tail
                    for i, node in enumerate(nodes):
                        if i:
                            assert node.prev is nodes[i - 1]
                        if i < len(nodes) - 1:
                            assert node.next is nodes[i + 1]
                if name == "circular":
                    circle_ok(lst, expected_list(base, operation, target, index))

s = SinglyLinkedList()
for v in [4, 5, 6]:
    s.insert_tail(v)
dot = build_linked_list_dot(s.head)
assert "null" in dot and 'label="next"' not in dot
assert "[0]" in dot
d = DoublyLinkedList()
for v in [4, 5, 6]:
    d.insert_tail(v)
ddot = build_linked_list_dot(d.head, tail=d.tail, doubly=True, show_tail=True)
assert ddot.count("style=dashed") == 2
assert "tail" in ddot and "head" in ddot
c = CircularLinkedList()
for v in [4, 5, 6]:
    c.insert_tail(v)
cdot = build_linked_list_dot(c.head, tail=c.tail, circular=True, show_tail=True)
assert cdot.count('label="next"') == 1
assert "null" not in cdot
empty_dot = build_linked_list_dot(None, show_tail=True)
assert "head" in empty_dot and "tail" in empty_dot and "null" in empty_dot
one = CircularLinkedList()
one.insert_head(7)
odot = build_linked_list_dot(one.head, tail=one.tail, circular=True, show_tail=True)
assert 'label="next"' in odot

# step callbacks should not mutate past the final list
frames = []
s = SinglyLinkedList()
for value in [2, 5, 8]:
    s.insert_tail(value)
s.delete(5, on_step=frames.append)
s.insert_at(1, 4, on_step=frames.append)
assert s.to_values() == [2, 4, 8]
assert frames

print("all checks passed")
