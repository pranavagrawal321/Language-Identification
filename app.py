import streamlit as st
import fasttext


def get_predictions(text):
    loaded_model = fasttext.load_model("models/fasttext_finetuned.bin")
    return loaded_model.predict(text)[0][0]


def on_submit():
    result = get_predictions(text)
    st.write("Predicted language:", result.split("__")[-1])


st.title("Language Identification")

text = st.text_input("Enter a text", key="text")

if st.button(label="Submit", on_click=on_submit):
    on_submit()