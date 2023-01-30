import threading
from queue import Queue


EOP = "END_OF_PRINTING"


class NBPrint(threading.Thread):
    """
    The actual thread that does the printing.
    While this class can be used manually, you lose nothing
    and gain abstraction by using the `Printer` class.
    """
    def __init__(self, q: Queue):
        """ Initialize thread (not start). """
        super().__init__()
        self._q = q

    def run(self):
        """
        This is what is run in the separate thread.
        Making a call directly to this will freeze the program.
        Use NBPrint.start() instead.
        """
        while True:
            print_value = self._q.get()
            if print_value == EOP:
                return
            print(*print_value[0], **print_value[1])

    
class Printer:
    def __init__(self):
        """ Initialize and set up multithreaded printer. """
        self._print_q = Queue()
        self._print_thread = NBPrint(self._print_q)
        self._print_thread.start()

    def end(self):
        """
        Close the printer. 
        Failing to use this will prevent the program from stopping,
        as the printer thread will continue running.
        """
        self._print_q.put(EOP)
        self._print_thread.join()

    def print(self, *args, **kwargs) -> None:
        """
        Put some object to print into the queue.
        This method can be used exactly like the builtin print statement,
        as all arguments passed here will be directly entered into a print
        later on, keywords and all.
        """
        self._print_q.put((args, kwargs))

    
