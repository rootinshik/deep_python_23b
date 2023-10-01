class CustomList(list):
    ...


if __name__ == '__main__':
    cl1 = CustomList([5, 1, 3, 7])
    cl2 = CustomList([1, 2, 7])
    cl3 = CustomList([6, 3, 10, 7])
    assert cl1 + cl2 == cl3
