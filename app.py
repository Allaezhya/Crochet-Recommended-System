import streamlit as st
import pickle
import pandas as pd
from PIL import Image
import requests
import io

def recommend(kerajinan):
    index = crochet[crochet['kerajinan'] == kerajinan].index[0]
    crochet_list = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6]

    recommended_crochet = []
    base_url = 'https://github.com/Allaezhya/Crochet-Recommended-System'
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

st.title("Sistem Rekomendasi Kerajinan Rajut")

selected_crochet = st.selectbox(
'Mencri projek selanjutnya? Pilih salah satu',
crochet['kerajinan'].values)

if st.button("Rekomendasikan"):
    recommendations = recommend(selected_crochet)
    st.write(f"Rekomendasi untuk {selected_crochet}:")

    for rec in recommendations:
        kerajinan_name, link, gambar = rec
        st.subheader(kerajinan_name)
        st.write(f"[Link ke tutorial] ({link})")

        st.write(f"URL gambar: {gambar}")  # Debugging untuk memeriksa URL gambar
        try:
            response = requests.get(gambar, stream=True)
            if response.status_code == 200:
                image_bytes = io.BytesIO(response.content)
                image = Image.open(image_bytes)
                st.image(image, caption=kerajinan_name, use_column_width=True)
            else:
                st.write("Gambar tidak ditemukan!")
        except Exception as e:
            st.write(f"Error: {e}")
            st.write("Gambar tidak dapat dimuat.")
