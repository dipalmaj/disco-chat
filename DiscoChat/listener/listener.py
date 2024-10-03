import socket


def main():
    """
    Bash to send TCP command to this listener
    echo "restart" | nc <IP_ADDRESS> <PORT>
    """
    host = '0.0.0.0'  # Listen on all available interfaces
    port = 12345       # Choose an available port for the listener

    # Create the socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)

    print(f"Listening on port {port}...")

    while True:
        conn, addr = s.accept()
        print(f"Connection from {addr}")

        data = conn.recv(1024)
        message = data.decode('utf-8').strip()

        if message == 'restart':
            print("Restarting...")
            # Add your restart logic here

        conn.close()


if __name__ == '__main__':
    main()