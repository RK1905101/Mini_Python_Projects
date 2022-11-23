"""
    docstring;
"""
import _thread


class CustomThread:
    """
        custom thread class with stop method;
    """

    def __init__(self, func, name: str, args=tuple()):

        self.func = func
        self.args = args
        self.name = name
        self.thread_id = None

        self.__stop_flag = True

        # set the stop and start flag;
        # self.__stop_flag = threading.Event()

    def stop(self):
        """Exit from the thread;"""

        _thread.exit()

        return None

    def run(self):

        self.thread_id = _thread.start_new_thread(self.func, self.args)

        return None

    def get_id(self):
        """
            return the thread identifier;

        """

        return self.thread_id
