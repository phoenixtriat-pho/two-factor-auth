# EKG — Gizli Program Engelleyici

Bu küçük araç, listelenen uygulamaları otomatik olarak kapatır ve bir OTP (TOTP) şifresi girilene kadar erişimi engeller. Aşağıda proje hakkında Türkçe kullanım ve yapılandırma talimatları bulabilirsiniz.

**Önemli:** Bu programda bilgisayarı kapatmaya yönelik bir komut (`shutdown /s /t 1`) bulunuyor. Test ederken dikkatli olun.

**Dosya:** Proje kökünde `ekg.py` bulunur. (Bu README aynı klasörde yer almalıdır.)

**Gereksinimler**
- Python 3.8+
- Bağımlılıklar: `psutil`, `keyboard`, `pyotp`, `qrcode`, `pillow` (qrcode görüntü oluşturmak için Pillow gerekir)

Kurulum (vurgulanan klasörde):

```bash
pip install -r requirements.txt
# veya
pip install psutil keyboard pyotp qrcode pillow
```

**Nasıl çalışır**
- `ekg.py` arkaplanda çalışır, görünmez bir Tkinter penceresi oluşturur ve belirlenen süreç isimlerini sürekli tarar.
- `programs` içinde listelenen süreç isimleri bulunduğunda script bu süreçleri kapatır.
- Doğru TOTP kodu girilirse ana pencere kapanır ve engelleme durur.
- Şifre ekranını açmak için kısayol: `Ctrl+Shift+F1` (dosyada `keyboard.add_hotkey("ctrl+shift+f1", goster_sifre_ekrani)` olarak ayarlı).

**OTP (TOTP) QR kodu nasıl oluşturulur**
Aşağıdaki küçük Python kodu ile bir gizli anahtar oluşturup, bir provisioning URI ve QR görüntüsü kaydedebilirsiniz. Bu QR'ı Google Authenticator veya benzeri bir uygulama ile tarayın.

```python
import pyotp
import qrcode

# 1) Gizli anahtar oluştur
secret = pyotp.random_base32()
print("Secret:", secret)

# 2) Provisioning URI oluştur (ör. user@example.com ve uygulama adı = EKG)
uri = pyotp.TOTP(secret).provisioning_uri(name="user@example.com", issuer_name="EKG")

# 3) QR oluştur ve kaydet
img = qrcode.make(uri)
img.save("otp_qr.png")

# QR'ı taradıktan sonra 'secret' değerini saklayın ve ekg.py içinde kullanın.
```

- Oluşturduğunuz `secret` anahtarını `ekg.py` içinde bulunan `ttotp = otp.TOTP("MVVWOYLQOBXXI4A=")` satırındaki sabitle değiştirin: `otp.TOTP("SIZIN_SECRET_DEGERINIZ")`.
- Güvenlik tavsiyesi: Sabit string yerine `secret.txt` gibi bir dosyaya kaydedip `ekg.py` içinde dosyadan okuyabilirsiniz. Örnek:

```python
with open("secret.txt") as f:
    secret = f.read().strip()
ttotp = otp.TOTP(secret)
```

**Program listesine nasıl eklenir**
- `ekg.py` içinde başta tanımlı `programs` kümesi vardır:

```python
programs = {"steam.exe", "WhatsApp.exe", "Taskmgr.exe", "Discord.exe","Code.exe"}
```

- Yeni bir program eklemek için ismini bu sete ekleyin. Örnek: `programs.add("chrome.exe")` veya doğrudan düzenleyin:

```python
programs = {"steam.exe", "WhatsApp.exe", "chrome.exe"}
```

Notlar:
- Süreç isimleri Windows'daki `Process Name` (ör. Görev Yöneticisi'nde görünen ad) ile eşleşmelidir.
- Büyük/küçük harf farkı denetimi script içinde olduğu gibi doğrudan string karşılaştırma yapar; gerektiğinde `process.info['name'].lower()` ile normalize edebilirsiniz.

**Çalıştırma**
- Komut satırından proje klasöründe çalıştırın:

```bash
python ekg.py
```

- Ayrıca `ekg.bat` dosyası varsa çift tıklayarak çalıştırabilirsiniz.

**Gelişmiş: secret dosyasından okuma örneği**
1. `secret.txt` oluşturun ve içinde sadece secret anahtarını yapıştırın (ör. MVVWOYLQOBXXI4A=)
2. `ekg.py` içinde aşağıdaki şekilde okuyun:

```python
import os

secret_path = os.path.join(os.path.dirname(__file__), "secret.txt")
with open(secret_path, "r") as f:
    secret = f.read().strip()

ttotp = otp.TOTP(secret)
```

**Güvenlik ve uyarılar**
- Program otomatik süreç sonlandırma ve sistem kapatma komutları içerir. Test ederken `os.system("shutdown /s /t 1")` satırını geçici olarak yoruma alın (comment out) veya değiştirin.
- `keyboard` kütüphanesi bazı sistemlerde yönetici (admin) izinleri gerektirebilir; kısayol düzgün çalışmazsa yönetici olarak çalıştırmayı deneyin.

**Sıkça Sorulanlar**
- QR tarandıktan sonra TOTP uygulaması size 6 haneli kod verecektir; bu kodu ekranda girerek doğrulama yapabilirsiniz.
- Secret kaybolursa yeni bir secret oluşturun ve QR'ı yeniden oluşturun.

Dosyalar
- [ekg.py](ekg.py)

İsterseniz README'yi genişleteyim (ör. `secret.txt` okunması için tam kod örneği ekleyeyim, veya `requirements.txt` içeriğini doğrulayıp örnek bir `ekg.bat` oluşturayım).



invisrun da terminal olmadan uygulamayı çalıştırmanıza yarar vbs ile çalıştırabilirsiniz