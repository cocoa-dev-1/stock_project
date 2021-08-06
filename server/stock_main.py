import socket
import threading
import pymysql
import sys
import hashlib

if sys.version_info < (3, 6):
    import sha3

db = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='sin532100!!',
    db="stock_project",
    charset='utf8'
)

cursor = db.cursor(pymysql.cursors.DictCursor)


# sql = 'SELECT * FROM stock_users ;'
# cursor.execute(sql)
# result = cursor.fetchall()
# print(result)

HOST = 'localhost'
PORT = 30110

client_users = {}

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_socket.setsockopt(socket.SQL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST,PORT))
server_socket.listen()

def check_name(name):
    sql = 'SELECT * FROM stock_users WHERE user_name = %s'
    cursor.execute(sql, (name))
    result = list(cursor.fetchall())
    if len(result) == 0:
        return True
    else:
        return 'User nickname already exists.'

def check_id(id):
    sql = 'SELECT * FROM stock_users WHERE user_id = %s'
    cursor.execute(sql, (id))
    result = list(cursor.fetchall())
    if len(result) == 0:
        return True
    else:
        return 'User id already exists.'

def client_thread(client_socket, addr):
    global client_users
    print('Connected addr: {0}:{1}'.format(addr[0],addr[1]))
    while True:
        try:

            data = client_socket.recv(1024)
            if not data:
                print('Disconnected by ',addr[0],':',addr[1])
                break

            receive_data = data.decode().split(':')
            receive_data_key = receive_data[0]
            if receive_data_key == "login":
                s = hashlib.sha3_256()
                s.update(receive_data[2].encode('utf-8'))
                hash_result = s.hexdigest()
                sql = f'SELECT * FROM stock_users WHERE user_id = "{receive_data[1]}" AND user_password = "{hash_result}"'
                cursor.execute(sql)
                result = list(cursor.fetchall())
                if result != []:
                    user_name = result[0]['user_name']
                    client_socket.send(f'login success:{user_name}:'.encode())
                else:
                    client_socket.send(f'login failed:The user does not exist.:'.encode())
            elif receive_data_key == 'sign up':
                try:
                    check_nm = check_name(receive_data[3])
                    check_user_id = check_id(receive_data[1])
                    if type(check_nm) == bool and type(check_user_id) == bool:
                        s = hashlib.sha3_256()
                        s.update(receive_data[2].encode('utf-8'))
                        hash_result = s.hexdigest()
                        sql = 'INSERT INTO stock_users(user_id,user_password,user_name) VALUES(%s,%s,%s)'
                        cursor.execute(sql, (receive_data[1],hash_result,receive_data[3]))
                        db.commit()
                        client_socket.send(f'sign up success:{receive_data[3]}'.encode())
                    else:
                        client_socket.send(f'sign up failed:{str(check_nm)}:{str(check_user_id)}:'.encode())
                except Exception as e:
                    print(e)
                    client_socket.send('error:An error occurred while registering as a member.'.encode())
            elif receive_data_key == 'buy_stock':
                
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

    