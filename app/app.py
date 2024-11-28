import io
import os
import requests
import PyPDF2
import streamlit as st
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv(dotenv_path="../.env")

# Fonction pour extraire le texte d'un fichier PDF
def extract_text_from_binary(file):
    pdf_data = io.BytesIO(file)
    reader = PyPDF2.PdfReader(pdf_data)
    num_pages = len(reader.pages)
    text = ""

    for page in range(num_pages):
        current_page = reader.pages[page]
        text += current_page.extract_text()
    return text

# Fonction pour appeler l'API Flask
def call_api(text, type="gpt"):
    url = f"{os.getenv('API_URL')}/extract-{type}"
    headers = {"Content-Type": "application/json"}
    data = {"text": text}
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()['yaml']
        else:
            return f"Erreur API : {response.json().get('error', 'Erreur inconnue')}"
    except requests.exceptions.RequestException as e:
        return f"Erreur de connexion à l'API : {e}"

# Application Streamlit
def main():
    # Configurer la sidebar
    # Titre principal de l'application
    st.title("Resume Extractor")

    # Uploader de fichier
    uploaded_file = st.file_uploader("Téléverser un fichier PDF", type=["pdf"])

    if uploaded_file is not None:
        st.write("Fichier chargé avec succès.")
        try:
            # Extraire le texte du fichier PDF
            text = extract_text_from_binary(uploaded_file.read())
            st.write("Texte extrait avec succès. Extraction en cours...")

            # Appeler l'API Flask
            yaml_output_gpt = call_api(text)
            # yaml_output_mistral = call_api(text, "mistral")

            # Afficher les résultats avec GPT
            st.subheader("Résultats GPT (YAML)")
            st.text(yaml_output_gpt)

            # Afficher les résultats avec Mistral
            # st.subheader("Résultats Mistral")
            # st.text(yaml_output_mistral)

            # download button for yaml_output_gpt
            st.download_button("Télécharger le résultat", yaml_output_gpt, "yaml_output_gpt.yaml", key="download-button")


        except Exception as e:
            st.error(f"Une erreur est survenue : {e}")

if __name__ == "__main__":
    main()
