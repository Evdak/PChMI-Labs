from laba1.main import main
from pywebio import start_server


if __name__ == '__main__':
    start_server(main, websocket_ping_interval=30)
