import time


# функциональное программировани -> возможность передавать функцию параметром в функцию
def math_result(a, b, f):
    return f(a, b)


def math_summ(a, b):
    return a + b


def math_multiply(a, b):
    return a * b


def beautiful_print(f):
    def inner(*args, **kwargs):
        delimeter = "*" * 100
        print(delimeter)
        result = f(*args, **kwargs)
        print(delimeter)
        return result

    return inner


class BeatifulPrint:
    def __init__(self, delimeter):
        self.delimeter = delimeter

    def __call__(self, f):
        def inner(*args, **kwargs):
            delimeter = self.delimeter * 100
            print(delimeter)
            result = f(*args, **kwargs)
            print(delimeter)
            return result

        return inner


def debug(f):
    def inner(*args, **kwargs):
        start_time = time.time()
        print("time", start_time)
        result = f(*args, **kwargs)
        print("timedelta", time.time() - start_time)
        return result

    return inner


def hello():
    # start_time = time.time()
    # print('time', start_time)
    # print('name', 'hello')
    print("hello")
    # print('timedelta', time.time() - start_time)


@BeatifulPrint("$%^")
@debug
def summ(a, b):
    print(a + b)


@beautiful_print
@debug
def get_summ(a, b):
    return a + b


hello()

# result = math_result(1, 2, math_summ)
# print(result)
#
# result = math_result(1, 2, math_multiply)
# print(result)

hello = beautiful_print(debug(hello))

hello()

summ(2, 3)

result = get_summ(4, 5)
print(result)


print(dir(summ))

print(summ(2, 3))


class SomeClass:
    def __call__(self, *args, **kwargs):
        print("Вызови меня как функцию")


s = SomeClass()

print(dir(s))

s()
