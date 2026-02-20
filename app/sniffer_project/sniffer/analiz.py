#сильно под сомнением, сделать проще
# комиты


from collections import Counter, defaultdict
from datetime import datetime
import statistics

class PacketAnalyzer:
    @staticmethod
    def get_protocol_stats(packets):
        """Считает протоколы"""
        return Counter(p.get('l4', 'OTHER') for p in packets)
    
    @staticmethod
    def get_ip_stats(packets):
        """Считает отправителей и получателей"""
        senders = defaultdict(int)
        receivers = defaultdict(int)
        
        for p in packets:
            if p.get('src'):
                senders[p['src']] += p.get('len', 0)
            if p.get('dst'):
                receivers[p['dst']] += p.get('len', 0)
        
        
        top_senders = sorted(senders.items(), key=lambda x: x[1], reverse=True)[:5]
        top_receivers = sorted(receivers.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'top_senders': dict(top_senders),
            'top_receivers': dict(top_receivers),
            'unique_senders': len(senders),
            'unique_receivers': len(receivers)
        }
    
    @staticmethod
    def get_port_stats(packets):
        """Считает порты"""
        ports = defaultdict(int)
        
        for p in packets:
            dport = p.get('dport')
            if dport and str(dport).isdigit():
                ports[int(dport)] += 1
        
        return dict(sorted(ports.items(), key=lambda x: x[1], reverse=True)[:10])
    
    @staticmethod
    def get_size_stats(packets):
        """Считает размеры пакетов"""
        sizes = [p.get('len', 0) for p in packets if p.get('len')]
        
        if not sizes:
            return {}
        
        return {
            'total_bytes': sum(sizes),
            'avg_size': statistics.mean(sizes),
            'min_size': min(sizes),
            'max_size': max(sizes),
            'jumbo_packets': len([s for s in sizes if s >= 1500])
        }
    
    @staticmethod
    def get_conversations(packets):
        """Кто с кем общается"""
        chats = defaultdict(int)
        
        for p in packets:
            src = p.get('src')
            dst = p.get('dst')
            if src and dst:
                pair = f"{src} → {dst}"
                chats[pair] += 1
        
        return dict(sorted(chats.items(), key=lambda x: x[1], reverse=True)[:5])
    
    @staticmethod
    def get_summary(packets):
        """Краткая сводка"""
        return {
            'total': len(packets),
            'protocols': PacketAnalyzer.get_protocol_stats(packets),
            'ips': PacketAnalyzer.get_ip_stats(packets),
            'ports': PacketAnalyzer.get_port_stats(packets),
            'sizes': PacketAnalyzer.get_size_stats(packets),
            'conversations': PacketAnalyzer.get_conversations(packets)
        }
    
    @staticmethod
    def print_summary(packets):
        """Вывод на экран"""
        s = PacketAnalyzer.get_summary(packets)
        
        print("\n" + "="*50)
        print("СТАТИСТИКА")
        print("="*50)
        print(f"Пакетов: {s['total']}")
        
        print("\nПротоколы:")
        for proto, count in s['protocols'].items():
            print(f"  {proto}: {count}")
        
        print("\nОтправители:")
        for ip, bytes_count in s['ips']['top_senders'].items():
            print(f"  {ip}: {bytes_count} байт")
        
        print("\nПорты:")
        for port, count in list(s['ports'].items())[:5]:
            print(f"  {port}: {count}")
        
        if s['sizes']:
            print(f"\nРазмеры: мин={s['sizes']['min_size']}, "
                  f"сред={s['sizes']['avg_size']:.0f}, "
                  f"макс={s['sizes']['max_size']} байт")
        
        print("\nРазговоры:")
        for chat, count in s['conversations'].items():

            print(f"  {chat}: {count} пакетов")
