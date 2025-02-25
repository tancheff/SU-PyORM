from typing import List


def test(args: List[int]):
    # for a in args:
    a = *args
    return a



list_a = [1, 2, 3, 4, 5]

print(test(list_a))
