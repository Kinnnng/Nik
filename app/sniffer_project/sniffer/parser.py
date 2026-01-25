# добавить время получения пакета
# решить проблему с Npcap



from scapy.layers.inet import IP, TCP, UDP, ICMP
#Scapy хранит пакет как “слоёный пирог” из протоколов (слоёв).

def parse_packet(pkt) -> dict | None:
    if IP not in pkt:
        return None
# dict — если пакет понятный и его можно разобрать
# None — если пакет не содержит IP-слоя
# Дальше проверям это слой IP или нет
# Если в пакете нет IPv4, то мы его пропускаем, чтобы дальше не словить ошибку
    ip = pkt[IP] # обращаемся к полям IP как к атрибутам
    row = {          
        "src": ip.src, #IP-адрес отправителя
        "dst": ip.dst, #IP-адрес получателя
        "proto": ip.proto, #номер протокола внутри IP
        "len": len(pkt), #размер пакета в байтах
    }
# Транспортый уровень

    if TCP in pkt:
        tcp = pkt[TCP] # достаём TCP слой
        row.update({    #добавляем новые поля в уже созданный словарь
            "l4": "TCP", # 4 проткол
            "sport": int(tcp.sport), #порт отправителя
            "dport": int(tcp.dport), #порт получателя
            "flags": str(tcp.flags),              # трёх этапное рукапожатие
        })
    elif UDP in pkt:
        udp = pkt[UDP]
        row.update({
            "l4": "UDP",
            "sport": int(udp.sport),
            "dport": int(udp.dport),
            "flags": "",
        })
    elif ICMP in pkt:
        icmp = pkt[ICMP]
        row.update({
            "l4": "ICMP",
            "sport": "", #здесь порты не исползуются
            "dport": "",
            "flags": f"type={icmp.type}",
        })
    else:
        row.update({"l4": "OTHER", "sport": "", "dport": "", "flags": ""}) #пустые

    return row
