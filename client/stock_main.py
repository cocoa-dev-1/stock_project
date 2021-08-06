from logging import root
import threading
import tkinter
import socket
import threading
import os
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import random
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
#from matplotlib.backends.backend_tkagg import FigureCanvasTKAgg
import pkg.api

root = tkinter.Tk()
root.title('주식')

HOST = '127.0.0.1'
PORT = 30110

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST,PORT))

user_login_success = False
user_name = ''

def login():
    user_id = input('아이디를 입력하세요. : ')
    user_pass = input('비밀번호를 입력하세요. : ')
    client_socket.send(f'login:{user_id}:{user_pass}:'.encode())
    # return f'{user_id}:{user_pass}:'

def logout():
    global user_name
    global user_login_success
    user_name = ''
    user_login_success = False

def register():
    user_id = input('사용할 아이디를 입력하세요. : ')
    user_pass = input('사용할 비밀번호를 입력하세요 : ')
    user_name = input('사용할 닉네임을 입력하세요. : ')
    client_socket.send(f'sign up:{user_id}:{user_pass}:{user_name}'.encode())
    # return f'{user_id}:{user_pass}:{user_name}:'

def end():
    os.system('kill %d' % os.getpid())

def main_page(type=1):
    print('종합 정보 시스템.')
    if type == 1:
        print('1. 로그인을 하시려면 1을 눌러주세요.')
        print('2. 회원가입을 하시려면 2를 눌러주세요.')
    print('3 프로그램을 종료하시려면 3을 눌러주세요.')
    result = input()
    if result == '1' and type == 1:
        login(client_socket)
    elif result == '2' and type == 1:
        register(client_socket)
    elif result == '3':
        end()
    elif result == '4' and type == 2:
        logout(client_socket)
    else:
        print('정확한 번호를 입력해주세요.')
        main_page()


def new_client_thread(client_socket):
    global user_name
    global user_login_success
    client_socket.send('connected:'.encode())
    # print('로그인 시스템 시작.\n1. login\n2. sign up')
    # test = input()
    # return_data = menus[test]()
    # print(return_data, test)
    # client_socket.send((test+':'+return_data).encode())
    main_page()

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print('Disconnected')
                break
            
            receive_data = data.decode()
            
            receive_data_split = receive_data.split(':')
            receive_data_key = receive_data_split[0]
            if receive_data_key == 'login success':
                print(f'로그인 성공 닉네임 : {receive_data_split[1]}')
                user_name = receive_data_split[1]
                user_login_success = True
                main_page(type=2)
            elif receive_data_key == 'login failed':
                print(f'로그인 실패\n이유:{receive_data_split[1]}')
                main_page()
                # return_data = menus['login']()
                # print(return_data, test)
                # client_socket.send((test+':'+return_data).encode())
            elif receive_data_key == 'sign up success':
                print(f'회원가입 성공 닉네임 : {receive_data_split[1]}')
                main_page()
            elif receive_data_key == 'sign up failed':
                print(f'회원가입 실패.\n이유:\n 닉네임 사용 여부:{receive_data_split[1]}\n 아이디 사용 여부:{receive_data_split[2]}')
                main_page()
        except ConnectionResetError as e:
            print('Disconnected')
            break

    client_socket.close()


new_thread = threading.Thread(target=new_client_thread, args=(client_socket,))
new_thread.daemon = True
new_thread.start()

root.mainloop()