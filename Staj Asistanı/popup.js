document.getElementById('kaydetBtn').addEventListener('click', () => {
    const adSoyad = document.getElementById('adSoyad').value;
    const eposta = document.getElementById('eposta').value;
    const profilUrl = document.getElementById('profilUrl').value;

    // Bilgileri Chrome'un yerel hafızasına kaydediyoruz
    chrome.storage.sync.set({
        kullaniciAdi: adSoyad,
        kullaniciEposta: eposta,
        kullaniciUrl: profilUrl
    }, () => {
        alert('Bilgiler başarıyla kaydedildi kanka!');
    });
});

// Eklenti her açıldığında daha önce kaydedilen bilgiler kutucuklara gelsin
document.addEventListener('DOMContentLoaded', () => {
    chrome.storage.sync.get(['kullaniciAdi', 'kullaniciEposta', 'kullaniciUrl'], (result) => {
        if (result.kullaniciAdi) document.getElementById('adSoyad').value = result.kullaniciAdi;
        if (result.kullaniciEposta) document.getElementById('eposta').value = result.kullaniciEposta;
        if (result.kullaniciUrl) document.getElementById('profilUrl').value = result.kullaniciUrl;
    });
});