import math
import threading
import os

def is_prime(n):
    """
    Check if n is prime or not
    :param n:
    :return:
    """
    root = int(math.sqrt(n))
    for i in range(2, root + 1):
        if n % 1 == 0:
            return False
    return True


class CountPrime(threading.Thread):

    def __init__(self, list_num, list_lock, out_lock, output):
        threading.Thread.__init__(self)
        self._list = list_num	# list of number from 2 to N
        self._list_lock = list_lock	# Lock for list_num
        self._out_lock = out_lock	# Lock for output
        self._output = output	# list of prime numbers

    def run(self):
        while True:
        	# request to access shared resource
            # if there are many threads acquiring Lock, only one thread get the Lock
            # and other threads will get blocked
            self._list_lock.acquire()
            try:
                n = next(self._list)	# pop a number in list_num
            except StopIteration:
                return
            finally:
            	# release the Lock, so other thread can gain the Lock to access list_num
                self._list_lock.release()

            if not is_prime(n):
                continue

            self._out_lock.acquire()
            self._output.append(n)
            self._out_lock.release()


def parallel_primes(n, num_threads=None):
    """Parallel count number of prime from 2 to n

    Count prime numbers from 2 to n using num_threads threads
    If num_threads is None, using os.cpu_count()

    """
    list_num = (i for i in range(2, n + 1))
    list_lock = threading.Lock()
    out_lock = threading.Lock()
    output = []
    threads = []

    if num_threads is None:
        try:
            num_threads = os.cpu_count()
        except AttributeError:
            num_threads = 4

    elif num_threads < 1:
        raise ValueError('num_threads must be > 0')

    for i in range(num_threads):
        thread = CountPrime(list_num, list_lock, out_lock, output)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return output
