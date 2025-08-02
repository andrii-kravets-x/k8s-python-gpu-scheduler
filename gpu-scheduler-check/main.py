import os
import time
import socket

def main():
    while True:
    node_name = socket.gethostname()
    cuda_devices = os.getenv("CUDA_VISIBLE_DEVICES", "Not set")
        print(f"Node: {node_name}, CUDA_VISIBLE_DEVICES: {cuda_devices}")
        time.sleep(10)

if __name__ == "__main__":
    main()

