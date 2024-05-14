import streamlit as st
import pandas as pd
import numpy as np
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
colored_header("Classification automatique de produits dans des catégories", "Projet Rakuten challenge, il s'agit de pouvoir classifier des annonces dans des catégories de produit en fonction de leur titre et de leur description textuelle.")
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
  st.write("* Ce projet utilise deux classifieurs entraînés sur les désignations et descriptions issues de 84916 annonces.")
  st.write("* Les annonces ont été saisies par des utilisateurs et en tant que telles sont de qualité variables, avec notamment des erreurs, approximations ou niveau de détail différents.")
  
  col1, col2 = st.columns(2)
  with col1:
    st.write("* Malgré la présence d'images, nous avons gardé les classifieurs basés sur les données textuelles pour plusieurs raisons : ils ont été parmi les plus performants lors de nos évaluations mais aussi les plus rapides et les plus légers.")   
  with col2:
    st.image("https://fr.shopping.rakuten.com/photo/web-app-development-made-simple-with-streamlit-format-poche-10412352030_L_NOPAD.jpg", width=200)
    st.write("Exemple d'image produit, ici une image issue d'une annonce en ligne qui s'avère de bonne qualité.")

  st.write("* Cette application permet de voir comment les classifieur de régression logistique et machine à vecteur support traitent des données jamais vues par les modèles, issues de la validation du challenge pour lesquelles nous ne possédons pas les labels.")
  st.write("* Pour ce faire, elle applique la même chaîne de preprocessing du texte que lors de notre traitement des données d'entraînement et déclenche les prédictions en utilisant les modèles entrainés.")
  st.write("* Voici les catégories cible :")
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

  st.text_area("Texte préprocessé",
    value=texte_filtered)
  
  if st.button("Prédire la classe"):
    text_vector = tfidf_vectorizer.transform([texte_filtered])
    text_vector = pd.DataFrame(text_vector.toarray(), columns=tfidf_vectorizer.get_feature_names_out())
    clf = load("./resources/model_RL.joblib")
    clf_svm = load("./resources/model_clf_svm.joblib")
    pred = clf.predict(text_vector)
    pred_svm = clf_svm.predict(text_vector)
    resulting_category = categories_codes[categories_codes['cat_code']==pred[0]]
    resulting_category_svm = categories_codes[categories_codes['cat_code']==pred_svm[0]]
    st.write("#### Régression logistique :")
    st.write("Catégorie prédite =", resulting_category['Catégories'].iloc[0])
    st.write("Code produit correspondant =", resulting_category['prdtypecode'].iloc[0])
    st.write("#### Machine à vecteurs de support :")
    st.write("Catégorie prédite =", resulting_category_svm['Catégories'].iloc[0])
    st.write("Code produit correspondant =", resulting_category_svm['prdtypecode'].iloc[0])
    

if page == pages[2] :
    st.write("### Améliorations envisageables")
    st.write("#### Pour des données pré-existantes")
    st.write("* La version actuelle pourrait permettre la détection de mauvaises classifications par les utilisateurs.")
    st.write("* On pourrait réaliser un crawler qui parcourt les annonces Rakuten et pour chaque annonce compare sa catégorie avec celles issues des modèles. Les différences seraient persistées pour un contrôle.")
    st.write("#### Pour une annonce en cours de saisie")
    st.write("* On pourrait suggérer automatiquement des catégories à l'utilisateur à parir des données saisies pour favoriser une bonne catégorisation des annonces crées.")
    st.write("* Il est également envisageable de montrer des annonces similaires dans la même catégorie pour harmoniser les offres (notamment au niveau des prix de vente).")
