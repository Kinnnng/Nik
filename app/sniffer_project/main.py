#!/usr/bin/env python3
from .capture import PacketCapture
from .storage import PacketStorage
import os

def main():
    print("="*50)
    print("СЕТЕВОЙ СНИФФЕР")
    print("="*50)
    
    if os.name == 'nt':
        print("[!] Windows: Убедись что Npcap установлен")
        print("    https://npcap.com")
    
    interface = input("Интерфейс (Enter - по умолчанию): ").strip() or None
    try:
        limit = int(input("Количество пакетов (100): ") or "100")
    except:
        limit = 100
    
    capture = PacketCapture(interface)
    packets = capture.start(limit)
    
    if not packets:
        print("[!] Нет пакетов для сохранения")
        return
    
    print("\n[*] Сохранение результатов...")
    storage = PacketStorage()
    storage.to_json(packets)
    storage.to_csv(packets)
    storage.to_text(packets)
    
    print("\n[+] Готово!")

if __name__ == "__main__":
    main()
