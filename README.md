# 🕵️‍♂️ ShadowNode Hunter

*Read this in [Turkish](#türkçe)*

ShadowNode Hunter is a Python and Scapy-based Blue Team (Defensive Security) tool developed to detect hidden devices and potential security threats on a Local Area Network (LAN). It is designed to collect anomaly data (dataset generation) for Machine Learning-based Intrusion Detection Systems (IDS) and network analysis applications.

## 🚀 How It Works (Layer 2 vs. Layer 3)

An attacker who has infiltrated the network or malware attempting lateral movement often drops ICMP (Ping) requests to hide from standard discovery tools. However, to communicate on the network, the device must still respond to ARP (Address Resolution Protocol) requests. ShadowNode Hunter exploits this behavior:

*   **Layer 2 (Physical Layer):** Performs an ARP scan to discover physically connected devices.
*   **Layer 3 (Logical Layer):** Sends ICMP (Ping) packets *only* to the devices physically detected in the previous step.
*   **Analysis Engine:** Targets that respond to ARP but drop/reject Ping requests are immediately flagged as a "Shadow Node".

## 🛠️ Features

*   **Smart Scanning:** Minimizes network noise by targeting ICMP scans only at live devices discovered via ARP, rather than scanning the entire subnet.
*   **Hidden Device Detection:** Identifies devices hiding behind firewalls or actively dropping ICMP packets.
*   **IDS & ML Integration:** Logs detected normal and abnormal device behaviors in real-time to a `shadow_nodes_dataset.csv` file, structuring the data to train Machine Learning models.

## 💻 Installation & Usage

Python 3 and the Scapy library are required to run the project.

```bash
# Install the required library
pip3 install scapy
```

Run the tool with root privileges (required for Scapy to open raw sockets):

```bash
sudo python3 shadow_hunter.py
```

---

# Türkçe

ShadowNode Hunter, yerel ağ (LAN) üzerindeki gizlenmiş cihazları ve potansiyel güvenlik tehditlerini tespit etmek için geliştirilmiş, Python ve Scapy tabanlı bir Blue Team (Savunma) aracıdır. Makine öğrenmesi tabanlı Saldırı Tespit Sistemleri (IDS) ve ağ analiz uygulamaları için anomali verisi toplama (Dataset oluşturma) amacıyla tasarlanmıştır.

## 🚀 Çalışma Mantığı (Layer 2 vs Layer 3)

Ağa sızmış bir saldırgan veya yatay hareket etmeye çalışan bir zararlı yazılım (malware), genellikle keşif araçlarından gizlenmek için cihazının Ping (ICMP) isteklerine cevap vermesini engeller. Ancak aynı ağda iletişim kurabilmek için ARP (Adres Çözümleme Protokolü) isteklerine cevap vermek zorundadır. ShadowNode Hunter bu zafiyeti şu şekilde kullanır:

*   **Layer 2 (Fiziksel Katman):** Ağdaki cihazları bulmak için ARP taraması yapar.
*   **Layer 3 (Mantıksal Katman):** Sadece fiziksel olarak tespit edilen cihazlara ICMP (Ping) paketi gönderir.
*   **Analiz Motoru:** ARP'a cevap verip, Ping isteğini reddeden (havada düşüren) hedefleri "Gölge Cihaz (Shadow Node)" olarak işaretler.

## 🛠️ Özellikler

*   **Akıllı Tarama:** ICMP taramasını tüm ağa değil, sadece ARP ile tespit edilen canlı cihazlara yaparak ağ gürültüsünü (noise) minimuma indirir.
*   **Gizli Cihaz Tespiti:** Firewall arkasına saklanan veya ICMP paketlerini drop eden cihazları tespit eder.
*   **IDS & ML Entegrasyonu:** Tespit edilen normal ve anormal cihaz davranışlarını, makine öğrenmesi (Machine Learning) modellerini eğitmek üzere anlık olarak `shadow_nodes_dataset.csv` dosyasına loglar.

## 💻 Kurulum ve Kullanım

Projeyi çalıştırmak için sisteminizde Python 3 ve Scapy kütüphanesinin kurulu olması gerekmektedir.

```bash
# Gerekli kütüphaneyi kurun
pip3 install scapy
```

Aracı root yetkileriyle (Raw socket açabilmek için) çalıştırın:

```bash
sudo python3 shadow_hunter.py
```
