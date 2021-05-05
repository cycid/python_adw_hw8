from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing
from socket import socket
from msgutils import recv_msg, send_msg
import time, datetime


range_list=[]
sep_list=[]
whole_number_range=2000000
adress = ('127.0.0.1', 33653)


def define_range():
    print('process start')
    step=int(whole_number_range/multiprocessing.cpu_count())
    for i in range(int(step),whole_number_range+1,int(step)):
        item=(i-step, i)
        range_list.append(item)
    print(range_list)
    return range_list




def generator(number_range):
    with socket() as s:
        rec=0
        s.connect(('127.0.0.1', 33653))
        for num in range(number_range[0],number_range[1] + 1):
           if num > 1:
               for i in range(2, num):
                   if (num % i) == 0:
                       break
               else:
                   send_msg(s,str(num).encode())
        time.sleep(3)
        #send_msg(s,str(0).encode())
        return

def send_message(sock,value_i):
    sock.send(value_i)
    return

def set_up_conn(adress):
    with socket() as s:
        s.connect(adress)


def run():

    define_range()
    set_up_conn(adress)

    t = datetime.datetime.now()
    with ProcessPoolExecutor(max_workers=5) as p:
        result = p.map(generator, range_list)









if __name__=="__main__":
    pass


