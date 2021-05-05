from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing,threading
import socket
import os
from multiprocessing import Queue
from msgutils import recv_msg, send_msg
import time, datetime, sys



q1=Queue()
lock=threading.Lock()
lock1=threading.Lock()
adress=('127.0.0.1',33653)
q = Queue()
q_before_check = Queue()





def start_server(adress, q_before_check):
    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(adress)
        s.listen(10)
        recive_message(s, q_before_check)





def recive_message(s,q_before_check):
    while True:
        t=threading.Thread(target=receive, args=((s.accept(), q_before_check)))
        t.start()
        t.join()


def receive(get_tuple,q_before_check):
    conn = get_tuple[0]
    while True:
        lock1.acquire()
        num = recv_msg(conn)
        if not num:
            lock1.release()
            break
        q_before_check.put(int(num))
        lock1.release()








def run_processes(q_before_check,q):
    process_list=[]
    for i in range(multiprocessing.cpu_count()):
        p=multiprocessing.Process(target=check, args=(q_before_check,q))
        process_list.append(p)
        p.start()
        p.join()
    return True








def write_to_file(q):
    def threads_to_write(q):
        i = 0
        while True:
            if q.empty()==False:
                val=str(q.get())
                lock.acquire()
                print(f'before write{val}')
                f.write(val+'\n')
                f.flush()
                lock.release()
                """if val==0:
                    sys.exit()"""

            """else:
                i=i+1
                print(f'this is i {i}')
                if i>20:
                    print("in else")
                    print(datetime.time())
                    return"""

    with open('list.txt', 'a') as f:
        with ThreadPoolExecutor(max_workers=10) as th:
            threads = []
            for i in range(10):
                threads.append(th.submit(threads_to_write, q))






def check(q_before_check,q):
    while True:
        if q_before_check.empty()==False:
            num=q_before_check.get()
            if num > 1:
                for i in range(2, num):
                    if (num % i) == 0:
                        pass
                    else:
                        q.put(num)
                        break

        """else:
            q.put(0)"""

def run():
    s = multiprocessing.Process(target=start_server, args=(adress, q_before_check))
    s2 = multiprocessing.Process(target=write_to_file, args=(q,))
    s3 = multiprocessing.Process(target=run_processes, args=(q_before_check, q))
    s3.start()
    s.start()
    s2.start()
    s2.join()
    s3.join()
    s.join()




if __name__=="__main__":
    pass



