import streamlit as st
import base64
from utils.functions import *
from dotenv import load_dotenv
import os

load_dotenv()

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        st.error(f"Error loading background image: {e}")
        return None

# Streamlit application setup
def main():
    st.set_page_config(page_title="Generate Blogs", page_icon='🤖', layout='centered', initial_sidebar_state='collapsed')

    base64_image = get_base64_image(os.getenv('BACKGROUND_IMAGE'))  # Update with your image path

    if base64_image:
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: url(data:image/jpg;base64,{base64_image});
                background-size: cover;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    st.header("Generate Blogs 🤖")

    st.markdown("""
        **Welcome to the Generate Blogs app!**  
        📝 This app allows you to quickly generate blog content based on a topic of your choice.  
        Simply enter the topic, select the number of words from the sidebar, and click the **Generate 🚀** button. You can also query the generated data for further analysis.
    """)

    input_text = st.text_input("Enter the Blog Topic")
    
    no_words = st.sidebar.slider('No of Words', 0, 1000, 100)  # default to 100
    st.sidebar.text(f"Selected No of Words: {no_words}")

    submit = st.button("Generate 🚀")

    if "response" not in st.session_state:
        st.session_state.response = None

    if submit:
        if input_text:
            try:
                llm, embed_model = model_selection()
                if llm and embed_model:
                    response = getLLamaresponse(input_text, no_words, llm)
                    if response:
                        st.session_state.response = response
                        save_load_from_disk(st.session_state.response, embed_model)
                        st.success("Blog saved to disk!")
                        st.write(st.session_state.response)
                        st.rerun()
                    else:
                        st.error("Failed to generate response.")
                else:
                    st.error("Failed to load models.")
            except Exception as e:
                st.error(f"Error generating blog: {e}")
        else:
            st.error("Please enter a blog topic.")

    if st.session_state.response:
        st.write("Stored response:", st.session_state.response)

    query_text = st.sidebar.text_input("Enter your query")
    query = st.sidebar.button("Query Data 🔍")

    if query and query_text:
        try:
            llm, embed_model = model_selection()
            if llm and embed_model:
                index = save_load_from_disk(st.session_state.response, embed_model)
                if index:
                    query_engine = index.as_query_engine()
                    query_response = query_engine.query(query_text)
                    st.markdown(query_response)
                else:
                    st.error("Failed to load index.")
            else:
                st.error("Failed to load models.")
        except Exception as e:
            st.error(f"Error querying data: {e}")

if __name__ == "__main__":
    main()