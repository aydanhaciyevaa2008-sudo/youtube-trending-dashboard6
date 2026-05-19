from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import uvicorn
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# İnternet linklərini tamamilə sildik. Data birbaşa daxildə yaradılır.
print("Məlumatlar bazası hazırlanır...")

titles = [

    "agillı 10 Məkan", "Kiber Təhlükəsizlik Nədir?",
    "Ən Çox Satılan Texnoloji Qadcetler", "Şahmatda Qazanmağın Sürətli Yolları"
]

channels = ["TechAzerbaijan", "SportTV", "AI World", "FinanceUz", "DataCamp AZ", "SpaceDoc", "BakuVlogs", "CyberSec"]

# 100 sətirlik dolğun və real görünüşlü məlumat bazası
np.random.seed(42)
data = {
    'title': np.random.choice(titles, 100),
    'channel_title': np.random.choice(channels, 100),
    'views': np.random.randint(50000, 5000000, 100),
    'likes': np.random.randint(2000, 350000, 100),
    'comment_count': np.random.randint(100, 25000, 100)
}

df = pd.DataFrame(data)
print("--- DATASET PROBLEMİZ YARANDI! ---")

@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/api/top-trending")
def get_top_trending(limit: int = 10):
    top_videos = df.sort_values(by="views", ascending=False).head(limit)
    return top_videos.to_dict(orient="records")

@app.get("/api/stats")
def get_stats():
    return {
        "total_videos": len(df),
        "total_views": int(df["views"].sum()),
        "average_likes": float(df["likes"].mean())
    }

if __name__ == "__main__":
    uvicorn.run("backend:app", host="127.0.0.1", port=8005, reload=True)