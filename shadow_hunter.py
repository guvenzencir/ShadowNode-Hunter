from scapy.all import *
import csv
from datetime import datetime

# Scapy'nin ekrandaki gereksiz uyarı/bilgi mesajlarını kapatalım ki terminalimiz temiz kalsın
conf.verb = 0

def arp_scan(ip_range):
    print(f"[*] {ip_range} için ARP Taraması başlatılıyor...")
    # Broadcast MAC adresine ARP isteği hazırlıyoruz
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_range)
    answered, _ = srp(arp_request, timeout=2)
    
    arp_alive = []
    for snd, rcv in answered:
        arp_alive.append(rcv.psrc) # Sadece cevap verenlerin IP adreslerini listeye ekliyoruz
    
    print(f"[+] ARP Taraması bitti. Toplam {len(arp_alive)} cihaz fiziksel olarak ağda bulundu.")
    return arp_alive

def icmp_scan(ip_list):
    print("[*] Bulunan cihazlara ICMP (Ping) Taraması başlatılıyor...")
    icmp_alive = []
    
    # Tüm ağı baştan taramak yerine, SADECE ARP ile bulduğumuz cihazların kapısını çalıyoruz.
    # Bu sayede ağda gereksiz trafik (noise) yaratmamış oluyoruz.
    for ip in ip_list:
        ping_pkt = IP(dst=ip) / ICMP()
        response = sr1(ping_pkt, timeout=0.5)
        
        # Eğer cihazdan bir echo-reply (cevap) geldiyse listeye ekle
        if response:
            icmp_alive.append(ip)
            
    print(f"[+] ICMP Taraması bitti. {len(icmp_alive)} cihaz ping isteğine cevap verdi.")
    return icmp_alive

def main():
    # Kendi Metasploitable/Sanal ağına göre buradaki IP bloğunu güncelleyebilirsin
    hedef_ag ="10.0.2.0/24" 
    
    # 1. Aşama: ARP Taraması
    arp_cihazlar = arp_scan(hedef_ag)
    
    if not arp_cihazlar:
        print("[-] Ağda hiçbir cihaz bulunamadı. Program kapatılıyor.")
        return

    # 2. Aşama: ICMP Taraması
    icmp_cihazlar = icmp_scan(arp_cihazlar)
    
    # 3. Aşama: Karşılaştırma ve Analiz
    golge_cihazlar = []
    print("\n" + "="*50)
    print(" GÖLGE CİHAZ (SHADOW NODE) ANALİZ SONUÇLARI")
    print("="*50)
    
    for ip in arp_cihazlar:
        if ip not in icmp_cihazlar:
            print(f"[!] DİKKAT: {ip} ARP'a yanıt veriyor ama Ping'i reddediyor! (Gölge Cihaz / Firewall Aktif)")
            golge_cihazlar.append(ip)
        else:
            print(f"[+] {ip} Normal davranış sergiliyor.")

    # 4. Aşama: IDS ve Makine Öğrenmesi İçin CSV Çıktısı
    dosya_adi = "shadow_nodes_dataset.csv"
    zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(dosya_adi, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Dosya ilk kez oluşturuluyorsa en üste başlıkları (Feature isimlerini) yazalım
        if file.tell() == 0:
            writer.writerow(["Tarih", "IP_Adresi", "Davranis_Tipi"])
        
        for ip in arp_cihazlar:
            durum = "Gizli_Cihaz" if ip in golge_cihazlar else "Normal_Cihaz"
            writer.writerow([zaman, ip, durum])
    
    print(f"\n[+] Analiz sonuçları makine öğrenmesi modellerinde kullanılmak üzere '{dosya_adi}' dosyasına işlendi.")

if __name__ == "__main__":
    main()
