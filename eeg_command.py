import socket
import pyautogui
import time
import csv
from datetime import datetime

# List to store key and timestamp data
eeg_data = []

def simulate_key_press(key):
    # Simulate key press based on the received data
    pyautogui.press(str(key))
    print(f"Simulated key press: {key}")

    # Record the EEG system time when the event occurs
    eeg_timestamp = time.time()

    # Convert the Unix timestamp to a readable format
    eeg_readable_timestamp = datetime.fromtimestamp(eeg_timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')
    print(f"EEG timestamp (readable): {eeg_readable_timestamp}")

    # Store key and timestamp data in the list
    eeg_data.append([key, eeg_readable_timestamp])

def save_to_csv():
    # Create a unique filename with the current datetime
    csv_filename = f'Data/EEG_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

    # Write key and timestamp data to the CSV file
    with open(csv_filename, mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Command', 'Timestamp']) 
        csv_writer.writerows(eeg_data)


# Create a socket and start listening for incoming connections
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# EEG laptop's IP and the chosen port
server.bind(('192.168.100.57', 5064))  
server.listen()

print("Waiting for incoming connections...")

try:
    while True:
        # Accept a connection from a client
        client, addr = server.accept()
        print(f"Connection from {addr}")

        # Receive data from the client
        data = client.recv(1024).decode('utf-8')

        if data in ('2', '3'):
            simulate_key_press(data)

        # Close the connection with the client
        client.close()

except KeyboardInterrupt:
    save_to_csv()
    # Handle KeyboardInterrupt (Ctrl+C) to exit the loop
    print("\nScript terminated by user.")

finally:
    # Close the server socket
    server.close()
