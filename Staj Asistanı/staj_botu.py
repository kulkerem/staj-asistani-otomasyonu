import time
import requests
from bs4 import BeautifulSoup
import telebot
import schedule

# Telegram Bot Ayarları (Kendi Token ve Chat ID'ni buraya yazmalısın)
TOKEN = "BURAYA_TELEGRAM_BOT_TOKEN_YAZ"
CHAT_ID = "BURAYA_CHAT_ID_YAZ"

bot = telebot.TeleBot(TOKEN)

# Daha önce gönderilen ilanların ID'lerini saklayarak mükerrer (tekrar) bildirimi engelliyoruz
gonderilen_ilanlar = set()


def telegrama_gonder(mesaj):
  try:
    bot.send_message(CHAT_ID, mesaj, parse_mode="Markdown")
  except Exception as e:
    print(f"Telegram mesajı gönderilirken hata oluştu: {e}")


# 1. Kaynak: Youthall Staj İlanları Taraması
def youthall_tara():
  print("INFO: Youthall taranıyor...")
  url = "https://youthall.com/tr/ilanlar/"  # Örnek hedef URL
  headers = {"User-Agent": "Mozilla/5.0"}

  try:
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
      print("Youthall sayfasına erişilemedi.")
      return

    soup = BeautifulSoup(response.text, "html.parser")
    # Not: Sitenin güncel HTML yapısına göre bu seçiciler (class/tag) uyarlanabilir
    ilanlar = soup.find_all(
        "div", class_="job-card"
    )  # Örnek kart seçici

    anahtar_kelimeler = [
        "yazılım",
        "bilgisayar",
        "software",
        "developer",
        "it",
        "mühendis",
        "veri",
        "data",
    ]

    for ilan in ilanlar:
      baslik = ilan.text.lower()
      # Anahtar kelime filtrelemesi
      if any(kelime in baslik for kelime in anahtar_kelimeler):
        ilan_linki = ilan.find("a")["href"] if ilan.find("a") else "Link yok"
        if ilan_linki not in gonderilen_ilanlar:
          gonderilen_ilanlar.add(ilan_linki)
          mesaj = (
              "🚀 *Yeni Staj Fırsatı (Youthall)*\n\n"
              f"📌 *İlan/Detay:* {ilan.text.strip()[:100]}...\n"
              f"🔗 [İlana Git]({ilan_linki})"
          )
          telegrama_gonder(mesaj)
  except Exception as e:
    print(f"Youthall tarama hatası: {e}")


# 2. Kaynak: Toptalent Staj Programları Taraması
def toptalent_tara():
  print("INFO: Toptalent taranıyor...")
  url = "https://toptalent.co/staj-ilanlari"  # Örnek hedef URL
  headers = {"User-Agent": "Mozilla/5.0"}

  try:
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
      return

    soup = BeautifulSoup(response.text, "html.parser")
    ilanlar = soup.find_all("div", class_="job-item")  # Örnek seçici

    for ilan in ilanlar:
      metin = ilan.text.lower()
      if any(k in metin for k in ["yazılım", "it", "stajyer", "developer"]):
        link = ilan.find("a")["href"] if ilan.find("a") else ""
        if link and link not in gonderilen_ilanlar:
          gonderilen_ilanlar.add(link)
          mesaj = (
              "🎯 *Yeni Fırsat (Toptalent)*\n\n"
              f"📌 *Detay:* {ilan.text.strip()[:100]}...\n"
              f"🔗 [İlana Git]({link})"
          )
          telegrama_gonder(mesaj)
  except Exception as e:
    print(f"Toptalent tarama hatası: {e}")


# 3. Kaynak: İstanbul Teknoloji Projeleri ve Yarışmalar (Hackathon / İBB / Teknofest vb.)
def istanbul_yarismalari_tara():
  print("INFO: İstanbul teknoloji yarışmaları ve hackathonlar taranıyor...")
  # Örnek olarak İstanbul odaklı yarışma duyurularının bulunduğu bir platform
  url = "https://www.ibb.istanbul/uluslararasi-veya-teknoloji-yarismalari"  # Örnek
  headers = {"User-Agent": "Mozilla/5.0"}

  try:
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
      return

    soup = BeautifulSoup(response.text, "html.parser")
    duyurular = soup.find_all(
        "div", class_="announcement-item"
    )  # Örnek seçici

    for duyuru in duyurular:
      icerik = duyuru.text.lower()
      # İstanbul ve yarışma odaklı anahtar kelimeler
      if any(
          k in icerik
          for k in [
              "istanbul",
              "yarışma",
              "hackathon",
              "proje",
              "teknoloji",
              "başvuru",
          ]
      ):
        link = duyuru.find("a")["href"] if duyuru.find("a") else ""
        if link and link not in gonderilen_ilanlar:
          gonderilen_ilanlar.add(link)
          mesaj = (
              "🏆 *İstanbul Teknoloji Yarışması / Hackathon Duyurusu!*\n\n"
              f"📌 *Detay:* {duyuru.text.strip()[:100]}...\n"
              f"🔗 [Detaylar ve Başvuru]({link})"
          )
          telegrama_gonder(mesaj)
  except Exception as e:
    print(f"Yarışma tarama hatası: {e}")


# Zamanlayıcı Ayarları (Hangi fonksiyonun ne sıklıkla çalışacağı)
schedule.every(2).hours.do(youthall_tara)
schedule.every(3).hours.do(toptalent_tara)
schedule.every(6).hours.do(istanbul_yarismalari_tara)

print("🤖 Gelişmiş Staj ve Yarışma Asistanı Botu Çalıştı...")

# Test amaçlı ilk çalıştırma
youthall_tara()
toptalent_tara()
istanbul_yarismalari_tara()

while True:
  schedule.run_pending()
  time.sleep(60)