class ListNode:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


def _step(on_step, message, pending=None, current=None, emphasis=None, removed=None):
    if on_step is None:
        return
    on_step(
        {
            "message": message,
            "pending": pending,
            "current": current,
            "emphasis": emphasis,
            "removed": removed,
        }
    )


def _after(node):
    if node is None:
        return "null"
    return str(node.value)


class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def nodes(self):
        current = self.head
        seen = set()
        while current is not None and current not in seen:
            seen.add(current)
            yield current
            current = current.next

    def to_values(self):
        return [node.value for node in self.nodes()]

    def insert_head(self, value, on_step=None):
        node = ListNode(value)
        _step(on_step, f"Create a node holding {value}. It is not linked yet.", pending=node)
        if self.head is None:
            self.head = node
            _step(
                on_step,
                f"The list is empty, so head points at {value}.",
                current=node,
                emphasis={node},
            )
            return node

        old_head = self.head
        node.next = old_head
        _step(
            on_step,
            f"Point {value}'s next at the current head, {old_head.value}.",
            pending=node,
            current=node,
        )
        self.head = node
        _step(
            on_step,
            f"Move head from {old_head.value} to {value}. Nothing else in the list moves.",
            current=node,
            emphasis={node},
        )
        return node

    def insert_tail(self, value, on_step=None):
        node = ListNode(value)
        _step(on_step, f"Create a node holding {value}. It is not linked yet.", pending=node)
        if self.head is None:
            self.head = node
            _step(
                on_step,
                f"The list is empty, so head points at {value}.",
                current=node,
                emphasis={node},
            )
            return node

        current = self.head
        while current.next is not None:
            _step(
                on_step,
                f"{current.value} points at {current.next.value}. There is no tail pointer, so keep walking from the head.",
                current=current,
                pending=node,
            )
            current = current.next

        _step(
            on_step,
            f"{current.value} is the tail, because its next pointer is null.",
            current=current,
            pending=node,
        )
        current.next = node
        _step(
            on_step,
            f"Point {current.value}'s next at {value}.",
            current=node,
            emphasis={node},
        )
        return node

    def insert_at(self, index, value, on_step=None):
        if index < 0:
            _step(on_step, f"Index {index} is invalid. Nothing was inserted.")
            return False
        if index == 0:
            self.insert_head(value, on_step=on_step)
            return True

        node = ListNode(value)
        _step(
            on_step,
            f"Create a node holding {value}. It should end up at index {index}.",
            pending=node,
        )
        if self.head is None:
            _step(
                on_step,
                "The list is empty, so the only valid index is 0. Nothing was inserted.",
                pending=node,
            )
            return False

        previous = self.head
        previous_index = 0
        while previous_index < index - 1:
            if previous.next is None:
                _step(
                    on_step,
                    f"The list ends at index {previous_index}, before index {index}. Nothing was inserted.",
                    current=previous,
                    pending=node,
                )
                return False
            _step(
                on_step,
                f"{previous.value} is at index {previous_index}. The node before index {index} is further along.",
                current=previous,
                pending=node,
            )
            previous = previous.next
            previous_index += 1

        follower = previous.next
        _step(
            on_step,
            f"{previous.value} is at index {previous_index}, immediately before the insertion point.",
            current=previous,
            pending=node,
        )
        node.next = follower
        _step(
            on_step,
            f"Point {value}'s next at {_after(follower)}.",
            pending=node,
            current=node,
        )
        previous.next = node
        _step(
            on_step,
            f"Point {previous.value}'s next at {value}. Every node after the insertion point shifts one index to the right.",
            emphasis={node},
        )
        return True

    def delete(self, value, on_step=None):
        if self.head is None:
            _step(on_step, "The list is empty, so there is nothing to delete.")
            return False

        previous = None
        current = self.head
        index = 0
        while current is not None:
            if current.value == value:
                _step(on_step, f"Found {value} at index {index}.", current=current, emphasis={current})
                follower = current.next
                if previous is None:
                    self.head = follower
                    detail = f"{value} is the head, so move head to {_after(follower)}."
                    emphasis = {follower} if follower is not None else None
                else:
                    previous.next = follower
                    detail = (
                        f"Point {previous.value}'s next past {value}, at {_after(follower)}. "
                        "That previous node had to be saved on the way in, because a node cannot see backward."
                    )
                    emphasis = {previous}
                current.next = None
                _step(on_step, detail, pending=current, removed={current}, emphasis=emphasis)
                return True

            if current.next is None:
                message = (
                    f"{current.value} at index {index} is not {value}, and next is null. "
                    f"{value} is not in the list."
                )
            else:
                message = (
                    f"{current.value} at index {index} is not {value}. "
                    "Save this node as the previous node and follow next."
                )
            _step(on_step, message, current=current)
            previous = current
            current = current.next
            index += 1
        return False

    def search(self, value, on_step=None):
        if self.head is None:
            _step(on_step, f"The list is empty, so {value} is not in the list.")
            return False

        current = self.head
        index = 0
        while current is not None:
            if current.value == value:
                _step(on_step, f"Found {value} at index {index}.", current=current, emphasis={current})
                return True
            if current.next is None:
                message = (
                    f"{current.value} at index {index} is not {value}, and next is null. "
                    f"{value} is not in the list."
                )
            else:
                message = f"{current.value} at index {index} is not {value}. Follow next."
            _step(on_step, message, current=current)
            current = current.next
            index += 1
        return False


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def nodes(self):
        current = self.head
        seen = set()
        while current is not None and current not in seen:
            seen.add(current)
            yield current
            current = current.next

    def to_values(self):
        return [node.value for node in self.nodes()]

    def insert_head(self, value, on_step=None):
        node = ListNode(value)
        _step(on_step, f"Create a node holding {value}. It is not linked yet.", pending=node)
        if self.head is None:
            self.head = self.tail = node
            _step(
                on_step,
                f"The list is empty, so head and tail both point at {value}.",
                current=node,
                emphasis={node},
            )
            return node

        old_head = self.head
        node.next = old_head
        _step(
            on_step,
            f"Point {value}'s next at the current head, {old_head.value}.",
            pending=node,
            current=node,
        )
        old_head.prev = node
        _step(
            on_step,
            f"Point {old_head.value}'s prev back at {value}.",
            pending=node,
            current=old_head,
        )
        self.head = node
        _step(
            on_step,
            f"Move head to {value}. Tail stays at {self.tail.value}.",
            current=node,
            emphasis={node},
        )
        return node

    def insert_tail(self, value, on_step=None):
        node = ListNode(value)
        _step(on_step, f"Create a node holding {value}. It is not linked yet.", pending=node)
        if self.tail is None:
            self.head = self.tail = node
            _step(
                on_step,
                f"The list is empty, so head and tail both point at {value}.",
                current=node,
                emphasis={node},
            )
            return node

        old_tail = self.tail
        node.prev = old_tail
        _step(
            on_step,
            f"Point {value}'s prev at the current tail, {old_tail.value}. "
            "The tail pointer reaches that node without a walk from the head.",
            pending=node,
            current=old_tail,
        )
        old_tail.next = node
        _step(
            on_step,
            f"Point {old_tail.value}'s next at {value}.",
            pending=node,
            current=node,
        )
        self.tail = node
        _step(
            on_step,
            f"Move tail to {value}. Head stays at {self.head.value}.",
            current=node,
            emphasis={node},
        )
        return node

    def delete_head(self, on_step=None):
        if self.head is None:
            _step(on_step, "The list is empty, so there is no head to delete.")
            return False
        self._detach(self.head, on_step, f"The head holds {self.head.value}.")
        return True

    def delete_tail(self, on_step=None):
        if self.tail is None:
            _step(on_step, "The list is empty, so there is no tail to delete.")
            return False
        self._detach(self.tail, on_step, f"The tail holds {self.tail.value}.")
        return True

    def delete(self, value, on_step=None):
        if self.head is None:
            _step(on_step, "The list is empty, so there is nothing to delete.")
            return False

        current = self.head
        index = 0
        while current is not None:
            if current.value == value:
                self._detach(current, on_step, f"Found {value} at index {index}.")
                return True
            if current.next is None:
                message = (
                    f"{current.value} at index {index} is not {value}, and next is null. "
                    f"{value} is not in the list."
                )
            else:
                message = f"{current.value} at index {index} is not {value}. Follow next."
            _step(on_step, message, current=current)
            current = current.next
            index += 1
        return False

    def search(self, value, on_step=None):
        if self.head is None:
            _step(on_step, f"The list is empty, so {value} is not in the list.")
            return False

        current = self.head
        index = 0
        while current is not None:
            if current.value == value:
                _step(on_step, f"Found {value} at index {index}.", current=current, emphasis={current})
                return True
            if current.next is None:
                message = (
                    f"{current.value} at index {index} is not {value}, and next is null. "
                    f"{value} is not in the list."
                )
            else:
                note = " Prev is not needed for a forward search." if index == 0 else ""
                message = f"{current.value} at index {index} is not {value}. Follow next.{note}"
            _step(on_step, message, current=current)
            current = current.next
            index += 1
        return False

    def _detach(self, node, on_step, lead):
        _step(on_step, lead, current=node, emphasis={node})
        previous = node.prev
        follower = node.next
        if previous is None:
            self.head = follower
        else:
            previous.next = follower
        if follower is None:
            self.tail = previous
        else:
            follower.prev = previous
        node.next = None
        node.prev = None

        if previous is None and follower is None:
            detail = f"{node.value} was the only node, so head and tail are now null."
        elif previous is None:
            detail = (
                f"There is no previous node, so head moves to {follower.value} "
                f"and {follower.value}'s prev is cleared."
            )
        elif follower is None:
            detail = (
                f"There is no next node, so tail moves to {previous.value} "
                f"and {previous.value}'s next is cleared."
            )
        else:
            detail = (
                f"Point {previous.value}'s next at {follower.value}, "
                f"and point {follower.value}'s prev at {previous.value}."
            )
        neighbors = {item for item in (previous, follower) if item is not None}
        _step(on_step, detail, pending=node, removed={item for item in (node,)}, emphasis=neighbors or None)


