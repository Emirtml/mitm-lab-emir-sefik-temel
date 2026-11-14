"""Role 3: localhost-only destination server for the MITM lab."""
import json
import socket

HOST, PORT = "127.0.0.1", 9001


def receive_line(connection: socket.socket) -> bytes:
    data = b""
    while not data.endswith(b"\n"):
        chunk = connection.recv(4096)
        if not chunk:
            break
        data += chunk
    return data


def main() -> None:
    print("[SERVER] MITM laboratuvarı | Hazırlayan: Emir Şefik Temel", flush=True)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((HOST, PORT))
        listener.listen(1)
        print(f"[SERVER] {HOST}:{PORT} üzerinde bağlantı bekleniyor.", flush=True)
        connection, address = listener.accept()
        with connection:
            raw = receive_line(connection)
            message = json.loads(raw.decode("utf-8"))
            print(f"[SERVER] Proxy bağlantısı kabul edildi: {address}", flush=True)
            print(f"[SERVER] Ulaşan veri: {message}", flush=True)
            reply = {"status": "received", "amount_seen": message["amount"]}
            connection.sendall((json.dumps(reply) + "\n").encode("utf-8"))
            print("[SERVER] Yanıt proxy üzerinden geri gönderildi.", flush=True)


if __name__ == "__main__":
    main()
