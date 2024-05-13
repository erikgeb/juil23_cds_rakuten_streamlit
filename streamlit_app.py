import streamlit as st
import pandas as pd
import numpy as np
import nltk
import html
import re
from unidecode import unidecode
from joblib import load

def colored_header(label, description=None, color_code="#803df5"):
    """Shows a header with a colored underline and an optional description."""
    st.subheader(label)
    st.write(
        f'<hr style="background-color: {color_code}; margin-top: 0; margin-bottom: 0; height: 3px; border: none; border-radius: 3px;">',
        unsafe_allow_html=True,
    )
    if description:
        st.caption(description)

def icon(emoji: str = "📊"):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )

def filter_stop_words(list):
    result_list=[]
    for mot in list:
        if (mot not in stop_words and len(mot)>=2):
            result_list.append(mot)
    return result_list

def preprocessInput(text_input):
    texte_filtered = html.unescape(text_input).lower().strip()
    texte_filtered = re.sub(r"[^a-z]+", " ", re.sub('<[^<]+?>', ' ', unidecode(re.sub('n°', 'numero ', texte_filtered))))
    splitted_words = texte_filtered.split()
    return " ".join(filter_stop_words(splitted_words))

icon()
colored_header("Classification automatique de produits dans des catégories", "Projet Rakuten challenge, il s'agit de pouvoir classifier des annonces dans des catégories de produit en fonction de leur titre, description textuelle et image.")
st.sidebar.title("Sommaire")
pages=["Introduction", "Classification automatique", "Améliorations"]
page=st.sidebar.radio("Aller vers", pages)
X_test=pd.read_csv('./resources/X_test_update.csv', index_col=0).fillna("")
# load stop words directly from disk to avoid reconfiguring them (which requires download of extra nltk packages)
stop_words = np.load("./resources/stop_words.npy")
categories_codes = pd.read_csv("./resources/categories_codes.csv", index_col=0)
tfidf_vectorizer = load('./resources/tfidf_vectorizer.pkl')

if page == pages[0] : 
  st.write("### Introduction")

  st.write("Exemple d'image produit")
  st.image("https://fr.shopping.rakuten.com/photo/web-app-development-made-simple-with-streamlit-format-poche-10412352030_L_NOPAD.jpg")
  st.dataframe(data=categories_codes)

if page == pages[1] : 
  st.write("### Classification automatique")
  col1, col2 = st.columns(2)
  if "chosen_idx" not in st.session_state:
    st.session_state.chosen_idx = np.random.randint(0, len(X_test))
  X_test_random = X_test.iloc[st.session_state.chosen_idx]

  with col1:
    st.write("Index de l'item:", st.session_state.chosen_idx)
  with col2:
    if st.button("Chager une autre entrée de test aléatoire"):
      st.session_state.chosen_idx = np.random.randint(0, len(X_test))
      st.rerun()

  designation = st.text_input("Designation", value=X_test_random['designation'], key="designation")
  st.text_area("Description",
  value=X_test_random['description'])

  st.write("Initialisation avec des valeurs de test aléatoires :")    
  # st.text_input("Image URL", "https://www.example.com")
  texte_filtered = preprocessInput(X_test_random['designation'] + ' ' + X_test_random['description'])
  #texte_filtered = html.unescape(texte_filtered).lower().strip()
  #texte_filtered = re.sub(r"[^a-z]+", " ", re.sub('<[^<]+?>', ' ', unidecode(re.sub('n°', 'numero ', texte_filtered))))
  #splitted_words = texte_filtered.split()
  #texte_filtered = " ".join(filter_stop_words(splitted_words))
  
  st.text_area("Texte préprocessé",
    value=texte_filtered)
  
  if st.button("Prédire la classe"):
    text_vector = tfidf_vectorizer.transform([texte_filtered])
    text_vector = pd.DataFrame(text_vector.toarray(), columns=tfidf_vectorizer.get_feature_names_out())
    clf = load("./resources/model_RL.joblib")
    pred = clf.predict(text_vector)
    resulting_category = categories_codes[categories_codes['cat_code']==pred[0]]
    st.write("Catégorie prédite =", resulting_category['Catégories'].iloc[0])
    st.write("Code produit correspondant =", resulting_category['prdtypecode'].iloc[0])
    
if page == pages[2] :
    multi = '''### Améliorations envisageables

    Le problème a été abordé comme une classification à partir des données de produits pré-existantes.
    En tant que tel, l'utilité de cette solution semble vouée à être de la détection de mauvaise classification
    par les utilisateurs lors de la création de leur annonce ou la proposition d'une catégorisation automatique 
    lorsqu'une annonce est en cours de création.
    '''
    st.markdown(multi)