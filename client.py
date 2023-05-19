import socket
import threading

host='127.0.0.1'
port=1234

def listen_to_messages_from_server(client):
    while True:
        message=client.recv(2048).decode('utf-8')
        if message!='':
            username=message.split("~")[0]
            content=message.split("~")[1]

            print(f"[{username}] ....... {content} ")
        else:
            print("Message received from client is empty")
    
def send_message_to_server(client):
    while True:
        message=input("Message: ")
        if message!='':
            client.sendall(message.encode())
        else:
            print("message is empty")
            exit(0)

def communicate_to_server(client):
    username=input("Enter Username:")
    if username!='':
        client.sendall(username.encode())
    else:
        print("username cannot be empty")
        exit(0)

    threading.Thread(target=listen_to_messages_from_server,args=(client,)).start()


    send_message_to_server(client)


def main():
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        client.connect((host,port))
        print("succefully connected to server")
    except:
        print(f"unable to connect to server {host} and {port}")

    communicate_to_server(client)
if __name__=='__main__':
    main()
