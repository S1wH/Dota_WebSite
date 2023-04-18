def file_output(func):
    def inner(sp: list, file_name: str = 'file.txt') -> list:
        with open(file_name, 'w') as file:
            file.write(f'{sp}\n')
            res = func(sp)
            file.write(f'{res}\n')
            return res

    return inner


@file_output
def delete_odd_elements(sp: list) -> list:
    return [el for index, el in enumerate(sp) if index % 2 == 0]


@file_output
def delete_even_elements(sp: list) -> list:
    return [el for index, el in enumerate(sp) if index % 2 == 1]


@file_output
def leave_first_last(sp: list) -> list:
    return [el for index, el in enumerate(sp) if index == 0 or index == len(sp) - 1]


@file_output
def leave_first_last_range(sp: list) -> list:
    return [sp[i] for i in range(len(sp)) if i in [0, len(sp) - 1]]

delete_even_elements([1, 2, 3, 4, 5], 'file1.txt')
delete_odd_elements([1, 2, 3, 4, 5], 'file2.txt')
leave_first_last([1, 2, 3, 4, 5])

print(leave_first_last_range([2, 3]))
