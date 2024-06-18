import streamlit as st
import pickle
import pandas as pd

def recommend(kerajinan):
    index = crochet[crochet['kerajinan'] == kerajinan].index[0]
    crochet_list = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6]

    recommended_crochet = []
    for i in crochet_list:
        recommended_crochet.append(crochet.iloc[i[0]].kerajinan)
        recommended_crochet.append(crochet.iloc[i[0]].link)
    return recommended_crochet


crochet_dict = pickle.load(open('crcohet_dict.pkl', 'rb'))
crochet = pd.DataFrame(crochet_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Crochet Recommender System")

selected_crochet = st.selectbox(
'Kerajinan apa yang ingin ada cari sebagai basis rekomendasi?',
crochet['kerajinan'].values)

if st.button("Recommend"):
    recommendation = recommend(selected_crochet)
    for i in recommendation:
        st.write(i)
