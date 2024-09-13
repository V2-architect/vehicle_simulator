

import threading
import time


class Foo:
    def __init__(self):
        self.x = 1

class Bar:
    def __init__(self, foo):
        self.foo = foo

    def plus(self):
        self.foo.x += 1

def main():
    foo = Foo()
    bar = Bar(foo)

    while True:
        bar.plus()
        print(f"foo.x: {foo.x}")
        time.sleep(1)

if __name__ == "__main__":
    main()
