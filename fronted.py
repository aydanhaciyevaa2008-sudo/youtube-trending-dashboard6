import streamlit as st
import requests
import pandas as pd

# Səhifə başlıq ayarları
st.set_page_config(page_title="YouTube Dashboard", layout="wide")

st.title("Barselona 📊 YouTube Trending Videos Analiz Paneli")
st.write("Daxili verilənlər bazasının backend API vasitəsilə vizuallaşdırılması")

# Yeni backend portumuza (8005) müraciət edirik
BACKEND_URL = "http://127.0.0.1:8005"

# Slider: İstifadəçinin neçə video görmək istədiyini seçməsi üçün
limit = st.slider("Göstəriləcək video sayı:", min_value=5, max_value=50, value=10)

st.markdown("---")

# Backend-dən məlumatları çəkirik
try:
    # 1. Statistika Kartları üçün müraciət
    stats_res = requests.get(f"{BACKEND_URL}/api/stats").json()

    col1, col2, col3 = st.columns(3)
    col1.metric("Ümumi Video Sayı", f"{stats_res['total_videos']:,}")
    col2.metric("Ümumi Baxış Sayı", f"{stats_res['total_views']:,}")
    col3.metric("Ortalama Bəyənmə", f"{int(stats_res['average_likes']):,}")

    st.markdown("---")

    # 2. Top Videoların Cədvəli üçün müraciət
    videos_res = requests.get(f"{BACKEND_URL}/api/top-trending?limit={limit}").json()
    df = pd.DataFrame(videos_res)

    st.subheader(f"🔥 Ən çox baxılan {limit} video")
    st.dataframe(df[['title', 'channel_title', 'views', 'likes', 'comment_count']], use_container_width=True)

    st.markdown("---")

    # 3. Qrafik: Baxış saylarının vizuallaşdırılması
    st.subheader("📊 Videoların Baxış Sayı Müqayisəsi")
    st.bar_chart(data=df, x="title", y="views")

except Exception as e:
    st.error(
        f"Backend ilə əlaqə qurula bilmədi. Zəhmət olmasa backend proqramınızın işlədiyindən və portunun 8005 olduğundan əmin olun.")