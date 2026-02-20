from scapy.all import sniff
from datetime import datetime
import time
from .parser import parse_packet

class PacketCapture:
    def __init__(self, interface=None):
        self.interface = interface
        self.packets = []
        self.count = 0
        self.start_time = None
        
    def _handler(self, pkt):
        parsed = parse_packet(pkt)
        if parsed:
            parsed['timestamp'] = datetime.now().isoformat()
            parsed['time_epoch'] = time.time()
            self.packets.append(parsed)
            self.count += 1
            if self.count % 10 == 0:
                print(f"\rСобрано пакетов: {self.count}", end='')
    
    def start(self, packet_limit=100):
        print(f"[*] Запуск захвата на интерфейсе {self.interface}")
        print(f"[*] Лимит: {packet_limit} пакетов")
        
        self.start_time = time.time()
        self.packets = []
        self.count = 0
        
        try:
            sniff(
                iface=self.interface,
                prn=self._handler,
                count=packet_limit,
                store=False
            )
        except Exception as e:
            print(f"\n[!] Ошибка: {e}")
            if 'npcap' in str(e).lower():
                print("[!] Проверь установку Npcap")
        
        duration = time.time() - self.start_time
        print(f"\n[+] Собрано {self.count} пакетов за {duration:.1f} сек")
        return self.packets
