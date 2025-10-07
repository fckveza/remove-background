# 🎥 YouTube Downloader (Python)

Script sederhana untuk **mengunduh video YouTube secara otomatis** menggunakan **Selenium + BeautifulSoup + Requests**, dengan dukungan **proxy SOCKS5**.  
Script ini menggunakan browser Chrome otomatis untuk mengambil link unduhan dari situs pihak ketiga (`yt-mp4.org`).

---

## 🚀 Fitur
- ✅ Menggunakan **Selenium WebDriver** untuk scraping otomatis.
- ✅ Mendukung **proxy SOCKS5 (authenticated)**.
- ✅ Otomatis **mendeteksi tombol download** dan mengekstrak URL video.
- ✅ Mengunduh video langsung ke server dengan **progress bar**.
- ✅ Otomatis menutup Chrome & Chromedriver jika error (via `KillPid()`).

---

## 🧩 Requirements
Pastikan kamu sudah menginstal dependensi berikut di environment Python kamu.

```bash
pip install selenium webdriver-manager beautifulsoup4 requests wget
