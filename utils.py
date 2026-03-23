# utils.py - GreenTax AI Yardımcı Fonksiyonları
"""
GreenTax AI Utility Module

Bu modül, SKDM/CBAM uyumluluğu için hesaplama motoru, 
AI önerileri ve demo veri yükleme fonksiyonlarını içerir.

Fonksiyonlar:
    - load_demo_data(): Demo veri setini oluşturur
    - calculate_emissions(): Karbon emisyonlarını hesaplar
    - generate_ai_recommendations(): AI tabanlı öneriler üretir
    - generate_mock_recommendations(): Mock öneriler üretir
"""

import pandas as pd
import numpy as np
import os
from typing import Dict, List, Any, Optional

# Demo veri setini yükleme fonksiyonu


def load_demo_data() -> pd.DataFrame:
    """
    Demo veri setini oluşturur. Gerçek kullanımda CSV dosyasından yüklenir.
    
    Returns:
        pd.DataFrame: 50 satır ve 4 sütun içeren demo veri seti
    """
    np.random.seed(42)  # Tutarlı sonuçlar için

    # Ürün tipleri ve hammadde kaynakları
    product_types = ['Çelik', 'Çimento', 'Alüminyum', 'Elektrik', 'Diğer']
    raw_materials = ['Yerli', 'İthal', 'Geri Dönüştürülmüş', 'Fosil Bazlı']

    # 50 satırlık demo veri
    data = {
        'Ürün Tipi': np.random.choice(product_types, 50),
        'Üretim Miktarı': np.random.uniform(100, 10000, 50).round(2),  # ton
        'Enerji Tüketimi': np.random.uniform(1000, 50000, 50).round(2),  # kWh
        'Hammadde Kaynağı': np.random.choice(raw_materials, 50)
    }

    return pd.DataFrame(data)

# SKDM hesaplama motoru


def calculate_emissions(
    data: pd.DataFrame,
    emission_factors: Dict[str, float],
    grid_intensity: float,
    carbon_price: float
) -> Dict[str, Any]:
    """
    SKDM emisyon hesaplamalarını gerçekleştirir.

    Formül: Total Emissions = (Production Quantity × Emission Factor) + 
            (Energy Consumption × Grid Intensity)

    Args:
        data: Üretim verileri (DataFrame)
        emission_factors: Ürün tipine göre emisyon faktörleri (ton CO2/ton ürün)
        grid_intensity: Şebeke karbon yoğunluğu (kg CO2/kWh)
        carbon_price: Karbon fiyatı (€/ton CO2)

    Returns:
        dict: Hesaplama sonuçları anahtar-değer çiftleri içeren sözlük

    Raises:
        ValueError: Girdi doğrulaması başarısız veya hesaplama hatası
        TypeError: Veri tipleri yanlış ise
    """
    try:
        # Girdi doğrulaması
        if not isinstance(data, pd.DataFrame):
            raise TypeError("data parametresi pandas DataFrame olmalıdır")
        if data.empty:
            raise ValueError("Veri seti boş olamaz")
        if not isinstance(emission_factors, dict):
            raise TypeError("emission_factors parametresi dict olmalıdır")
        if not isinstance(grid_intensity, (int, float)) or grid_intensity < 0:
            raise ValueError("grid_intensity pozitif sayı olmalıdır")
        if not isinstance(carbon_price, (int, float)) or carbon_price < 0:
            raise ValueError("carbon_price pozitif sayı olmalıdır")

        # Veri kopyası oluştur
        df = data.copy()

        # Emisyon faktörlerini ekle
        df['Emission Factor'] = df['Ürün Tipi'].map(
            emission_factors).fillna(1.0)

        # Emisyon hesaplamaları (ton CO2 cinsinden)
        df['Üretim Emisyonu'] = df['Üretim Miktarı'] * \
            df['Emission Factor']  # ton CO2
        # ton CO2 (kg'dan ton'a çevirme)
        df['Enerji Emisyonu'] = (df['Enerji Tüketimi'] * grid_intensity) / 1000
        df['Toplam Emisyon'] = df['Üretim Emisyonu'] + df['Enerji Emisyonu']

        # Vergi hesaplaması
        df['Vergi Yükü'] = df['Toplam Emisyon'] * carbon_price  # €

        # Toplam değerler
        total_emissions = df['Toplam Emisyon'].sum()
        total_tax = df['Vergi Yükü'].sum()

        # Karbon yoğunluğu (kg CO2/€ üretim değeri - demo için basit hesaplama)
        # Gerçekte üretim değeri gerekli, burada yaklaşık olarak üretim miktarı
        # ile çarpım
        carbon_intensity = (total_emissions * 1000) / \
            df['Üretim Miktarı'].sum() if df['Üretim Miktarı'].sum() > 0 else 0

        # Aylık trend verisi (demo için rastgele)
        months = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
                  'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
        monthly_emissions = np.random.uniform(
            total_emissions * 0.7, total_emissions * 1.3, 12)
        monthly_data = pd.DataFrame({
            'Ay': months,
            'Emisyon': monthly_emissions.round(1)
        })

        # Hammadde bazlı emisyon dağılımı
        raw_material_emissions = df.groupby('Hammadde Kaynağı')[
            'Toplam Emisyon'].sum().reset_index()
        raw_material_emissions.columns = ['Hammadde Kaynağı', 'Emisyon']

        # Ürün bazlı veri (scatter plot için)
        product_data = df[['Ürün Tipi', 'Üretim Miktarı',
                           'Toplam Emisyon', 'Vergi Yükü']].copy()
        product_data.columns = [
            'Ürün Tipi',
            'Üretim Miktarı',
            'Emisyon',
            'Vergi Yükü']

        return {
            'total_emissions': total_emissions,
            'total_tax': total_tax,
            'carbon_intensity': carbon_intensity,
            'monthly_trend': monthly_data,
            'raw_material_emissions': raw_material_emissions,
            'product_data': product_data,
            'detailed_data': df
        }

    except Exception as e:
        raise ValueError(f"Hesaplama sırasında hata: {str(e)}")

