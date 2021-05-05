import client_num, server_num
from concurrent.futures import ProcessPoolExecutor



if __name__=="__main__":
    with ProcessPoolExecutor() as process:
        process.submit(client_num.run)
        process.submit(server_num.run)