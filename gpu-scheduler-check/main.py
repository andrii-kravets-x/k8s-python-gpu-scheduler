import os
import time
import socket

def main():
    node_name = socket.gethostname()
    cuda_devices = os.getenv("CUDA_VISIBLE_DEVICES", "Not set")
    while True:
        print(f"Node: {node_name}, CUDA_VISIBLE_DEVICES: {cuda_devices}", flush=True)
        time.sleep(5)

if __name__ == "__main__":
    main()
