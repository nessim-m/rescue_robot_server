# import socket
# from flask import Flask, render_template, Response
#
# from camera_opencv import Camera
#
# HOST = '192.168.1.139'  # Standard loopback interface address (localhost)
# PORT = 5001  # Port to listen on (non-privileged ports are > 1023)
#
# dataFromClient = ""
#
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print('Connected by', addr)
#         while True:
#             # conn.sendall(b"hi!!?")
#             data = conn.recv(1024)
#             print(data)
#             if not data:
#                 break
#             dataFromClient = data.decode('utf-8')
#             if 'start' in dataFromClient:
#                 app = Flask(__name__)
#             # print('sending data recieved back...')
#             # conn.sendall(data)
#             conn.send(b"Connected")
#             break
#
#
# # def start():
# #     camera = Camera()
#
#
# def gen(camera):
#     while True:
#         frame = camera.get_frame()
#
#         yield (b'--frame\r\n'
#
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#
#
# @app.route('/')
# def video_feed():
#     return Response(gen(Camera()),
#
#                     mimetype='multipart/x-mixed-replace; boundary=frame')
#
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', threaded=True)

# ----------------------------------------------------------------------------------


import random
import socket
import threading
import time
import psutil
from flask import Flask, render_template, Response
from camera_opencv import Camera

HOST = '192.168.1.139'
PORT = 5001
ADDR = (HOST, PORT)
HEADER = 64
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {HOST}")
    while True:
        conn, addr = server.accept()
        thread_count = threading.active_count() - 1
        if thread_count == 0:
            thread = threading.Thread(target=handle_robot_status_client, args=(conn, addr))
            thread.start()
        elif thread_count == 1:
            thread = threading.Thread(target=handle_robot_distance_client, args=(conn, addr))
            thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


def get_cpu_use():
    """ Return CPU usage using psutil"""
    cpu_cent = psutil.cpu_percent()
    return str(cpu_cent)


def get_cpu_temp_func():
    """ Return CPU temperature """
    result = 0
    mypath = "/sys/class/thermal/thermal_zone0/temp"
    with open(mypath, 'r') as mytmpfile:
        for line in mytmpfile:
            result = line

    result = float(result) / 1000
    result = round(result, 1)
    return str(result)


def get_ram_info():
    """ Return RAM usage using psutil """
    ram_cent = psutil.virtual_memory()[2]
    return str(ram_cent)


print("[STARTING] server is starting...")
start()


def gen(camera):
    while True:
        frame = camera.get_frame()

        yield (b'--frame\r\n'

               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def video_feed():
    return Response(gen(Camera()),

                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)




# THREAD 1
def handle_robot_status_client(conn, addr):
    print(f"[ROBOT STATUS CLIENT] {addr} connected.")
    connected = True

    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"[{addr}] {msg}")
            conn.send(b"Ready")
            if 'start' in dataFromClient:
                app = Flask(__name__)
        else:
            connected = False

    conn.close()


# THREAD 2
def handle_robot_distance_client(conn, addr):
    print(f"[ROBOT DISTANCE CLIENT] {addr} connected.")
    connected = True
    time.sleep(2)
    while connected:
        conn.send(str(random.randint(0, 50)).encode('ASCII'))
        time.sleep(1)
        conn.send(str(random.randint(0, 50)).encode('ASCII'))
        time.sleep(1)

    conn.close()


# THREAD 3
def handle_robot_cpu_temp_client(conn, addr):
    print(f"[ROBOT DISTANCE CLIENT] {addr} connected.")
    connected = True
    time.sleep(2)
    while connected:
        conn.send(u'{get_cpu_temp_func()}\N{DEGREE SIGN}'.encode('ASCII'))
        time.sleep(2)

    conn.close()


# THREAD 4
def handle_robot_cpu_usage_client(conn, addr):
    print(f"[ROBOT DISTANCE CLIENT] {addr} connected.")
    connected = True
    time.sleep(2)
    while connected:
        conn.send(f"{get_cpu_use()}%".encode('ASCII'))
        time.sleep(2)

    conn.close()


# THREAD 5
def handle_robot_ram_usage_client(conn, addr):
    print(f"[ROBOT DISTANCE CLIENT] {addr} connected.")
    connected = True
    time.sleep(2)
    while connected:
        conn.send(f"{get_ram_info()}%".encode('ASCII'))
        time.sleep(2)

    conn.close()

