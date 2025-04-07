import socket

class UDPSender:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port

    def send(self, name: str, payload: str):
        """
        Sends a message over UDP in the format: 'name:payload\\n'
        - `name`: sensor name or device label
        - `payload`: comma-separated values or single reading
        """
        message = f"{name}:{payload}\n"
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.sendto(message.encode(), (self.ip, self.port))
        finally:
            sock.close()

