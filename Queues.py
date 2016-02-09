########################################
# CS63: Artificial Intelligence, Lab 1
# Spring 2016, Swarthmore College
########################################

class _Queue(object):
    """Abstract base class for FIFO_Queue, LIFO_QUEUE, and Random_Queue
    A queue supports the following operations:
        - adding items with add()
        - removing and returning items with get()
        - determining the number of items with len()
        - checking containment with 'in'
        - printing
    Child classes are required to store items in the self.contents field, but
    may use different data structures for self.contents. Child classes
    importantly differ in which item is returned by get().
    """
    def __init__(self):
        self.contents = []

    def add(self, item):
        """Stores item in the queue."""
        self.contents.append(item)

    def get(self):
        """Removes some item from the queue and returns it."""
        raise NotImplementedError("TODO???")

    def __len__(self):
        """ 'len(q)' calls this method.  Passes the len() call to
        self.contents. This requires that all child classes implement
        contents as a Python type with a valid __len__.
        """
        return len(self.contents)

    def __repr__(self):
        """ 'print q' calls this method.  Passes the repr() call to
        self.contents. This requires that all child classes implement
        contents as a Python type with a valid __repr__.
        """
        return repr(self.contents)

    def __contains__(self, item):
        """ x in q' calls this method.
        Passes the containment check to self.contents. This requires that all
        child classes implement contents as a Python type with a valid
        __contains__.
        """
        return item in self.contents

class QueueException(Exception):
    def __init__(self, msg):
        self.message = msg

class FIFO_Queue(_Queue):
    """First-in-first-out, also known as a classic 'queue', queue
    implementation.  The first call to get() returns the item from the
    first call to add(), the second returns the second, and so on.
    """
    def get(self):
        try:
            return self.contents.pop(0)
        except IndexError:
            raise QueueException("Can't get from an empty queue")

class LIFO_Queue(_Queue):
    """Last-in-first-out, also known as a 'stack', queue implementation.
    The first call to get() returns the item from the most recent call
    to add(), the second returns the next-most-recent, and so on.
    """
    def get(self):
        try:
            return self.contents.pop(-1)
        except IndexError:
            raise QueueException("Can't get from an empty queue")

class Random_Queue(_Queue):
    """Randomized queue implementation.  Each call to get() returns an
    item from the queue chosen uniformly at random.
    """
    def get(self):
        if len(self.contents) == 0:
            raise QueueException("Can't get from an empty queue")
        else:
            return self.contents.pop(randrange(len(self.contents)))


from heapq import heappush, heappop
class Priority_Queue(_Queue):
    def __init__(self):
        self.pq = []
        self.contents = set()

    def add(self, item, priority):
        heappush(self.pq, (priority, item))
        self.contents.add(item)

    def get(self):
        try:
            item = heappop(self.pq)[1]
            self.contents.remove(item)
        except IndexError:
            raise QueueException("Can't get from an empty queue")
        return item

    def __repr__(self):
        return repr(self.pq)

def TestPriorityQueue():
    print "------------"
    print "Testing a PriorityQueue"
    pq = PriorityQueue()
    print "Check that an empty queue is printable"
    print pq
    print "Inserting a:10, b:5, c:2, d:12, e:2, f:25, and g:2"
    pq.add("a", 10)
    pq.add("b", 5)
    pq.add("c", 2)
    pq.add("d", 12)
    pq.add("e", 2)
    pq.add("f", 25)
    pq.add("g", 2)
    print pq
    print "Removing the minimum until empty"
    while (len(pq)>0):
        print pq.get()

def TestQueue(q):
    print "------------"
    print "Testing", type(q)
    for i in range(10):
        q.add(i*10)
    print "Queue contains:", q
    print "Length of Queue is", len(q)
    if 22 in q:
        print "We have a problem"
    if 50 in q:
        print "50 is in Queue"
    for i in range(10):
        print "Get returned", q.get()
    try:
        q.get()
    except QueueException:
        print "Correctly throws exception when get called on empty queue"

def main():
    TestQueue(FIFO_Queue())
    TestQueue(LIFO_Queue())
    TestQueue(Random_Queue())
    TestPriorityQueue()

if __name__ == '__main__':
    main()
