list_a = [1, 2, 3, 4, 5, 6, 7]
list_b = [2, 4, 0]

for val in list_b:
    if val not in list_a:
        raise ValueError("You have missing values in the main list!")

