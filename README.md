# GreenTax AI — CBAM Compliance Platform

🌱 **GreenTax AI**, şirketlerin AB Sınırda Karbon Düzenleme Mekanizması (SKDM/CBAM) uyumluluğunu yöneten profesyonel bir web uygulamasıdır.

## 📋 Proje Açıklaması

Bu proje, AB'nin Sınırda Karbon Düzenleme Mekanizması (SKDM/CBAM) kapsamında şirketlerin karbon emisyonlarını hesaplamalarına, vergi yüklerini analiz etmelerine ve stratejik kararlar almalarına yardımcı olan kapsamlı bir web uygulamasıdır.

## 🚀 Özellikler

- **Veri Giriş Katmanı**: CSV dosya yükleme veya hazır demo veri kullanımı
- **SKDM Hesaplama Motoru**: Emisyon hesaplamaları ve vergi yükü analizi
- **Analitik Dashboard**: Metrik kartları ve etkileşimli grafikler
- **AI Strateji Katmanı**: Yapay zeka tabanlı özelleştirilmiş öneriler
- **Modern UI/UX**: Dark mode destekli, profesyonel yeşil tema

## 📋 Gereksinimler

- Python 3.8+
- pip (Python paket yöneticisi)

## 🛠️ Kurulum ve Çalıştırma

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/Kenanacrr/greentax-ai.git
cd greentax-ai
```

### 2. Sanal Ortam Oluşturun (Önerilen)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate     # Windows
```

### 3. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 4. Uygulamayı Çalıştırın
```bash
streamlit run app.py
```

### 5. Tarayıcıda Açın
Uygulama otomatik olarak varsayılan tarayıcınızda açılacaktır. Genellikle `http://localhost:8501` adresinde çalışır.

## 📊 Kullanım

1. **Veri Yükleme**: Sol sidebar'dan CSV dosyasını yükleyin veya demo veriyi kullanın.
2. **Parametre Ayarları**: Şebeke yoğunluğu ve diğer parametreleri ayarlayın.
3. **Analiz**: Metrikleri inceleyin, grafikleri keşfedin ve AI önerilerini değerlendirin.

### CSV Dosya Formatı
Yükleyeceğiniz CSV dosyası aşağıdaki sütunları içermelidir:
- `Ürün Tipi`: Ürün kategorisi (Çelik, Çimento, Alüminyum, Elektrik, Diğer)
- `Üretim Miktarı`: Ton cinsinden üretim miktarı
- `Enerji Tüketimi`: kWh cinsinden enerji tüketimi
- `Hammadde Kaynağı`: Hammadde kaynağı (Yerli, İthal, Geri Dönüştürülmüş, Fosil Bazlı)

## 🔧 Teknik Detaylar

### Hesaplama Formülü
```
Total Emissions = (Production Quantity × Emission Factor) + (Energy Consumption × Grid Intensity)
```

### Emission Factor'ları (ton CO2/ton ürün)
- Çelik: 2.5
- Çimento: 0.8
- Alüminyum: 8.5
- Elektrik: 0.4
- Diğer: 1.0

### Karbon Fiyatı
- 85€/ton CO2 (AB güncel ortalaması)

## 🤖 AI Özellikleri

Uygulama, analiz sonuçlarına göre aşağıdaki gibi öneriler üretir:
- Yüksek vergi yüküne sahip ürünlerin belirlenmesi
- Hammadde tedarik stratejileri
- Karbon yoğunluğu optimizasyonu
- Genel SKDM uyumluluk önerileri

## 📁 Proje Yapısı

```
greentax-ai/
├── app.py              # Ana Streamlit uygulaması
├── utils.py            # Yardımcı fonksiyonlar ve hesaplama motoru
├── style.css           # Özel CSS stilleri
├── demo_data.csv       # Demo veri seti
├── requirements.txt    # Python bağımlılıkları
└── README.md          # Bu dosya
```

## � API Entegrasyonu (Opsiyonel)

Gerçek AI önerileri için Anthropic Claude veya OpenAI API anahtarlarını ekleyebilirsiniz:

### Anthropic Claude API
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### OpenAI API
```bash
export OPENAI_API_KEY="your-api-key-here"
```

API anahtarları olmadan uygulama mock önerilerle çalışır.

## 📚 Teknik Bilgiler

### SKDM/CBAM Nedir?
AB Sınırda Karbon Düzenleme Mekanizması (SKDM/CBAM), Avrupa Birliği'nin İklim Eylem Planının bir parçasıdır. Bu mekanizma, AB'ye ithal edilen ürünlerde karbon sızıntısını önlemek için tasarlanmıştır.

### Hesaplama Modeli
1. **Üretim Emisyonu**: Ürün tipi × Üretim Miktarı × Emisyon Faktörü
2. **Enerji Emisyonu**: Enerji Tüketimi × Şebeke Yoğunluğu
3. **Toplam Emisyon**: Üretim Emisyonu + Enerji Emisyonu
4. **Vergi Yükü**: Toplam Emisyon × Karbon Fiyatı

### Parametre Açıklaması
- **Grid Intensity**: Elektrik şebekenizin ortalama karbon yoğunluğu
- **Carbon Price**: AB ETS (Emissions Trading System) referans fiyatı
- **Emission Factors**: Ürün tipine göre standar emisyon faktörleri

## �🐛 Sorun Giderme

### Uygulama Açılmıyor
- Python sürümünüzü kontrol edin: `python --version`
- Bağımlılıkları tekrar yükleyin: `pip install -r requirements.txt`
- Port çakışması durumunda: `streamlit run app.py --server.port 8502`

### CSV Yükleme Hatası
- CSV dosyasının UTF-8 encoding olduğundan emin olun
- Gerekli sütunların mevcut olduğunu kontrol edin
- Ondalık ayıracı olarak nokta (.) kullandığınızdan emin olun

## 📞 Destek

Herhangi bir sorun yaşarsanız, lütfen GitHub Issues sayfasında raporlayın.

## 📄 Lisans

Bu proje açık kaynak kodludur ve MIT lisansı altında yayınlanmıştır.

---

**Geliştirici**: Kıdemli Full-Stack Python Geliştirici ve Veri Analisti
**Tarih**: 2026
**Versiyon**: 1.0.0
