# 🕵️‍♂️ ShadowNode Hunter

ShadowNode Hunter, yerel ağ (LAN) üzerindeki gizlenmiş cihazları ve potansiyel güvenlik tehditlerini tespit etmek için geliştirilmiş, Python ve Scapy tabanlı bir Blue Team (Savunma) aracıdır.

Makine öğrenmesi tabanlı Saldırı Tespit Sistemleri (IDS) ve ağ analiz uygulamaları için anomali verisi toplama (Dataset oluşturma) amacıyla tasarlanmıştır.

## 🚀 Çalışma Mantığı (Layer 2 vs Layer 3)

Ağa sızmış bir saldırgan veya yatay hareket etmeye çalışan bir zararlı yazılım (malware), genellikle keşif araçlarından gizlenmek için cihazının Ping (ICMP) isteklerine cevap vermesini engeller. Ancak aynı ağda iletişim kurabilmek için ARP (Adres Çözümleme Protokolü) isteklerine cevap vermek zorundadır.

ShadowNode Hunter bu zafiyeti şu şekilde kullanır:
1. **Layer 2 (Fiziksel Katman):** Ağdaki cihazları bulmak için ARP taraması yapar.
2. **Layer 3 (Mantıksal Katman):** Sadece fiziksel olarak tespit edilen cihazlara ICMP (Ping) paketi gönderir.
3. **Analiz Motoru:** ARP'a cevap verip, Ping isteğini reddeden (havada düşüren) hedefleri **"Gölge Cihaz (Shadow Node)"** olarak işaretler.

## 🛠️ Özellikler

- **Akıllı Tarama:** ICMP taramasını tüm ağa değil, sadece ARP ile tespit edilen canlı cihazlara yaparak ağ gürültüsünü (noise) minimuma indirir.
- **Gizli Cihaz Tespiti:** Firewall arkasına saklanan veya ICMP paketlerini drop eden cihazları tespit eder.
- **IDS & ML Entegrasyonu:** Tespit edilen normal ve anormal cihaz davranışlarını, makine öğrenmesi (Machine Learning) modellerini eğitmek üzere anlık olarak `shadow_nodes_dataset.csv` dosyasına loglar.

## 💻 Kurulum ve Kullanım

Projeyi çalıştırmak için sisteminizde Python 3 ve Scapy kütüphanesinin kurulu olması gerekmektedir.

```bash
# Gerekli kütüphaneyi kurun
pip3 install scapy

# Aracı root yetkileriyle (Raw socket açabilmek için) çalıştırın
sudo python3 shadow_hunter.py
