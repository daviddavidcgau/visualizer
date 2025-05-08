import streamlit as st
from PIL import Image
import os
import base64

from visualizers.blister import blister_visualizer
from visualizers.stick import stick_pack_visualizer
from visualizers.sachet import sachet_visualizer
from visualizers.liquid import liquid_visualizer

# Set page config FIRST
st.set_page_config(layout="wide")

# -------------------- Global CSS --------------------
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Aptos', sans-serif;
        }
        .fixed-banner {
            position: fixed;
            top: 60px; /* lowered below Streamlit top menu */
            left: 0;
            width: 100%;
            height: 80px;
            z-index: 9999;
            background-color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 5px 0;
        }
        .fixed-banner img {
            height: 65px;
            object-fit: contain;
        }
        .content-offset {
            margin-top: 170px; /* matches top offset + banner height */
        }
    </style>
""", unsafe_allow_html=True)

# -------------------- Top Banner --------------------
def top_banner():
    banner_path = os.path.join("assets", "banner.png")
    if os.path.exists(banner_path):
        with open(banner_path, "rb") as f:
            banner_data = f.read()
            encoded = base64.b64encode(banner_data).decode()
            banner_url = f"data:image/png;base64,{encoded}"
            st.markdown(f"""
                <div class="fixed-banner">
                    <img src="{banner_url}" alt="Banner">
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Banner image not found")

# -------------------- Main --------------------
def main():
    top_banner()  # Show banner on all pages
    st.markdown('<div class="content-offset"></div>', unsafe_allow_html=True)

    st.sidebar.title("Select Machine Type")
    machine_choice = st.sidebar.radio("Choose a machine to simulate:", [
        "Blister Packaging",
        "Sachet",
        "Stick Pack",
        "Liquid"
    ])

    if machine_choice == "Blister Packaging":
        blister_visualizer()
    elif machine_choice == "Stick Pack":
        stick_pack_visualizer()
    elif machine_choice == "Sachet":
        sachet_visualizer()
    elif machine_choice == "Liquid":
        liquid_visualizer()
    else:
        st.markdown(f"## {machine_choice} Module Coming Soon")
        st.info("This module is under development. Please check back later.")

if __name__ == '__main__':
    main()
