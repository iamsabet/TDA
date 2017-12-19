from threading import Thread

import TwitsManipulator

left = 1468168240000
right = 1468177200000
threads = []
step = (right - left) / 48


class Main():
    def twitsManipulator(self):
        print(left,right)
        TwitsManipulator.twitsManipulator(left, right)


if __name__ == '__main__':
    obj = Main()
    for x in range(0, 48):
        right = left + step
        print(x,") -- left: ", left, " - right: ", right)
        thread_temp = Thread(target=obj.twitsManipulator)
        print(thread_temp)
        threads.append(thread_temp)
        thread_temp.start()
        left = left + step
    for x in range(0, 7):
        threads[x].join()
    print("Finished")
