import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
import os
import math

@st.cache_data

def load_image(path):
    if os.path.exists(path):
        return Image.open(path)
    else:
        return None

def sachet_visualizer():
    # ------------------ Configurations ------------------
    machine_data = {
        "DXDK900A": 936,
        "DXDK1200": 1236,
        "DXDP450": 450
    }

    product_speeds = {
        "Granule": 55,
        "Powder (easy flow)": 30,
        "Powder (some difficulty)": 30,
        "Liquid (easy flow)": 55,
        "Liquid (semi-viscous)": 45,
        "Liquid (viscous)": 30
    }

    machine_specs = {
        "DXDK900A": {
            "Speed": "≤65 cycles/min",
            "Sachet Length": "50-180 mm",
            "Sachet Width": "40-150 mm",
            "Max Sealing Width": "450 mm",
            "Packing Dose (Granule/Powder)": "40-150 g",
            "Packing Dose (Liquid)": "1-20 mL",
            "Packaging Material Width": "936 mm",
            "Machine Dimension": "1.6x1.62x2.1 m",
            "Weight": "1200 kg",
            "Power": "13 kW"
        },
        "DXDK1200": {
            "Speed": "≤80 cycles/min",
            "Sachet Length": "40-180 mm",
            "Sachet Width": "40-170 mm",
            "Max Sealing Width": "550 mm",
            "Packing Dose (Granule/Powder)": "40-151 g",
            "Packing Dose (Liquid)": "1-30 mL",
            "Packaging Material Width": "1190-1250 mm",
            "Machine Dimension": "2.2x2.1x2.15 m",
            "Weight": "1200 kg",
            "Power": "13 kW"
        },
        "DXDP450": {
            "Speed": "90 cycles/min",
            "Sachet Length": "-",
            "Sachet Width": "-",
            "Max Sealing Width": "450 mm",
            "Packing Dose (Granule/Powder)": "40-154 g",
            "Packing Dose (Liquid)": "-",
            "Packaging Material Width": "450 mm",
            "Machine Dimension": "1.6x1.4x2.3 m",
            "Weight": "1500 kg",
            "Power": "8 kW"
        }
    }

    ASSET_DIR = "assets"
    MACHINE_IMAGE_DIR = "machine_images"

    sachet_img_path = os.path.join(ASSET_DIR, "sachet.png")
    sachet_img = load_image(sachet_img_path)

    if sachet_img:
        sachet_img = sachet_img.resize((50, 80))  # Resize for consistent plotting

    # ------------------ User Inputs ------------------
    st.title("Sachet Pack Visualizer")

    model_choice = st.selectbox("Select Model", ["All"] + list(machine_data.keys()))
    product_choice = st.selectbox("Select Product Type", list(product_speeds.keys()))
    pack_width = st.number_input("Pack Width (mm)", min_value=1, value=60)
    pack_height = st.number_input("Pack Height (mm)", min_value=1, value=80)

    if st.button("Reset"):
        st.rerun()

    models_to_show = machine_data.keys() if model_choice == "All" else [model_choice]

    # ------------------ Visualizations ------------------
    for model in models_to_show:
        # Film width processing: cut in half, subtract 10mm from each side of half width
        original_film_width = machine_data[model]
        if model in ["DXDK900A", "DXDK1200"]:
            film_width = (original_film_width / 2) - 20  # 10mm buffer on each side of half
        else:
            film_width = original_film_width
        speed = product_speeds[product_choice]

        number_of_sachets = max(1, int(film_width / pack_width))
        sachets_per_minute = number_of_sachets * speed

        st.markdown(f"### Model: {model}")
        st.markdown(f"<div class='metric-font'><b>Cycles per Minute ({product_choice}):</b> {speed}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-font'><b>Sachets per Cycle:</b> {number_of_sachets}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-font'><b>Sachets per Minute (Feeding):</b> {sachets_per_minute:.2f}</div>", unsafe_allow_html=True)

        #matlab plot
        fig, ax = plt.subplots(figsize=(10, 1))
        start_x = 10
        gap = 0  # No gap between sachets
        total_width = start_x + pack_width * number_of_sachets

        ax.set_xlim(0, total_width)
        ax.set_ylim(0, pack_height)
        ax.set_aspect('equal', adjustable='box')
        ax.grid(True, linestyle='--', color='lightgray')

        for i in range(number_of_sachets):
            x = start_x + pack_width * i
            ax.imshow(sachet_img, extent=(x, x + pack_width, 0, pack_height), aspect='auto')

        ax.set_xticks(range(0, int(film_width) + 1, 50))
        ax.set_yticks(range(0, pack_height + 1, 20))

        col1, col2 = st.columns([3, 2])

        with col1:
            st.pyplot(fig, clear_figure=True)
            # Insert specifications
            specs = machine_specs.get(model, {})
            st.markdown("<h6>Machine Specifications</h6>", unsafe_allow_html=True)
            for k, v in specs.items():
                st.markdown(f"<div style='line-height:1.1'><small><b>{k}:</b> {v}</small></div>", unsafe_allow_html=True)

        with col2:
            machine_image_path = os.path.join(MACHINE_IMAGE_DIR, f"{model}.png")
            machine_image = load_image(machine_image_path)
            if machine_image:
                st.image(machine_image, caption=f"{model}", use_container_width=True)
            else:
                st.warning(f"Machine image not found for {model}")

    # Close the div
    st.markdown("""
        </div>
    """, unsafe_allow_html=True)
