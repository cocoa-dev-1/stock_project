import threading
import tkinter
import socket
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTKAgg
import pkg.api

HOST = '127.0.0.1'
PORT = 30120

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST,PORT))

def new_client_thread(client_socket):
    pass


new_thread = threading.Thread(target=new_client_thread, args=(client_socket,))
new_thread.daemon = True
new_thread.start()