class CircularLinkedList:
    """Singly linked circle with a head pointer and a tail pointer."""

    def __init__(self):
        self.head = None
        self.tail = None

    def nodes(self):
        if self.head is None:
            return
        current = self.head
        while current is not None:
            yield current
            current = current.next
            if current is None or current is self.head:
                return

    def to_values(self):
        return [node.value for node in self.nodes()]

    def insert_head(self, value, on_step=None):
        node = ListNode(value)
        _step(on_step, f"Create a node holding {value}. It is not linked yet.", pending=node)
        if self.head is None:
            node.next = node
            self.head = self.tail = node
            _step(
                on_step,
                f"The list is empty. {value} points at itself, and both head and tail point at it.",
                current=node,
                emphasis={node},
            )
            return node

        old_head = self.head
        node.next = old_head
        _step(
            on_step,
            f"Point {value}'s next at the current head, {old_head.value}.",
            pending=node,
            current=node,
        )
        self.tail.next = node
        _step(
            on_step,
            f"Point the tail, {self.tail.value}, at {value}. "
            f"The new node is reachable from the tail, and head still points at {old_head.value}.",
            pending=node,
            current=self.tail,
        )
        self.head = node
        _step(
            on_step,
            f"Move head to {value}. Tail stays at {self.tail.value}, and its next pointer closes the circle.",
            current=node,
            emphasis={node},
        )
        return node

    def insert_tail(self, value, on_step=None):
        node = ListNode(value)
        _step(on_step, f"Create a node holding {value}. It is not linked yet.", pending=node)
        if self.head is None:
            node.next = node
            self.head = self.tail = node
            _step(
                on_step,
                f"The list is empty. {value} points at itself, and both head and tail point at it.",
                current=node,
                emphasis={node},
            )
            return node

        node.next = self.head
        _step(
            on_step,
            f"Point {value}'s next at the head, {self.head.value}, so the circle can close through the new node.",
            pending=node,
            current=node,
        )
        old_tail = self.tail
        old_tail.next = node
        _step(
            on_step,
            f"Point the current tail, {old_tail.value}, at {value}.",
            pending=node,
            current=old_tail,
        )
        self.tail = node
        _step(
            on_step,
            f"Move tail to {value}. Head stays at {self.head.value}.",
            current=node,
            emphasis={node},
        )
        return node

    def delete(self, value, on_step=None):
        if self.head is None:
            _step(on_step, "The list is empty, so there is nothing to delete.")
            return False

        previous = self.tail
        current = self.head
        index = 0
        seen = 0
        limit = max(1, sum(1 for _ in self.nodes()))
        while True:
            seen += 1
            if seen > limit:
                raise RuntimeError("Circular list walk did not return to the head.")

            if current.value == value:
                _step(on_step, f"Found {value} at index {index}.", current=current, emphasis={current})
                if self.head is self.tail:
                    self.head = None
                    self.tail = None
                    current.next = None
                    _step(
                        on_step,
                        f"{value} was the only node. Head and tail are now null.",
                        pending=current,
                        removed={current},
                    )
                    return True
                if current is self.head:
                    self.tail.next = current.next
                    self.head = current.next
                    current.next = None
                    _step(
                        on_step,
                        f"Point the tail, {self.tail.value}, at the new head, {self.head.value}, and move head forward.",
                        pending=current,
                        removed={current},
                        emphasis={self.head},
                    )
                    return True
                if current is self.tail:
                    previous.next = self.head
                    self.tail = previous
                    current.next = None
                    _step(
                        on_step,
                        f"Point {previous.value}'s next back at the head, {self.head.value}, and move tail to {previous.value}.",
                        pending=current,
                        removed={current},
                        emphasis={previous},
                    )
                    return True
                follower = current.next
                previous.next = follower
                current.next = None
                _step(
                    on_step,
                    f"Point {previous.value}'s next past {value}, at {follower.value}.",
                    pending=current,
                    removed={current},
                    emphasis={previous},
                )
                return True

            if current.next is self.head:
                _step(
                    on_step,
                    f"{current.value} at index {index} is not {value}, and the next node is the head again. "
                    f"{value} is not in the list.",
                    current=current,
                )
                return False

            _step(
                on_step,
                f"{current.value} at index {index} is not {value}. Follow next, and stop if the next node is the head.",
                current=current,
            )
            previous = current
            current = current.next
            index += 1

    def traverse(self, on_step=None):
        if self.head is None:
            _step(on_step, "The list is empty, so there is no lap to walk.")
            return

        current = self.head
        index = 0
        seen = 0
        limit = max(1, sum(1 for _ in self.nodes()))
        while True:
            seen += 1
            if seen > limit + 1:
                raise RuntimeError("Circular list walk did not return to the head.")
            _step(on_step, f"Visit index {index}: {current.value}.", current=current)
            if current.next is self.head:
                _step(
                    on_step,
                    f"The next pointer of {current.value} leads back to the head, {self.head.value}. One lap is finished.",
                    current=self.head,
                    emphasis={self.head},
                )
                return
            current = current.next
            index += 1
