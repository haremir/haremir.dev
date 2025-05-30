# Kişisel Portfolyo Web Sitesi

Bu proje, Flask kullanılarak geliştirilmiş kişisel bir portfolyo web sitesidir. Veri bilimi ve Python geliştirme projelerini sergilemek için tasarlanmıştır.

## Özellikler

- Responsive tasarım (mobil uyumlu)
- Karanlık/Aydınlık tema desteği
- Teknik blog bölümü
- Admin paneli
- GitHub projeleri entegrasyonu
- Bootstrap 5 ve Bootstrap Icons kullanımı
- Inter font ailesi

## Teknolojiler

- Python 3.x
- Flask
- SQLite
- Bootstrap 5
- HTML5/CSS3
- JavaScript

## Kurulum

1. Projeyi klonlayın:
```bash
git clone https://github.com/haremir/portfolio.git
cd portfolio
```

2. Sanal ortam oluşturun ve aktifleştirin:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac için
venv\Scripts\activate     # Windows için
```

3. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

4. Veritabanını oluşturun:
```bash
flask db init
flask db migrate
flask db upgrade
```

5. Uygulamayı çalıştırın:
```bash
python app.py
```

## Kullanım

- Ana sayfa: Projeler ve yetenekler
- Blog: Teknik yazılar ve makaleler
- Admin Panel: Blog yazılarını yönetmek için

## Katkıda Bulunma

1. Bu depoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik: Açıklama'`)
4. Branch'inizi push edin (`git push origin feature/yeniOzellik`)
5. Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## İletişim

- GitHub: [@haremir](https://github.com/haremir)
- LinkedIn: [Harun Emirhan Bostancı](https://www.linkedin.com/in/haremir826/)
- E-posta: harunemirhan826@gmail.com 