# AI önerileri oluşturma fonksiyonu


def generate_ai_recommendations(results: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Analiz sonuçlarına göre AI tabanlı stratejik öneriler üretir.
    Anthropic/OpenAI API entegrasyonu ile gerçek AI önerileri.

    Args:
        results: Hesaplama sonuçları (calculate_emissions döndürüsü)

    Returns:
        list: Öneri sözlüklerinin listesi
    """
    try:
        # API key kontrolü
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        openai_key = os.getenv('OPENAI_API_KEY')

        if anthropic_key:
            # Anthropic Claude kullanımı
            import anthropic
            client = anthropic.Anthropic(api_key=anthropic_key)

            prompt = f"""
            Aşağıdaki SKDM/CBAM emisyon analizi sonuçlarına göre stratejik öneriler üretin.

            Toplam Emisyon: {results['total_emissions']:.1f} ton CO2
            Toplam Vergi Yükü: €{results['total_tax']:.0f}
            Karbon Yoğunluğu: {results['carbon_intensity']:.2f} kg CO2/€

            Ürün bazlı veriler:
            {results['product_data'].to_string(index=False)}

            Hammadde bazlı emisyon dağılımı:
            {results['raw_material_emissions'].to_string(index=False)}

            Lütfen 3-5 spesifik, uygulanabilir öneri üretin. Her öneri için:
            - Başlık
            - Durum açıklaması
            - Spesifik öneri

            Yanıtınızı JSON formatında döndürün.
            """

            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                temperature=0.7,
                system="Sen bir karbon emisyonu uzmanısın. SKDM/CBAM uyumluluk konusunda öneriler veriyorsun.",
                messages=[{"role": "user", "content": prompt}]
            )

            # JSON parse et ve döndür
            import json
            recommendations_text = response.content[0].text
            recommendations = json.loads(recommendations_text)
            return recommendations

        elif openai_key:
            # OpenAI GPT kullanımı
            import openai
            client = openai.OpenAI(api_key=openai_key)

            prompt = f"""
            Aşağıdaki SKDM/CBAM emisyon analizi sonuçlarına göre stratejik öneriler üretin.

            Toplam Emisyon: {results['total_emissions']:.1f} ton CO2
            Toplam Vergi Yükü: €{results['total_tax']:.0f}
            Karbon Yoğunluğu: {results['carbon_intensity']:.2f} kg CO2/€

            Lütfen 3-5 spesifik öneri üretin. Her öneri için başlık, açıklama ve spesifik tavsiye içersin.
            """

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Sen bir karbon emisyonu uzmanısın. SKDM/CBAM konusunda öneriler veriyorsun."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )

            # Yanıtı parse et (basit parsing)
            ai_response = response.choices[0].message.content
            # Mock formatına dönüştür
            return parse_ai_response_to_recommendations(ai_response)

        else:
            # API key yok, mock öneriler
            return generate_mock_recommendations(results)

    except Exception as e:
        # Hata durumunda mock önerilere geç
        print(f"AI API hatası: {str(e)}. Mock öneriler kullanılıyor.")
        return generate_mock_recommendations(results)


def parse_ai_response_to_recommendations(ai_response):
    """
    AI yanıtını öneri formatına dönüştürür.
    """
    # Basit parsing - gerçek implementasyonda daha sofistike olabilir
    recommendations = []
    lines = ai_response.split('\n')

    current_rec = {}
    for line in lines:
        line = line.strip()
        if line.startswith('Başlık:') or line.startswith('Title:'):
            if current_rec:
                recommendations.append(current_rec)
            current_rec = {'title': line.split(':', 1)[1].strip()}
        elif line.startswith('Açıklama:') or line.startswith('Description:'):
            current_rec['description'] = line.split(':', 1)[1].strip()
        elif line.startswith('Öneri:') or line.startswith('Recommendation:'):
            current_rec['recommendation'] = line.split(':', 1)[1].strip()

    if current_rec:
        recommendations.append(current_rec)

    return recommendations if recommendations else generate_mock_recommendations({
    })


def generate_mock_recommendations(results: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    API mevcut değilse kullanılacak mock öneriler üretir.

    Args:
        results: Hesaplama sonuçları (calculate_emissions döndürüsü)

    Returns:
        list: Mock öneri sözlüklerinin listesi
    """
    recommendations = []

    try:
        # En yüksek vergi yüküne sahip ürünü bul
        product_data = results.get('product_data', pd.DataFrame())
        if isinstance(product_data, pd.DataFrame) and not product_data.empty:
            if 'Vergi Yükü' in product_data.columns:
                highest_tax_idx = product_data['Vergi Yükü'].idxmax()
                highest_tax_product = product_data.loc[highest_tax_idx]

                recommendations.append({
                    'title': f"Yüksek Vergi Yükü: {highest_tax_product['Ürün Tipi']}",
                    'description': f"{highest_tax_product['Ürün Tipi']} ürününde {highest_tax_product['Vergi Yükü']:.0f}€ vergi yükü tespit edildi.",
                    'recommendation': "Yenilenebilir enerji kaynaklarına geçiş yaparak enerji tüketimi emisyonlarını %30-50 azaltabilirsiniz."
                })
    except Exception as e:
        print(f"Ürün verisi işlemesinde hata: {str(e)}")

    try:
        # Hammadde kaynaklarına göre öneriler
        raw_material_data = results.get(
            'raw_material_emissions', pd.DataFrame())
        if isinstance(
                raw_material_data,
                pd.DataFrame) and not raw_material_data.empty:
            if 'Hammadde Kaynağı' in raw_material_data.columns and 'Emisyon' in raw_material_data.columns:
                fossil_based = raw_material_data[raw_material_data['Hammadde Kaynağı']
                                                 == 'Fosil Bazlı']
                if not fossil_based.empty:
                    fossil_emission = fossil_based['Emisyon'].sum()
                    total_emissions = results.get('total_emissions', 0)
                    if total_emissions > 0 and fossil_emission > total_emissions * 0.3:
                        recommendations.append({
                            'title': "Hammadde Tedarik Stratejisi",
                            'description': "Fosil bazlı hammadde kullanımı toplam emisyonların %30'undan fazlasını oluşturuyor.",
                            'recommendation': "Geri dönüştürülmüş veya yenilenebilir kaynaklı hammadde tedarikçilerine geçiş yaparak emisyonları azaltın."
                        })
    except Exception as e:
        print(f"Hammadde verisi işlemesinde hata: {str(e)}")

    try:
        # Genel öneriler
        if results.get('carbon_intensity', 0) > 5.0:
            recommendations.append({
                'title': "Karbon Yoğunluğu Optimizasyonu",
                'description': f"Karbon yoğunluğunuz {results.get('carbon_intensity', 0):.2f} kg CO2/€ ile yüksek seviyede.",
                'recommendation': "Üretim proseslerinizi optimize edin ve enerji verimliliği projelerine yatırım yapın."
            })
    except Exception as e:
        print(f"Karbon yoğunluğu analizi hatası: {str(e)}")

    # Eğer öneri yoksa varsayılan öneri
    if not recommendations:
        recommendations.append({
            'title': "Genel SKDM Uyumluluk Önerisi",
            'description': "Verileriniz SKDM standartlarına uygun görünüyor.",
            'recommendation': "Düzenli emisyon izleme ve raporlama sisteminizi sürdürün."
        })

    return recommendations
