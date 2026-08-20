from scapy.all import *
import csv
from datetime import datetime

conf.verb = 0

def arp_scan(ip_range):
    print(f"[*] {ip_range} için ARP Taraması başlatılıyor...")
  
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_range)
    answered, _ = srp(arp_request, timeout=2)
    
    arp_alive = []
    for snd, rcv in answered:
        arp_alive.append(rcv.psrc) 
    
    print(f"[+] ARP Taraması bitti. Toplam {len(arp_alive)} cihaz fiziksel olarak ağda bulundu.")
    return arp_alive

def icmp_scan(ip_list):
    print("[*] Bulunan cihazlara ICMP (Ping) Taraması başlatılıyor...")
    icmp_alive = []
    
   
    for ip in ip_list:
        ping_pkt = IP(dst=ip) / ICMP()
        response = sr1(ping_pkt, timeout=0.5)
        
    
        if response:
            icmp_alive.append(ip)
            
    print(f"[+] ICMP Taraması bitti. {len(icmp_alive)} cihaz ping isteğine cevap verdi.")
    return icmp_alive

def main():
    # Kendi Metasploitable/Sanal ağına göre buradaki IP bloğunu güncelleyebilirsin
    hedef_ag ="10.0.2.0/24" 
    
    arp_cihazlar = arp_scan(hedef_ag)
    
    if not arp_cihazlar:
        print("[-] Ağda hiçbir cihaz bulunamadı. Program kapatılıyor.")
        return
    icmp_cihazlar = icmp_scan(arp_cihazlar)
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
    dosya_adi = "shadow_nodes_dataset.csv"
    zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(dosya_adi, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["Tarih", "IP_Adresi", "Davranis_Tipi"])
        
        for ip in arp_cihazlar:
            durum = "Gizli_Cihaz" if ip in golge_cihazlar else "Normal_Cihaz"
            writer.writerow([zaman, ip, durum])
    
    print(f"\n[+] Analiz sonuçları makine öğrenmesi modellerinde kullanılmak üzere '{dosya_adi}' dosyasına işlendi.")

if __name__ == "__main__":
    main()
