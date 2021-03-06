from threading import Thread

import TwitsAnaysis

# 1468168200000 France - Portugal ( Final ) - 154 mins (1)
# 1468177440000

# 1467909000000	France - Germany (Semi Final) 111mins (2)
# 1467915720000

# 1467563400000	France - Iceland (Quarter Final) 108mins (3)
# 1467570000000

# 1467483720000	Germany Italy - ( 1/8 ) 158 mins (1 - 1) penalties (6 - 5)
# 1467493200000

left = 1467483720000
right = 1467493200000

threads = []
step = (right - left) / 32


class Main:
    def twitsManipulator(self):
        print(left, right)
        TwitsAnaysis.twitsManipulator(left, right)


if __name__ == '__main__':
    obj = Main()
    for x in range(0, 32):
        right = left + step
        print(x, ") -- left: ", left, " - right: ", right)
        thread_temp = Thread(target=obj.twitsManipulator)
        print(thread_temp)
        threads.append(thread_temp)
        thread_temp.start()
        left = left + step

    for x in range(0, 32):
        threads[x].join()

    print("Finished")
