# -*- coding: utf-8 -*-

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################


class Stack(object):
    def __init__(self):
        self.array = []

    def __del__(self):
        del self.array[:]

    def push(self, item):
        self.array.append(item)

    def pop(self):
        if len(self.array) > 0:
            return self.array.pop()
        return None

    def top(self):
        n = len(self.array)
        if n > 0:
            return self.array[n - 1]
        return None

    def empty(self):
        return 0 == len(self.array)

    def show(self):
        if 0 == len(self.array):
            print('stack is empty')
        else:
            print('---')

            for item in reversed(self.array):
                print(item)

            print('---')


def demo001():
    stack = Stack()
    assert stack.empty()

    item = 1
    stack.push(item)
    assert not stack.empty()
    stack.show()

    assert item == stack.top()
    assert item == stack.pop()
    stack.show()

    stack.push(item)
    assert not stack.empty()
    stack.show()

    item = 2
    stack.push(item)
    assert not stack.empty()
    stack.show()

    assert item == stack.top()
    assert item == stack.pop()
    assert not stack.empty()
    stack.show()

    item = 1
    assert item == stack.top()
    assert item == stack.pop()
    assert stack.empty()
    stack.show()


if __name__ == '__main__':
    demo001()
