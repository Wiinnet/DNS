import socket
from dnslib import DNSRecord, DNSHeader, RR
from dnslib.dns import A, QTYPE

DNS_SERVER_IP = "127.0.0.1"
DNS_SERVER_PORT = 53
DOMAIN = "wiinnet.net"
IP_ADDRESS = "192.168.1.1" 

def handle_query(data, addr, server_socket):
    try:
        dns_request = DNSRecord.parse(data)
        query_name = str(dns_request.q.qname)

        if query_name == DOMAIN + ".":
            print(f"Requête DNS pour {query_name} de {addr}")

            dns_response = DNSRecord()
            dns_response.header = DNSHeader(id=dns_request.header.id, qr=1, aa=1, ra=1)
            dns_response.add_answer(RR(query_name, QTYPE.A, rdata=A(IP_ADDRESS), ttl=60))

            server_socket.sendto(dns_response.pack(), addr)
        else:
            print(f"Requête inconnue pour {query_name} de {addr}")
    except Exception as e:
        print(f"Erreur dans la gestion de la requête: {e}")

def start_dns_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((DNS_SERVER_IP, DNS_SERVER_PORT))
    print(f"Serveur DNS démarré sur {DNS_SERVER_IP}:{DNS_SERVER_PORT}")

    while True:
        try:
            data, addr = server_socket.recvfrom(512)
            handle_query(data, addr, server_socket)
        except KeyboardInterrupt:
            print("\nArrêt du serveur DNS.")
            break

if __name__ == "__main__":
    start_dns_server()
