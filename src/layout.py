import streamlit as st
from PIL import Image


class CustomLayout:

    @classmethod
    def apply(cls) -> None:
        # Apply all layout component
        # cls.hide_image_buttons()
        cls.hide_streamlit_marks()
        cls.condense_container()

    @staticmethod
    def hide_streamlit_marks() -> None:
        """Hide streamlit button and copyright."""
        st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def condense_container(border_size: int = 0) -> None:
        """Condense the container by reducing all paddings."""
        st.markdown(f"""
        <style>
            .reportview-container .main .block-container{{
                padding-top: {border_size}rem;
                padding-right: {border_size}rem;
                padding-left: {border_size}rem;
                padding-bottom: {border_size}rem;
            }}
            
            .stMarkdown > div > p {{
                margin: {border_size};
            }}
        </style>""", unsafe_allow_html=True)

    @staticmethod
    def hide_image_buttons() -> None:
        """Hide streamlit's "enlarge" buttons on images."""
        st.markdown("""
        <style>
            div:nth-child(1) > div > div > button {
                display: None !important;
                visibility: hidden;
            }
        </style>
        """, unsafe_allow_html=True)


class CodeText:

    def __init__(self):
        self.__apply_css()

    @staticmethod
    def __apply_css() -> None:
        """
        Effectively create the BigText component by adding its CSS to the
        page.
        """
        st.markdown("""
        <style>
            .stCodeBlock {
                margin: 0;
                width: 200px
            }
            
            .stCodeBlock > pre {
                padding-top: 8px;
                padding-bottom: 8px;
            }
            
            .stCodeBlock > pre > code > span {
                font-size: 30px;
                line-height: 30px;
            }
            
            .stCodeBlock > div {
                display: flex;
                flex-direction: column;
                justify-content: space-around;
            }
            
            .stCodeBlock button {
                opacity: 1;
                transform: scale(1);
                outline: none;
                color: rgb(49, 51, 63);
                transition: unset !important;
            }
        </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def write(text) -> None:
        """Write big text."""
        st.code(text, language="python")


def set_page_config(title: str, favicon_path: str = None):
    """Set page configuration."""

    # Load the favicon image
    favicon = None
    if favicon_path:
        favicon = Image.open(favicon_path)

    # Set page config
    st.set_page_config(
        page_title=title,
        page_icon=favicon,
    )


def display_image(image_path: str):
    image: Image = Image.open(image_path)
    st.image(image=image)
