def minimax(level_order):
    nodes = level_order
    current = 0
    level = 1
    outputs = []

    while True:
        left = 2 * current + 1
        right = 2 * current + 2
        next_level = level + 1

        if left >= len(nodes):
            break

        if right >= len(nodes):
            selected = left
            current = selected
            level = next_level
            continue

        left_val = nodes[left]
        right_val = nodes[right]

        if next_level % 2 == 1:
            if left_val >= right_val:
                selected = left
                cut_val = right_val
            else:
                selected = right
                cut_val = left_val
        else:
            if left_val <= right_val:
                selected = left
                cut_val = right_val
            else:
                selected = right
                cut_val = left_val

        outputs.append(cut_val)

        current = selected
        level = next_level

    return outputs

if __name__ == "__main__":
    input_str = input().strip()
    level_order = list(map(int, input_str.split()))
    outputs = minimax(level_order)
    if outputs:
        print(' '.join(map(str, outputs)))
    else:
        print('Error')
