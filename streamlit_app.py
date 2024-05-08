import streamlit as st

st.title("Projet de classification de produits dans des catégories")
st.sidebar.title("Sommaire")
pages=["Introduction", "Exploration", "DataVizualization", "Modélisation"]
page=st.sidebar.radio("Aller vers", pages)

if page == pages[0] : 
  st.write("### Introduction")

if page == pages[1] : 
  st.write("### Exploration")

if page == pages[2] : 
  st.write("### DataVizualization")

if page == pages[3] : 
  st.write("### Modélisation")

