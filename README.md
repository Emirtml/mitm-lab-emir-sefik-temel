# Three-Role Localhost MITM Simulation Lab

**Author:** Emir Şefik Temel  
**Course / Domain:** Cybersecurity & Network Security Lab  

## Overview

This repository presents an educational, localhost-based **Man-in-the-Middle (MITM)** attack simulation built with Python. Designed strictly for controlled academic environments, the project demonstrates how unencrypted network traffic (`HTTP`/plain TCP sockets) can be intercepted, inspected, and tampered with in transit without the communicating parties realizing it.

All communication takes place exclusively over the local loopback interface (`127.0.0.1`). No real network interfaces are sniffed, and no ARP spoofing or external packet injection is performed.

---

## System Architecture & Roles

The lab isolates the attack scenario into three independent Python scripts representing the core actors of a MITM interception:

1. **Client (`client.py` — Role 1: Victim)**
   * Initiates a JSON-formatted payment transaction (`amount: 100`) intended for the destination server.
   * Connects to the proxy port (`127.0.0.1:9000`) instead of reaching the legitimate server directly, simulating traffic redirection.

2. **Attacker (`attacker.py` — Role 2: Man-in-the-Middle Proxy)**
   * Listens on `127.0.0.1:9000`, intercepts the incoming payload from the client, and logs the original data.
   * Modifies the transaction payload in real time (changing `amount` from `100` to `900` and injecting a custom note) before forwarding it upstream to the server (`127.0.0.1:9001`).
   * Utilizes **Scapy** to construct an offline in-memory `IP / TCP / Raw` packet representation of the altered payload and outputs its layer headers to the terminal for packet-level inspection.

3. **Server (`server.py` — Role 3: Destination Host)**
   * Listens on `127.0.0.1:9001` and processes incoming requests.
   * Because the connection lacks cryptographic integrity verification or authentication, the server accepts the manipulated `900` value as legitimate and returns an acknowledgment through the proxy.

---

## Project Structure

```text
mitm-lab-emir-sefik-temel/
├── server.py           # Destination server listening on port 9001
├── attacker.py         # Localhost MITM proxy (port 9000) & Scapy packet analyzer
├── client.py           # Client sending the initial payment payload
├── requirements.txt    # Python dependencies (scapy)
└── README.md           # Project documentation
