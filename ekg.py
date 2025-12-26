import tkinter as tk
from tkinter import messagebox
import psutil
import os
import time
import threading
import keyboard
import pyotp as otp
import qrcode
#def olustur_otp():
#    secret = otp.random_base32()

# Provisioning URI (Authenticator uygulamaları bu URI'yi QR'dan okur)
 #   uri = otp.TOTP(secret).provisioning_uri(name="user@example.com", issuer_name="EKG")

# QR oluşturup dosyaya kaydet
  #  img = qrcode.make(uri)
   # img.save("otp_qr.png")
# Engellenen programlar ve şifre
programs = {"steam.exe", "WhatsApp.exe", "Taskmgr.exe", "Discord.exe","Code.exe"}
# Şifre ekranını gösteren pencere
def sifre_ekrani():
    global pencere
    pencere = tk.Toplevel(root)  # Ana görünmeyen pencerenin üstünde bir Toplevel oluşturuyoruz
    pencere.title("Gizli Program Engelleyici")
    pencere.geometry("300x150")
    pencere.withdraw()  # Başlangıçta gizli olsun

    def gizle():
        pencere.withdraw()  # Pencereyi gizle

    def dogrula():
        sifre = sifre_girdisi.get()
        ttotp = otp.TOTP("MVVWOYLQOBXXI4A=")
        if sifre == ttotp.now():
            messagebox.showinfo("Başarılı", "Doğru şifre. Programlara izin verildi.")
            pencere.destroy()
            root.destroy()  # Pencereyi kapat
        else:
            messagebox.showerror("Hatalı Şifre", "Yanlış şifre girildi. Bilgisayar kapanacak!")
            os.system("shutdown /s /t 1")  # Bilgisayarı kapat

    # Şifre giriş alanı
    tk.Label(pencere, text="Şifre Giriniz:").pack(pady=10)
    sifre_girdisi = tk.Entry(pencere, show="*")
    sifre_girdisi.pack(pady=5)

    tk.Button(pencere, text="Onayla", command=dogrula).pack(pady=10)
    
    # Çarpıya basıldığında gizle
    pencere.protocol("WM_DELETE_WINDOW", gizle)
    
    return pencere

# Tuş kombinasyonuyla şifre ekranını gösterme
def goster_sifre_ekrani():
    if pencere.winfo_viewable():  # Şifre ekranı zaten görünüyorsa gizle
        pencere.withdraw()
    else:
        pencere.deiconify()  # Şifre ekranını göster

# Program engelleme fonksiyonu
def program_engelleyici():
    while True:
        # Şifre girilmemişse engellemeye devam et
        for process in psutil.process_iter(['pid', 'name']):
            try:
                if process.info['name'] in programs:
                    process.terminate()  # Engellenen programı kapat
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        time.sleep(2)

# Ana uygulamayı başlatan işlev
def main():
    global root, pencere
    root = tk.Tk()  # Görünmeyen ana pencere
    root.withdraw()  # Ana pencereyi gizliyoruz
    pencere = sifre_ekrani()  # Şifre ekranını oluştur

    # Kısayol tuşunu ayarla (Örneğin: Ctrl+Shift+S ile şifre ekranı açılacak)
    keyboard.add_hotkey("ctrl+shift+f1", goster_sifre_ekrani)

    # Engelleyici iş parçacığı
    engelleyici_thread = threading.Thread(target=program_engelleyici, daemon=True)
    engelleyici_thread.start()

    # Ana döngü başlat
    root.mainloop()

if __name__ == "__main__":
    main()
