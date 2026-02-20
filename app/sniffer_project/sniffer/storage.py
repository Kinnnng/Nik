import json
import csv
from datetime import datetime

class PacketStorage:
    @staticmethod
    def to_json(packets, filename=None):
        if not filename:
            filename = f"packets_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(packets, f, indent=2, ensure_ascii=False)
        print(f"[+] Сохранено в {filename}")
        return filename
    
    @staticmethod
    def to_csv(packets, filename=None):
        if not filename:
            filename = f"packets_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        if packets:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=packets[0].keys())
                writer.writeheader()
                writer.writerows(packets)
            print(f"[+] Сохранено в {filename}")
            return filename
    
    @staticmethod
    def to_text(packets, filename=None):
        if not filename:
            filename = f"packets_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            for i, pkt in enumerate(packets, 1):
                f.write(f"Пакет {i}:\n")
                for key, value in pkt.items():
                    f.write(f"  {key}: {value}\n")
                f.write("-" * 40 + "\n")
        print(f"[+] Сохранено в {filename}")
        return filename
