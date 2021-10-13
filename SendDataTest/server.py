import socket
import time
import numpy as np
import main
import threading
import signal
class Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
 
        # The shutdown_flag is a threading.Event object that
        # indicates whether the thread should be terminated.
        self.shutdown_flag = threading.Event()
    
    def run(self):
        start_flag = False
        operationController = main.Main()
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        server_address = ('localhost', 10000)
        print('starting up on {} port {}'.format(*server_address))
        sock.bind(server_address)
        sock.settimeout(1)

        # Listen for incoming connections
        sock.listen(1)

        while not self.shutdown_flag.is_set():
            # Wait for a connection
            try:
                print('waiting for a connection')
                connection, client_address = sock.accept()
                start_flag = True
            except:
                pass
            else:
                try:
                    print('connection from', client_address)
                    start = time.time()
                    # Receive the data in small chunks
                    fullmessage = bytearray(0)
                    while True:
                        receive_message = connection.recv(4096)
                        if receive_message:
                            fullmessage += receive_message
                        else:
                            if(fullmessage[-3:] == b'end'):
                                fullmessage = fullmessage[:-3]
                                break
                            else:
                                fullmessage = bytearray(0)
                                raise Exception
                except:
                    print("error: conection lost")
                    connection.close()
                    break
                else:
                    header = fullmessage[:32].decode("utf-8").split(';')
                    message = np.frombuffer(fullmessage[32:], dtype=eval(header[0])).reshape(eval(header[1]))
                    print('time to get the data: ', time.time() - start)
                    operationController.makeOp(message)
                    # Clean up the connection
                    connection.close()
        if start_flag:
            operationController.close()
        print("Fin thread")

class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass
 
 
def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit

if __name__ == "__main__":
    # Register the signal handlers
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)
    print("Start")
    try:
        serv = Server()
        serv.start()
        while True:
            time.sleep(0.5)
    except ServiceExit:
        serv.shutdown_flag.set()
        serv.join()
        print("End")
