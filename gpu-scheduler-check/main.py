import os
import time
import socket

def main():
    name = socket.gethostname()
    cuda_devices = os.getenv("CUDA_VISIBLE_DEVICES", "Not set")
    while True:
        print(f"Pod name: {name}, CUDA_VISIBLE_DEVICES: {cuda_devices}", flush=True)
        time.sleep(10)

if __name__ == "__main__":
    main()
