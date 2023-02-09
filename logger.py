import datetime
from threading import Thread
import requests
from aiohttp import web
import socket
import subprocess

log_file = '{date:%H_%M_%S_%d_%m_%Y}.txt'.format(date=datetime.datetime.now())


def get_port():
    sock = socket.socket()
    sock.bind(("0.0.0.0", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


def log(s):
    print(s.replace("\n", ""))
    with open(log_file, "a") as logs:
        logs.write(s)


def server_emu(tcp_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r = requests.get("http://54.148.133.180:30000/dc/helloWorld").json()
    server.connect((r['ipAddress'], r['port']))
    client.bind(('127.0.0.1', tcp_port))
    client.listen(1)
    conn, addr = client.accept()
    while True:
        request = conn.recv(4096)
        log(f"se: {request}\n")
        server.sendall(request)
        response = server.recv(4096)
        log(f"re: {response}\n")
        log("\n")
        conn.sendall(response)


def main():
    print("=================================================")
    print("==== Dark and Darker server logger by gookie ====")
    web_port = get_port()
    tcp_port = get_port()
    routes = web.RouteTableDef()

    with open('.\\DungeonCrawler\\Binaries\\Win64\\steam_appid.txt', "w") as steam_appid:
        steam_appid.write('2258570')

    @routes.get('/dc/helloWorld')
    async def handler(r):
        return web.json_response({'ipAddress': '127.0.0.1', 'port': tcp_port})

    app = web.Application()
    app.add_routes(routes)
    Thread(target=server_emu, args=(tcp_port, )).start()
    subprocess.Popen(f'DungeonCrawler.exe -server=127.0.0.1:{web_port}')
    web.run_app(app, port=web_port)


if __name__ == '__main__':
    main()
