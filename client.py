"""Role 1: localhost-only client for the MITM lab."""
import json
import socket

PROXY_HOST, PROXY_PORT = "127.0.0.1", 9000


def receive_line(connection: socket.socket) -> bytes:
    data = b""
    while not data.endswith(b"\n"):
        chunk = connection.recv(4096)
        if not chunk:
            break
        data += chunk
    return data


def main() -> None:
    message = {"from": "Alice", "to": "Bob", "amount": 100, "note": "Laboratuvar örneği"}
    print("[CLIENT] MITM laboratuvarı | Hazırlayan: Emir Şefik Temel", flush=True)
    print(f"[CLIENT] Proxy'ye gönderilen veri: {message}", flush=True)
    with socket.create_connection((PROXY_HOST, PROXY_PORT), timeout=5) as proxy:
        proxy.sendall((json.dumps(message, ensure_ascii=False) + "\n").encode("utf-8"))
        reply = json.loads(receive_line(proxy).decode("utf-8"))
    print(f"[CLIENT] Proxy'den gelen sunucu yanıtı: {reply}", flush=True)
    print("[CLIENT] Sonuç: Sunucu 900 TL gördü; istemci 100 TL göndermişti.", flush=True)


if __name__ == "__main__":
    main()
