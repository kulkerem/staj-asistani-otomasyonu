import time
import requests
from bs4 import BeautifulSoup
import telebot
import schedule

# Telegram Bot Ayarları
TOKEN = "8760553861:AAGqOX__B499znFRqIf5pJ-BhGcveCqJW4g"
CHAT_ID = "6835466084"

bot = telebot.TeleBot(TOKEN)

# Tekrar eden bildirimleri engellemek için hafıza
gonderilen_ilanlar = set()


def telegrama_gonder(mesaj):
  try:
    bot.send_message(CHAT_ID, mesaj, parse_mode="Markdown")
  except Exception as e:
    print(f"Telegram mesajı gönderilirken hata oluştu: {e}")


# 1. Kaynak: Youthall Staj İlanları
def youthall_tara():
  print("INFO: Youthall taranıyor...")
  url = "https://youthall.com/tr/ilanlar/"
  headers = {"User-Agent": "Mozilla/5.0"}

  try:
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
      return

    soup = BeautifulSoup(response.text, "html.parser")
    ilanlar = soup.find_all("div", class_="job-card")

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
      if any(kelime in baslik for kelime in anahtar_kelimeler):
        ilan_linki = ilan.find("a")["href"] if ilan.find("a") else "Link yok"
        if ilan_linki not in gonderilen_ilanlar:
          gonderilen_ilanlar.add(ilan_linki)
          mesaj = (
              "🚀 *Yeni Staj Fırsatı (Youthall)*\n\n"
              f"📌 *Detay:* {ilan.text.strip()[:100]}...\n"
              f"🔗 [İlana Git]({ilan_linki})"
          )
          telegrama_gonder(mesaj)
  except Exception as e:
    print(f"Youthall tarama hatası: {e}")


# 2. Kaynak: Toptalent Staj Programları
def toptalent_tara():
  print("INFO: Toptalent taranıyor...")
  url = "https://toptalent.co/staj-ilanlari"
  headers = {"User-Agent": "Mozilla/5.0"}

  try:
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
      return

    soup = BeautifulSoup(response.text, "html.parser")
    ilanlar = soup.find_all("div", class_="job-item")

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


# 3. Kaynak: LinkedIn Staj İlanları (Yeni Eklendi!)
def linkedin_tara():
  print("INFO: LinkedIn staj ilanları taranıyor...")
  # LinkedIn açık arama / staj filtresi bağlantısı
  url = "https://www.linkedin.com/jobs/search/?keywords=yaz%C4%B1l%C4%B1m%20stajyeri&location=T%C3%BCrkiye"
  headers = {"User-Agent": "Mozilla/5.0"}

  try:
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
      return

    soup = BeautifulSoup(response.text, "html.parser")
    # LinkedIn kart yapısına uygun seçici
    ilanlar = soup.find_all("div", class_="base-search-card__info")

    for ilan in ilanlar:
      metin = ilan.text.lower()
      link_tag = ilan.find("a", class_="base-card__full-link")
      link = link_tag["href"] if link_tag else ""

      if link and link not in gonderilen_ilanlar:
        gonderilen_ilanlar.add(link)
        mesaj = (
            "💼 *Yeni LinkedIn Staj İlanı!*\n\n"
            f"📌 *Detay:* {ilan.text.strip()[:100]}...\n"
            f"🔗 [İlana Git]({link})"
        )
        telegrama_gonder(mesaj)
  except Exception as e:
    print(f"LinkedIn tarama hatası: {e}")


# 4. Kaynak: İstanbul Teknoloji Projeleri ve Yarışmalar
def istanbul_yarismalari_tara():
  print("INFO: İstanbul teknoloji yarışmaları ve hackathonlar taranıyor...")
  url = "https://www.ibb.istanbul/uluslararasi-veya-teknoloji-yarismalari"
  headers = {"User-Agent": "Mozilla/5.0"}

  try:
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
      return

    soup = BeautifulSoup(response.text, "html.parser")
    duyurular = soup.find_all("div", class_="announcement-item")

    for duyuru in duyurular:
      icerik = duyuru.text.lower()
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


# Zamanlayıcı Döngüsü
schedule.every(2).hours.do(youthall_tara)
schedule.every(3).hours.do(toptalent_tara)
schedule.every(4).hours.do(linkedin_tara)  # LinkedIn için periyot
schedule.every(6).hours.do(istanbul_yarismalari_tara)

print("🤖 LinkedIn Destekli Gelişmiş Staj ve Yarışma Asistanı Çalıştı...")

# Test amaçlı ilk çalıştırma
youthall_tara()
toptalent_tara()
linkedin_tara()
istanbul_yarismalari_tara()

while True:
  schedule.run_pending()
  time.sleep(60)