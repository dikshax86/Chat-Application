import socket
import threading

HOST='127.0.0.1'
PORT=1234
LISTENER_LIMIT=5
active_clients=[]

#funtion to listen for any messages from client
def listen_for_messages(client,username):
    while True:
        responce=client.recv(2048).decode('utf-8')
        if responce!='':
            final_msg=username+'~'+responce
            send_messages_to_all(final_msg)
        else:
            print(f"message sent from client {username} is empty")
    
def send_messages_to_client(client,message):
    client.sendall(message.encode())


def send_messages_to_all(message):
    for user in active_clients:
        send_messages_to_client(user[1],message)


def client_handler(client):
    #server is listening the client meassages 
    while True:
        username=client.recv(2048).decode('utf-8')
        if username!='':
            active_clients.append((username,client))
            # prompt_msg="SERVER~"+f"added {username} to the chat"
            prompt_msg="WELCOME~"+f"Avaliable users:- {len(active_clients)}"+f"\nusers {', '.join([user for user, _ in active_clients])}"
            send_messages_to_client(client,prompt_msg)
            break
        else:
            print("client username is empty")
           
    threading.Thread(target=listen_for_messages,args=(client,username)).start()

def main():
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        server.bind((HOST,PORT))
        print(f"running the server of {HOST} and {PORT}")
    except:
        print(f"unable to bind the HOST {HOST} and PORT {PORT}")

    server.listen(LISTENER_LIMIT)

    while True:
        client,address=server.accept()
        print(f"successfully connected to client {address[0]},{address[1]}")

        threading.Thread(target=client_handler,args=(client, )).start()
if __name__ == '__main__':
    main()
