import math

def dream():
    for hope in range(5):
        try:
            value = hope / 2
        except ZeroDivisionError:
            value = 0
    return value

def loop_forever():
    while False:
        pass
