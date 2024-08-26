import requests
from PIL import Image
import pytesseract
from io import BytesIO
import base64

# Fungsi untuk menangani CAPTCHA dalam format base64
def handle_captcha_base64(base64_data):
    base64_image = base64_data.split(',')[1]  # Menghapus prefix 'data:image/png;base64,'
    image_data = base64.b64decode(base64_image)
    image = Image.open(BytesIO(image_data))
    return image

# Input dari pengguna
nik = input("Masukkan NIK: ")
tanggal_lahir = input("Masukkan Tanggal Lahir (dd-mm-yyyy): ")

# Mendapatkan CAPTCHA
captcha_url = 'https://webskrining.bpjs-kesehatan.go.id/skrining/captcha-servlet'
response = requests.get(captcha_url)

if response.status_code == 200:
    # Jika CAPTCHA dalam format base64
    captcha_base64_data = response.text  # Asumsikan respons adalah base64
    captcha_image = handle_captcha_base64(captcha_base64_data)
    
    # Simpan gambar CAPTCHA untuk verifikasi
    captcha_image.save('captcha_image.png')
    print("CAPTCHA image saved as 'captcha_image.png'.")

    # Menggunakan OCR untuk membaca CAPTCHA dari gambar
    captcha_text = pytesseract.image_to_string(captcha_image, config='--psm 8')  # config '--psm 8' untuk OCR single line text
    captcha_text = captcha_text.strip()
    print(f"CAPTCHA Text: {captcha_text}")

    # Kirim data form dengan CAPTCHA
    form_url = 'https://webskrining.bpjs-kesehatan.go.id/skrining/v1/skrining/request'
    data = {
        'url': 'Skrining-RPT',
        'param': nik,  # NIK dari input pengguna
        'param2': tanggal_lahir,  # Tanggal lahir dari input pengguna
        'param3': None,
        'captchaCode': captcha_text,  # Kode CAPTCHA yang terdeteksi
        'captchaID': None,  # CAPTCHA ID harus didapat dari respon CAPTCHA sebelumnya
        'userAgent': None,
        'noSkrining': None
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.post(form_url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print("Response Text:", response.text)
else:
    print("Failed to retrieve CAPTCHA.")
