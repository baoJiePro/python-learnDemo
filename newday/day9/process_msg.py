from multiprocessing import Process, Queue


def f(q):
    q.put([42, None, 'hello'])


q = Queue()
p = Process(target=f, args=(q,))
p.start()
print(q.get())
p.join()

