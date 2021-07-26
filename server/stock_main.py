import socket
import threading
import pymysql


db = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='sin532100!!',
    db="stock_project",
    charset='utf8'
)

# sql = 'SELECT * FROM stock_users ;'
# cursor.execute(sql)
# result = cursor.fetchall()
# print(result)

HOST = 'localhost'
PORT = 30120

client_users = {}

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_socket.setsockopt(socket.SQL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST,PORT))
server_socket.listen()

def client_thread(client_socket, addr):
    global client_users
    print('Connected addr: {0}:{1}'.format(addr[0],addr[1]))
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print('Disconnected by ' + addr[0]+':'+addr[1])
                break

            receive_data = data.decode().split(':')
            receive_data_key = receive_data[1]
            if receive_data_key == "login":
                cursor = db.cursor(pymysql.cursors.DictCursor)
                sql = f'SELECT * FROM stock_users WHERE user_id = "{receive_data[1]}" AND user_password = "{receive_data[2]}"'
                cursor.execute(sql)
                result = list(cursor.fetchall())
                user_name = result[0]['user_name']
                if result != ():
                    client_socket.send(f'login_success:{user_name}')
                else:
                    client_socket.send(f'login_failed:invail')
            elif receive_data_key == 'sign up':
                pass
            
                

        except ConnectionResetError as e:
            print('Disconnected by ' + addr[0],':',addr[1])
            break

    client_socket.close()

while True:
    
    print('waiting for client')

    client_socket, addr = server_socket.accept()
    client_users[addr[1]] = client_socket
    new_thread = threading.Thread(target=client_thread, args=(client_socket,addr))
    new_thread.daemon = True
    new_thread.start()

    