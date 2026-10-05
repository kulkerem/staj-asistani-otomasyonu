# 🚀 Staj Başvuru ve Takip Otomasyonu

Bu proje, yazılım ve teknoloji stajı arayan öğrencilerin başvuru süreçlerini otomatikleştirmek ve hızlandırmak için geliştirilmiş kişisel bir asistan aracıdır.

## 🛠️ Kullanılan Teknolojiler
* **Python** (Requests, BeautifulSoup, Telebot, Schedule)
* **JavaScript & HTML** (Chrome Extension Manifest V3)
* **Telegram Bot API** (Anlık Bildirimler)
* **Git & GitHub** (Versiyon Kontrolü)

## 📌 Projenin Bileşenleri

### 1. Youthall Akıllı Telegram Botu (`staj_botu.py`)
* Youthall üzerindeki staj ilanlarını periyodik olarak tarar.
* Belirlenen anahtar kelimelere (*yazılım, bilgisayar, software, developer, it, mühendis, veri, data*) göre filtreleme yapar.
* Sadece hedefe uygun staj fırsatlarını anlık olarak Telegram üzerinden bildirir.
* Tekrar eden bildirimleri engellemek için hafıza mekanizmasına sahiptir.

### 2. Chrome Form Doldurma Asistanı (Chrome Extension)
* Manifest V3 standartlarına uygundur.
* Kullanıcının temel bilgilerini (Ad Soyad, E-posta, GitHub/LinkedIn URL) tarayıcının güvenli hafızasında saklar.
* Şirketlerin başvuru formlarındaki ilgili input alanlarını otomatik olarak algılar ve tek tıkla doldurur.

## 🚀 Kurulum ve Çalıştırma

### Python Botunu Çalıştırma:
1. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install requests beautifulsoup4 telebot schedule