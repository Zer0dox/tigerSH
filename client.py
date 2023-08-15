from cryptography.fernet import Fernet
import socket
import os
import time

debug_mode = True
log_name = "tigerSH.log"

# Simple write to file function
def write_to_file(filename, content):

    with open(filename, 'w') as file:
        file.write(content)
        file.close()

# Check if in debug mode
def d_mode_log(key):

    # Log key to file.
    if debug_mode == True:
        write_to_file(log_name, key)

# Simple clear screen function (portable)
def clear_screen():

    os_name = os.name

    if os_name == 'posix':
        # Unix/Linux/MacOS/BSD/etc.
        os.system('clear')
    elif os_name == 'nt':

        # Windows
        os.system('cls')
    else:

        # Fallback for other operating systems.
        print('\n' * os.get_terminal_size().lines)

# Main init of script
def main():

    host = input("Please enter host of remote tigerSH: ")
    port = 116 # According to server port.

    cmdline = "sh@"+host+"~# "
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        try:
            
            # Establish connection to remote tigerSH server
            print("Attempting to connect to "+host+"...")
            s.connect((host, port))
            print("Performing key exchange for encryption...")
            key = s.recv(1024)
            print("Received!")
            print(key.hex())
            cipher_suite = Fernet(key)
            clear_screen() # Clean screen
            d_mode_log() # Check if script is being ran in debug mode

            # Begin command input
            while(True):

                try:

                    req = input(cmdline)
                    encrypted_req = cipher_suite.encrypt(req.encode())
                    s.sendall(encrypted_req)
                    encrypted_data = s.recv(1024)
                    decrypted_data = cipher_suite.decrypt(encrypted_data)
                    print('Received:', decrypted_data.decode())

                except Exception as e:

                    print(str(e))

        except Exception as e:

            print(str(e))

if __name__ == "__main__":
    main()

