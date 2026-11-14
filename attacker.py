"""Role 2: a deliberately vulnerable localhost proxy for classroom use only.

It accepts exactly one client request, modifies an example field, forwards it to
the local server, then prints a Scapy-built *offline* example packet. It never
sniffs an interface and never sends packets.
"""
import json
import socket

from scapy.all import IP, TCP, Raw  # type: ignore[import-untyped]

LISTEN_HOST, LISTEN_PORT = "127.0.0.1", 9000
SERVER_HOST, SERVER_PORT = "127.0.0.1", 9001


def receive_line(connection: socket.socket) -> bytes:
    data = b""
    while not data.endswith(b"\n"):
        chunk = connection.recv(4096)
        if not chunk:
            break
        data += chunk
    return data


def show_offline_packet(payload: bytes) -> None:
    """Analyse a crafted example packet in memory; do not transmit it."""
    packet = IP(src="127.0.0.1", dst="127.0.0.1") / TCP(sport=50123, dport=9001, flags="PA") / Raw(load=payload)
    print("[ATTACKER][SCAPY] Sahte/örnek paket analizi (ağa gönderilmedi):", flush=True)
    print(f"  IP: {packet[IP].src} -> {packet[IP].dst} | protocol={packet[IP].proto}", flush=True)
    print(f"  TCP: {packet[TCP].sport} -> {packet[TCP].dport} | flags={packet[TCP].flags}", flush=True)
    print(f"  Raw: {packet[Raw].load.decode('utf-8')}", flush=True)


def main() -> None:
    print("[ATTACKER] MITM laboratuvarı | Hazırlayan: Emir Şefik Temel", flush=True)
    print("[ATTACKER] Yalnızca localhost proxy; paket dinleme/gönderme yapılmaz.", flush=True)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((LISTEN_HOST, LISTEN_PORT))
        listener.listen(1)
        print(f"[ATTACKER] {LISTEN_HOST}:{LISTEN_PORT} üzerinde istemci bekleniyor.", flush=True)
        client, address = listener.accept()
        with client:
            original = json.loads(receive_line(client).decode("utf-8"))
            print(f"[ATTACKER] İstemci bağlandı: {address}", flush=True)
            print(f"[ATTACKER] Yakalanan veri: {original}", flush=True)
            altered = {**original, "amount": 900, "note": "Mallory tarafından örnekte değiştirildi"}
            print(f"[ATTACKER] Değiştirilen veri: {altered}", flush=True)
            encoded = (json.dumps(altered, ensure_ascii=False) + "\n").encode("utf-8")
            show_offline_packet(encoded.rstrip())
            with socket.create_connection((SERVER_HOST, SERVER_PORT), timeout=5) as upstream:
                upstream.sendall(encoded)
                reply = receive_line(upstream)
            client.sendall(reply)
            print("[ATTACKER] Sunucu yanıtı istemciye iletildi.", flush=True)


if __name__ == "__main__":
    main()
