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

def liquid_visualizer():
    # ------------------ Configurations ------------------
    machine_data = {
        "SGA20": 100,
        "SGA40": 300,
        "SGA40WJ": 300
    }

    product_speeds = {
        "liquid (easy flow)": 27,
        "liquid (semi-viscous)": 25,
        "liquid (viscous)": 15
    }

    ASSET_DIR = "assets"
    MACHINE_IMAGE_DIR = "machine_images"

    image_map = {
        "SGA20": "liquid.png",
        "SGA40": "liquid.png",
        "SGA40WJ": "liquid_wj.png"
    }

    # ------------------ User Inputs ------------------
    st.title("Liquid Filler Visualizer")

    model_choice = st.selectbox("Select Model", ["All"] + list(machine_data.keys()), index=0)
    product_choice = st.selectbox("Select Product Type", list(product_speeds.keys()))
    bottle_width = st.number_input("Bottle Width (mm)", min_value=1, value=50)
    pack_height = st.number_input("Pack Height (mm)", min_value=1, value=120)
    max_plot_height_px = st.slider("Plot Height (pixels)", min_value=200, max_value=1500, value=1000, step=50)

    if st.button("Reset"):
        st.rerun()

    models_to_show = machine_data.keys() if model_choice == "All" else [model_choice]

    for model in models_to_show:
        pitch_distance = machine_data[model]
        speed = product_speeds[product_choice]
        bottles_per_cycle = max(1, int(pitch_distance / bottle_width))
        bottles_per_minute = bottles_per_cycle * speed

        bottle_img_path = os.path.join(ASSET_DIR, image_map[model])
        bottle_img = load_image(bottle_img_path)

        machine_image_path = os.path.join(MACHINE_IMAGE_DIR, f"{model}.png")
        machine_image = load_image(machine_image_path)

        total_width = bottles_per_cycle * bottle_width

        pixels_per_mm = max_plot_height_px / pack_height
        fig_height_inches = max_plot_height_px / 100.0
        fig_width_inches = (total_width * pixels_per_mm) / 100.0

        fig, ax = plt.subplots(figsize=(fig_width_inches, fig_height_inches))

        ax.set_xlim(0, total_width)
        ax.set_ylim(0, pack_height)
        ax.set_aspect('equal')
        ax.grid(True, linestyle='--', color='lightgray')

        for i in range(bottles_per_cycle):
            x = i * bottle_width
            ax.imshow(bottle_img, extent=(x, x + bottle_width, 0, pack_height), aspect='auto')

        ax.set_xticks(range(0, total_width + 1, 50))
        ax.set_yticks(range(0, pack_height + 1, 20))

        col_a, col_b = st.columns([3, 2], gap="large")

        with col_a:
            with st.container():
                st.markdown(f"### Model: {model}")
                st.markdown(f"<div class='metric-font'><b>Pitch Distance:</b> {pitch_distance} mm</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-font'><b>Cycles per Minute ({product_choice}):</b> {speed}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-font'><b>Bottles per Cycle:</b> {bottles_per_cycle}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-font'><b>Bottles per Minute:</b> {bottles_per_minute}</div>", unsafe_allow_html=True)

        col_plot, col_image = st.columns([3, 2], gap="large")

        with col_plot:
            st.pyplot(fig, clear_figure=True)

        with col_image:
            if machine_image:
                st.image(machine_image, caption=f"{model}", use_container_width=True)
            else:
                st.warning(f"Machine image not found for {model}")

            with st.container():
                st.markdown("### Machine Information")
                st.markdown("### Specifications")
            if model == "SGA20":
                st.write("SGA20: Compact design suitable for low to medium output with 100mm pitch indexing. Ideal for easy-flow liquids.")
                st.write("""
- **Max. Output:** 20 cycles/min, 5 bottles/cycle
- **Fill Capacity:** 1–20 ml/bottle
- **Packaging Material Width:** 120–240 mm
- **Packaging Material Thickness:** 0.3–0.4 mm
- **Machine Dimension (L×W×H):** 3.5×0.95×1.6 m
- **Weight:** 1400 kg
- **Power:** 13 kW
""")
            elif model == "SGA40":
                st.write("SGA40: Mid-range filler with 300mm pitch for larger bottles or multiple heads. Suited for easy to semi-viscous liquids.")
                st.write("""
- **Max. Output:** 35 cycles/min, 15 bottles/cycle
- **Fill Capacity:** 1–120 ml/bottle
- **Packaging Material Width:** 120–240 mm
- **Packaging Material Thickness:** 0.3–0.5 mm
- **Machine Dimension (L×W×H):** 8.1×1.6×1.8 m
- **Weight:** 5000 kg
- **Power:** 36–40 kW
""")
            elif model == "SGA40WJ":
                st.write("SGA40WJ: Enhanced variant of SGA40 with optional weighing and jacketed tanks. Optimized for viscous and sensitive liquids.")
                st.write("""
- **Max. Output:** 35 cycles/min, 15 bottles/cycle
- **Fill Capacity:** 1–120 ml/bottle
- **Packaging Material Width:** 120–240 mm
- **Packaging Material Thickness:** 0.3–0.5 mm
- **Machine Dimension (L×W×H):** 8.1×1.6×1.8 m
- **Weight:** 5000 kg
- **Power:** 36–40 kW
""")

            

