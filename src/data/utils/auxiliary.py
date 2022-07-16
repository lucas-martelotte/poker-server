def linear_animation(input_value, start_x, start_y, final_x, final_y):

    lam = (input_value - start_x)/(final_x - start_x)

    return (1-lam)*start_y + lam*final_y

def insert_and_extend(array, index, value):
    # This functions inserts the value at the index. If the index
    # is out of range, the list is extended until it isn't anymore.
    extend_amount = index - len(array) + 1
    if extend_amount > 0:
        array.extend([0]*extend_amount)
    array[index] = value

def list_union(first, second):
    return first + list(set(second)-set(first))