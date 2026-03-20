#!/usr/bin/python3
"""Module providing a lockbox puzzle implementation"""


def canUnlockAll(boxes: list) -> bool:
    """Checks if a dual-level list of >0 ints can be fully explored."""

    # First guard clauses
    # Not a list = cannot process
    if not (isinstance(boxes, list)):
        # print("@dev: Boxes is NOT a list")
        return False
    # Empty box or single cell = success
    # (because of rule "first cell is always unlocked")
    if len(boxes) < 2:
        # print("@dev: Boxes has 0 or 1 element nothing to check")
        return True

    # Revised base logic compared to draft is:
    #   1) We exploit assertion that 1st level cells's content is a sublist.
    #   2) We exploit assertion that sublist's content is positive integers
    #      so data usable as a list index.
    #   3) We set a "visited_boxes" register to track boxes opened once.
    #   4) We set a "boxes_to_explore" register to create a todolist.
    #      With "first 1st level cell" inside it since we know it's the start.
    #   5) Then we just pop a task from list, explore related cell's content,
    #      and add new tasks if the found keys don't match already visited ones

    boxes_to_explore = set()
    boxes_to_explore.add(0)
    visited_boxes = set()
    visited_boxes.add(0)  # First box of index 0 is visited
    invalid_keys = set()

    # We continue working as long as we have boxes to open.
    # Inside the loop we go box by box to see if there are new keys
    #   to add to our list of boxes we can (now) open but didn't (yet).
    while (boxes_to_explore):
        key_of_next_box = boxes_to_explore.pop()
        for key in boxes[key_of_next_box]:
            if key not in (visited_boxes | invalid_keys):
                try:
                    boxes[key]
                    # Won't be executed if was out of range
                    # Warning: list -> append, Set -> add
                    boxes_to_explore.add(key)
                except Exception as e:
                    invalid_keys.add(key)
        visited_boxes.add(key_of_next_box)
    # print(f"@dev: For starting boxes {boxes}")
    # print(f"@dev: we could open the following: {visited_boxes}")

    return len(visited_boxes) == len(boxes)
