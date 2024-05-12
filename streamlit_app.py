import streamlit as st
import pandas as pd

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

icon()
colored_header("Classification automatique de produits dans des catégories", "Projet Rakuten challenge, il s'agit de pouvoir classifier des annonces dans des catégories de produit en fonction de leur titre, description textuelle et image.")
st.sidebar.title("Sommaire")
pages=["Introduction", "DataVizualization", "Modélisation"]
page=st.sidebar.radio("Aller vers", pages)
X_test=pd.read_csv('./resources/X_test_update.csv', index_col=0).fillna("")

if page == pages[0] : 
  st.write("### Introduction")
  st.write("Exemple d'image produit")
  st.image("https://fr.shopping.rakuten.com/photo/web-app-development-made-simple-with-streamlit-format-poche-10412352030_L_NOPAD.jpg")

if page == pages[1] : 
  st.write("### DataVizualization")
  X_test=pd.read_csv('./resources/X_test_update.csv', index_col=0)
  X_train=pd.read_csv('./resources/X_train_update.csv', index_col=0)
  Y_train=pd.read_csv('./resources/Y_train_CVw08PX.csv', index_col=0)

if page == pages[2] : 
  st.write("### Modélisation")
  st.write("Initialisation avec des valeurs de test aléatoires :")
  X_test_random = X_test.sample().iloc[0]
  designation = st.text_input("Designation", value=X_test_random['designation'], key="designation")
  st.text_area("Description",
   value=X_test_random['description'])
  st.text_input("Image URL", "https://www.example.com")

  col1, col2 = st.columns(2)
  if col1.button("Use another random test data entry"):
    # The simple click of the button will redraw UI and select another random item
    useless = None

  col2.button("Predict class")
