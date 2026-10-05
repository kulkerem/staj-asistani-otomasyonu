// Sayfa yüklendiğinde çalışacak ana fonksiyon
window.addEventListener('load', () => {
    // Chrome hafızasındaki bilgileri çekiyoruz
    chrome.storage.sync.get(['kullaniciAdi', 'kullaniciEposta', 'kullaniciUrl'], (data) => {
        if (!data.kullaniciAdi) return; // Kayıtlı bilgi yoksa işlem yapma

        // Sayfadaki tüm input (veri giriş) kutularını tarıyoruz
        const inputs = document.querySelectorAll('input');

        inputs.forEach(input => {
            const placeholder = (input.placeholder || "").toLowerCase();
            const name = (input.name || "").toLowerCase();
            const type = (input.type || "").toLowerCase();

            // İsim alanını bul ve doldur
            if (placeholder.includes('ad') || name.includes('name') || name.includes('fullname')) {
                input.value = data.kullaniciAdi;
                input.dispatchEvent(new Event('input', { bubbles: true })); // Sitenin haberi olsun diye tetikliyoruz
            }

            // E-posta alanını bul ve doldur
            if (type === 'email' || placeholder.includes('mail') || name.includes('email')) {
                input.value = data.kullaniciEposta;
                input.dispatchEvent(new Event('input', { bubbles: true }));
            }

            // LinkedIn / GitHub / Website alanını bul ve doldur
            if (placeholder.includes('linkedin') || placeholder.includes('github') || name.includes('url') || name.includes('website')) {
                input.value = data.kullaniciUrl;
                input.dispatchEvent(new Event('input', { bubbles: true }));
            }
        });

        console.log("Staj Asistanı: Form alanları tarandı ve dolduruldu!");
    });
});