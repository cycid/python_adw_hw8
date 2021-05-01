from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing,threading
import socket
import os
from multiprocessing import Queue
from msgutils import recv_msg, send_msg
import time



q1=Queue()
lock=threading.Lock()
adress=('127.0.0.1',33653)





def start_server(adress, q):
    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(adress)
        s.listen(10)
        run_processes(s, q)





"""def recive_message(s,q):
    while True:
        t = threading.Thread(target=recive_message2, args=(s.accept(), q))
        t.start()
        t.join()"""



def recive_message2(s, q):
    rec=0
    get_tuple = s.accept()
    conn = get_tuple[0]
    while True:
        num = int(recv_msg(conn))
        if num > 1:
            for i in range(2, num):
                if (num % i) == 0:
                    break
                else:
                    print(num)
                    q.put(num)
                    break

        # check(int(number),q)
        if num == 0:
            rec+=1
            if rec==4:
                time.sleep(20)
                print("all messages received")
                break







def run_processes(s,q):
    """with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as p:
        p.submit(recive_message, args=(s,q))
        p.submit(recive_message, args=(s,q))
        p.submit(recive_message, args=(s,q))
        p.submit(recive_message, args=(s,q))"""
    process_list=[]
    for i in range(5):
        p=multiprocessing.Process(target=recive_message2, args=(s,q))
        process_list.append(p)
        print("start process")
        p.start()
        p.join()
    return True

def exam(q):
    i=0
    with open("error.txt", "a") as o:
        while True:
            time.sleep(2)
            o.write("join")
            o.flush()
            i+=1
            if i==10:
                break

            """if q.empty() == True:                
                val = str(q.get())
                #lock.acquire()
                print(f'{val} before writing{lock.locked()}')
                o.write(val)
                #lock.release()
                if val == 0:
                    break"""







def write_to_file(q):
    def threads_to_write(q):
            while True:
                if q.empty()==False:
                    val=str(q.get())

                    lock.acquire()
                    f.write(val+'\n')
                    f.flush()
                    lock.release()
                    if val==0:
                        break

                    """if q.empty()==True:
                        print("empty")
                        break"""

    with open('list.txt', 'a') as f:
        with ThreadPoolExecutor(max_workers=10) as th:
            threads = []
            for i in range(10):
                threads.append(th.submit(threads_to_write, q))






def check(num,q):
    if num > 1:
        for i in range(2, num):
            if (num % i) == 0:
                return
            else:
                print(multiprocessing.current_process())
                q.put(num)
                return
    return

if __name__=="__main__":
    q=Queue()
    #exam(q)
    """with ProcessPoolExecutor(max_workers=2) as proc:
        proc.submit(start_server, args=((adress), q))
        proc.submit(write_to_file, q)"""
    """with ThreadPoolExecutor(max_workers=10) as th:
        threads=[]
        for i in range(10):
            print("run")
            threads.append(th.submit(write_to_file, ))"""
    s=multiprocessing.Process(target=start_server, args=(adress, q))
    s2=multiprocessing.Process(target=write_to_file, args=(q,))
    s.start()
    s2.start()
    s2.join()
    s.join()
    #start_server(adress)

