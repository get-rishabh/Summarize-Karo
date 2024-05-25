import streamlit as st

st.set_page_config(page_title="Multimodal Data Summarization Using Gemini")
from streamlit_option_menu import option_menu
import home, app1, app2, app3


class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({"title": title, "function": func})

    def run():
        with st.sidebar:
            app = option_menu(
                menu_title="Dashboard",
                options=[
                    "Home",
                    "Youtube Video Summarizer",
                    "Image Analyzer & Summarizer",
                    "Document Summarizer",
                ],
                icons=[
                    "house-door",
                    "youtube",
                    "file-earmark-image",
                    "file-earmark-pdf",
                ],
                menu_icon="bookmark-dash",
                default_index=0,
                styles={
                    "container": {
                        "padding": "5!important",
                        "background-color": "black",
                    },
                    "icon": {"color": "white", "font-size": "18px"},
                    "nav-link": {
                        "color": "white",
                        "font-size": "20px",
                        "text-align": "left",
                        "margin": "0px",
                        "--hover-color": "grey",
                    },
                    "nav-link-selected": {"background-color": "orange"},
                },
            )

        if app == "Home":
            home.app()
        if app == "Youtube Video Summarizer":
            app1.app()
        if app == "Image Analyzer & Summarizer":
            app2.app()
        if app == "Document Summarizer":
            app3.app()

    run()
