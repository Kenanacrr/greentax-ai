# GreenTax AI - SKDM/CBAM Uyumluluk Yönetim Sistemi
# Bu uygulama, şirketlerin AB Sınırda Karbon Düzenleme Mekanizması (SKDM/CBAM) uyumluluğunu
# yönetmek için geliştirilmiştir.

# Gerekli kütüphaneler
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils import calculate_emissions, generate_ai_recommendations, load_demo_data
import os

# Sayfa yapılandırması
st.set_page_config(
    page_title="GreenTax AI - SKDM/CBAM Yönetimi",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Özel CSS stilleri
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Ana başlık
st.title("🌱 GreenTax AI - SKDM/CBAM Uyumluluk Yönetim Sistemi")
st.markdown("---")

# Sidebar - Veri girişi
st.sidebar.header("📊 Veri Girişi")

# Dosya yükleme
uploaded_file = st.sidebar.file_uploader(
    "CSV dosyasını yükleyin",
    type=['csv'],
    help="Ürün Tipi, Üretim Miktarı, Enerji Tüketimi, Hammadde Kaynağı sütunlarını içeren CSV dosyası"
)

# Demo veri kullanımı
use_demo = st.sidebar.checkbox("Demo veri setini kullan", value=True)

# Ana veri yükleme mantığı
@st.cache_data
def load_data(file=None, use_demo=True):
    if file is not None:
        try:
            df = pd.read_csv(file)
            required_cols = ['Ürün Tipi', 'Üretim Miktarı', 'Enerji Tüketimi', 'Hammadde Kaynağı']
            if not all(col in df.columns for col in required_cols):
                st.error(f"CSV dosyası şu sütunları içermelidir: {', '.join(required_cols)}")
                return None
            return df
        except Exception as e:
            st.error(f"Dosya yüklenirken hata: {str(e)}")
            return None
    elif use_demo:
        return load_demo_data()
    else:
        return None

# Veri yükleme
data = load_data(uploaded_file, use_demo)

if data is not None:
    st.sidebar.success("Veri başarıyla yüklendi!")
    
    # Veri önizleme
    with st.expander("📋 Veri Önizleme", expanded=False):
        st.dataframe(data.head(), width='stretch')
    
    # Hesaplama parametreleri
    st.sidebar.header("⚙️ Hesaplama Parametreleri")
    
    # Emission Factor'ları (ürün tipine göre)
    emission_factors = {
        'Çelik': 2.5,  # ton CO2/ton ürün
        'Çimento': 0.8,
        'Alüminyum': 8.5,
        'Elektrik': 0.4,
        'Diğer': 1.0
    }
    
    # Grid Intensity (ülkeye göre, varsayılan Türkiye)
    grid_intensity = st.sidebar.number_input(
        "Şebeke Yoğunluğu (kg CO2/kWh)",
        value=0.45,
        min_value=0.0,
        step=0.01,
        help="Ülkenizin elektrik şebeke karbon yoğunluğu"
    )
    
    # Karbon fiyatı
    carbon_price = 85.0  # €/ton CO2
    
    # Hesaplamaları yap
    results = calculate_emissions(data, emission_factors, grid_intensity, carbon_price)
    
    # Ana dashboard
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Toplam Emisyon",
            f"{results['total_emissions']:.1f} ton CO2",
            help="SKDM kapsamındaki toplam karbon emisyonu"
        )
    
    with col2:
        st.metric(
            "Toplam Vergi Yükü",
            f"€{results['total_tax']:.0f}",
            help="85€/ton karbon fiyatı üzerinden hesaplanan vergi"
        )
    
    with col3:
        st.metric(
            "Karbon Yoğunluğu",
            f"{results['carbon_intensity']:.2f} kg CO2/€",
            help="Üretim değerine göre karbon yoğunluğu"
        )
    
    st.markdown("---")
    
    # Grafikler
    st.header("📈 Analitik Görseller")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Aylık emisyon trendi (demo için rastgele aylık veri)
        monthly_data = results['monthly_trend']
        fig_area = px.area(
            monthly_data, 
            x='Ay', 
            y='Emisyon',
            title="Aylık Emisyon Trendi",
            color_discrete_sequence=['#2ECC71']
        )
        fig_area.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_area, width='stretch')
    
    with col2:
        # Hammadde bazlı emisyon dağılımı
        raw_material_emissions = results['raw_material_emissions']
        fig_sunburst = px.sunburst(
            raw_material_emissions,
            path=['Hammadde Kaynağı'],
            values='Emisyon',
            title="Hammadde Bazlı Emisyon Dağılımı",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_sunburst.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_sunburst, width='stretch')
    
    # Scatter plot - Üretim miktarı vs Emisyon
    fig_scatter = px.scatter(
        results['product_data'],
        x='Üretim Miktarı',
        y='Emisyon',
        color='Ürün Tipi',
        size='Vergi Yükü',
        title="Üretim Miktarı vs Emisyon Korelasyonu",
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    fig_scatter.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    st.plotly_chart(fig_scatter, width='stretch')
    
    st.markdown("---")
    
    # AI Önerileri
    st.header("🤖 AI Strateji Önerileri")
    
    recommendations = generate_ai_recommendations(results)
    
    for rec in recommendations:
        with st.container():
            st.subheader(f"🎯 {rec['title']}")
            st.write(rec['description'])
            st.info(f"💡 Öneri: {rec['recommendation']}")
            st.markdown("---")
    
else:
    st.sidebar.warning("Lütfen bir CSV dosyası yükleyin veya demo veriyi kullanın.")
    st.info("🌟 GreenTax AI'ye hoş geldiniz! Sol taraftan veri yükleyerek SKDM/CBAM analizinizi başlatın.")