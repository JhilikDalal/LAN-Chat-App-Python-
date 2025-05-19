import socket   # enables TCP communication.
import threading    #allows running tasks (like receiving messages) simultaneously.

SERVER_IP = input("Enter the server IP Address:")  # Input the IP address of the server
PORT = 5000

#Listens for messages from the server using recv(). Decodes and prints messages.
#If no message received (recv() returns empty), it means the server closed connection, so it breaks out of loop.
#Handles exceptions (like network errors) by printing a message and stopping.
def receive_message(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
            else:
                # Server closed connection
                print("Disconnected from server.")
                break
        except:
            print("Connection closed.")
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creates a TCP socket object for connecting to the server.
    try:
        client.connect((SERVER_IP, PORT))   #Tries to connect to the server’s IP and port.
        print(f"Connected to the server at {SERVER_IP}:{PORT}")
        print("Enter Your Message Here:")
    except Exception as e:                  #If connection fails (server offline, wrong IP, etc.), it prints an error and exits.
        print(f"Failed to connect to server: {e}")
        return

    # Start the thread to receive messages
    #Starts a background thread that calls receive_message(client) to continuously listen for incoming messages.
    threading.Thread(target=receive_message, args=(client,), daemon=True).start()#daemon=True means thread closes automatically when main program exits.

    while True:
        message = input()
        if message.lower() == 'exit':
            print("Closing connection...")
            client.close()
            break
        try:
            client.send(message.encode())
        except Exception as e:
            print(f"Failed to send message: {e}")
            break

if __name__ == "__main__":
    main()
