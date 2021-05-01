from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing,threading
import socket
import os
from multiprocessing import Queue
from msgutils import recv_msg, send_msg
import time



q1=Queue()
lock=threading.Lock()
lock1=threading.Lock()
adress=('127.0.0.1',33653)





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



"""def recive_message2(s, q):
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
                break"""







def run_processes(q_before_check,q):
    process_list=[]
    for i in range(5):
        p=multiprocessing.Process(target=check, args=(q_before_check,q))
        process_list.append(p)
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
                    print(f'writing{val}')
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






def check(q_before_check,q):
    while True:
        if q_before_check.empty()==False:
            num=q_before_check.get()
            print(f'{num}in c before iter')
            if num > 1:
                for i in range(2, num):
                    if (num % i) == 0:
                        pass
                    else:
                        print(f'{num}in check{threading.get_ident()}')
                        q.put(num)
                        break





if __name__=="__main__":
    q=Queue()
    q_before_check=Queue()
    #exam(q)
    """with ProcessPoolExecutor(max_workers=2) as proc:
        proc.submit(start_server, args=((adress), q))
        proc.submit(write_to_file, q)"""
    """with ThreadPoolExecutor(max_workers=10) as th:
        threads=[]
        for i in range(10):
            print("run")
            threads.append(th.submit(write_to_file, ))"""
    s=multiprocessing.Process(target=start_server, args=(adress, q_before_check))
    s2=multiprocessing.Process(target=write_to_file, args=(q,))
    s3=multiprocessing.Process(target=run_processes, args=(q_before_check, q))
    s3.start()
    s.start()
    s2.start()
    s2.join()
    s3.join()
    s.join()
    #start_server(adress)

