#!/usr/bin/env python3
# Tcp Port Forwarding (Reverse Proxy)
# Author : istiakshihab <istiak@pm.me>


import socket
import threading
import time
import logging


format = '%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=format)

class PortConfig:
    def __init__(
        self, 
        localhost, 
        localport, 
        remotehost, 
        remoteport) -> None:
        self.localhost = localhost
        self.localport = localport
        self.remotehost = remotehost
        self.remoteport = remoteport
    def __str__(self) -> str:
        return "localhost: " + self.localhost + ":" + self.localport + "\nremotehost: " + self.remotehost + ":" + self.remoteport

def handle(buffer, direction, src_address, src_port, dst_address, dst_port):
    '''
    intercept the data flows between local port and the target port
    '''
    if direction:
        logging.debug(f"{src_address, src_port} -> {dst_address, dst_port} {len(buffer)} bytes")
    else:
        logging.debug(f"{src_address, src_port} <- {dst_address, dst_port} {len(buffer)} bytes")
    return buffer


def transfer(src, dst, direction):
    src_address, src_port = src.getsockname()
    dst_address, dst_port = dst.getsockname()
    while True:
        try:
            buffer = src.recv(4096)
            if len(buffer) > 0:
                dst.send(handle(buffer, direction, src_address, src_port, dst_address, dst_port))
        except Exception as e:
            logging.error(repr(e))
            break
    logging.warning(f"Closing connect {src_address, src_port}! ")
    src.close()
    logging.warning(f"Closing connect {dst_address, dst_port}! ")
    dst.close()


def server(local_host, local_port, remote_host, remote_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((local_host, local_port))
    server_socket.listen(0x40)
    logging.info(f"Server started {local_host, local_port}")
    logging.info(f"Connect to {local_host, local_port} to get the content of {remote_host, remote_port}")
    while True:
        src_socket, src_address = server_socket.accept()
        logging.info(f"[Establishing] {src_address} -> {local_host, local_port} -> ? -> {remote_host, remote_port}")
        try:
            dst_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dst_socket.connect((remote_host, remote_port))
            logging.info(f"[OK] {src_address} -> {local_host, local_port} -> {dst_socket.getsockname()} -> {remote_host, remote_port}")
            s = threading.Thread(target=transfer, args=(dst_socket, src_socket, False))
            r = threading.Thread(target=transfer, args=(src_socket, dst_socket, True))
            s.start()
            r.start()
        except Exception as e:
            logging.error(repr(e))


def main():
    port_config_list = []
    with open("port-forward.config") as f:
        for line in f.readlines():
            config_list = line.strip().split()
            port_config = PortConfig(
                    config_list[0],
                    int(config_list[1]),
                    config_list[2],
                    int(config_list[3])
                    )
            port_config_list.append(
                port_config
            )
    for config in port_config_list:
        threading.Thread(
            target =  server,
            args= (
                config.localhost, 
                config.localport, 
                config.remotehost, 
                config.remoteport
            )
        ).start()
    while True:
        time.sleep(60)
            
            
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--listen-host", help="the host to listen", required=True)
    # parser.add_argument("--listen-port", type=int, help="the port to bind", required=True)
    # parser.add_argument("--connect-host", help="the target host to connect", required=True)
    # parser.add_argument("--connect-port", type=int, help="the target port to connect", required=True)
    # args = parser.parse_args()
    # server(args.listen_host, args.listen_port,
    #        args.connect_host, args.connect_port)


if __name__ == "__main__":
    main()
