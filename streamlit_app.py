import streamlit as st

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


#st.title("Projet de classification de produits dans des catégories")
icon()
colored_header("Classification automatique de produits dans des catégories", "Projet Rakuten challenge, il s'agit de pouvoir classifier des annonces dans des catégories de produit en fonction de leur titre, description textuelle et image.")
st.sidebar.title("Sommaire")
pages=["Introduction", "Exploration", "DataVizualization", "Modélisation"]
page=st.sidebar.radio("Aller vers", pages)

if page == pages[0] : 
  st.write("### Introduction")

  st.code("exampleCode = \"this is an example\"")
  st.code("exampleCode = exampleCode + \".\"")

  st.image("https://fr.shopping.rakuten.com/photo/web-app-development-made-simple-with-streamlit-format-poche-10412352030_L_NOPAD.jpg")

if page == pages[1] : 
  st.write("### Exploration")

if page == pages[2] : 
  st.write("### DataVizualization")

if page == pages[3] : 
  st.write("### Modélisation")

