import streamlit as st
import pickle
import pandas as pd
import os
from PIL import Image
import requests

def recommend(kerajinan):
    index = crochet[crochet['kerajinan'] == kerajinan].index[0]
    crochet_list = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6]

    recommended_crochet = []
    base_url = 'https://raw.githubusercontent.com/Allaezhya/Crochet-Recommended-System/repository/utama/images'
    
    for i in crochet_list:
        kerajinan_name = crochet.iloc[i[0]].kerajinan
        link = crochet.iloc[i[0]].link
        image_jalur = crochet.iloc[i[0]].gambar

        full_image_path = base_url + image_jalur

        recommended_crochet.append([kerajinan_name, link, full_image_path])
    return recommended_crochet

crochet_dict = pickle.load(open('crochet_dict.pkl', 'rb'))
crochet = pd.DataFrame(crochet_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Crochet Recommender System")

selected_crochet = st.selectbox(
'Kerajinan apa yang ingin ada cari sebagai basis rekomendasi?',
crochet['kerajinan'].values)

if st.button("Recommend"):
    recommendations = recommend(selected_crochet)

    st.write(f"Rekomendasi untuk {selected_crochet}:")
    for rec in recommendations:
        kerajinan_name, link, gambar = rec
        st.subheader(kerajinan_name)
        st.write(f"[Link ke tutorial] ({link})")

        st.write(f"URL gambar: {gambar}")  # Debugging untuk memeriksa path gambar
        try:
            image = Image.open(requests.get(gambar, stream=True).raw)
            st.image(image, caption=kerajinan_name, use_column_width=True)
        except Exception as e:
            st.write("Gambar tidak ditemukan!")
