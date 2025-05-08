import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import pandas as pd
import os

def stick_pack_visualizer():
    # Machine models and their film widths
    machine_data = {
        "DXDB960": 960,
        "DBF1000": 1000
    }

    # Speeds depending on machine and product
    speed_data = {
        "DXDB960": {
            "Granule": 70,
            "liquid (easy flow)": 70,
            "liquid (semi-viscous)": 50,
            "liquid (viscous)": 40,
            "powder (easy flow)": 50,
            "powder (some difficulty)": 40
        },
        "DBF1000": {
            "Granule": 45,
            "liquid (easy flow)": 45,
            "liquid (semi-viscous)": 40,
            "liquid (viscous)": 30,
            "powder (easy flow)": 40,
            "powder (some difficulty)": 30
        }
    }

    ASSET_DIR = "assets"
    MACHINE_IMAGE_DIR = "machine_images"

    def load_image_safe(path, placeholder_color=(255, 255, 255)):
        if os.path.exists(path):
            return Image.open(path)
        else:
            st.warning(f"Image not found: {path}")
            return Image.new("RGB", (100, 100), placeholder_color)

    stick_img = load_image_safe(os.path.join(ASSET_DIR, "stick.png"))

    # User Inputs
    model = st.selectbox("Select Machine Model", options=["All Models"] + list(machine_data.keys()))
    pack_width = st.number_input("Pack Width (mm)", value=23)
    pack_height = st.number_input("Pack Height (mm)", value=100)
    product_type = st.selectbox("Select Product Type", options=[
        "Granule",
        "liquid (easy flow)",
        "liquid (semi-viscous)",
        "liquid (viscous)",
        "powder (easy flow)",
        "powder (some difficulty)"
    ])

    if st.button("Reset"):
        st.rerun()

    def draw_stick_pack(model_name):
        film_width = machine_data[model_name]
        speed = speed_data[model_name][product_type]

        # Calculate number of sticks per cycle
        sticks_per_cycle = film_width / ((pack_width * 2) + 10)
        sticks_per_cycle = int(sticks_per_cycle)

        # Calculate packs per minute
        packs_per_minute = sticks_per_cycle * speed

        st.markdown(f"### Model: {model_name}")
        st.markdown(f"Cycles per Minute ({product_type}): {speed}")
        st.markdown(f"Sticks per Cycle: {sticks_per_cycle}")
        st.markdown(f"Packs per Minute (Feeding): {packs_per_minute}")

        # MATLAB Plot
        big_width = film_width
        big_height = pack_height + 40  # add some margin

        fig, ax = plt.subplots(figsize=(10, 2))
        ax.set_xlim(0, big_width)
        ax.set_ylim(0, big_height)
        ax.set_aspect('equal', adjustable='box')
        ax.grid(True, which='both', color='lightgray', linestyle='--', linewidth=0.5)
        ax.set_xticks(range(0, big_width + 1, 20))
        ax.set_yticks(range(0, big_height + 1, 20))
        ax.set_xticklabels(range(0, big_width + 1, 20), rotation=90)
        ax.set_yticklabels(range(0, big_height + 1, 20))

        stick_spacing = big_width / (sticks_per_cycle + 1)

        for i in range(sticks_per_cycle):
            x = stick_spacing * (i + 1) - (pack_width / 2)
            y = (big_height - pack_height) / 2
            ax.add_patch(patches.Rectangle((x, y), pack_width, pack_height, linewidth=1, edgecolor='blue', facecolor='none'))
            ax.imshow(stick_img, extent=(x, x + pack_width, y, y + pack_height), zorder=2)

        ax.set_title(f"Stick Pack Layout - {model_name} ({sticks_per_cycle} Sticks per Cycle)")

        # Layout with Machine Image
        machine_image_path = os.path.join(MACHINE_IMAGE_DIR, f"{model_name}.png")
        col1, col2 = st.columns([3, 2])
        with col2:
            if os.path.exists(machine_image_path):
                st.image(machine_image_path, caption=f"{model_name} Machine", use_container_width=True)
            else:
                st.warning(f"Image not found for {model_name}")
        with col1:
            st.pyplot(fig)

            # Display additional specifications
            if model_name == "DBF1000":
                st.markdown("**Specifications**")
                st.markdown("""
                **Speed:** ≤40 cycles/min  
                **Sachet Length:** 60-200 mm  
                **Sachet Width:** 20-45 mm  
                **Max Sealing Width:** 1000 mm  
                **Packing Dose (Granule/Powder):** 40-153 g  
                **Packing Dose (Liquid):** 1.5 - 20 mL  
                **Packaging Material Width:** 1000 mm  
                **Machine Dimension (LxWxH):** 1.8x1.86x2.5 m  
                **Weight:** 2600 kg  
                **Power:** 11.25 kW  
                """)
            elif model_name == "DXDB960":
                st.markdown("**Specifications**")
                st.markdown("""
                **Speed:** ≤60 cycles/min  
                **Sachet Length:** 90-160 mm  
                **Sachet Width:** 25-40 mm  
                **Max Sealing Width:** 960 mm  
                **Packing Dose (Granule/Powder):** 40-152 g  
                **Packing Dose (Liquid):** 1 - 20 mL  
                **Packaging Material Width:** 960 mm  
                **Machine Dimension (LxWxH):** 2.4x1.9x3.1 m  
                **Weight:** 3500 kg  
                **Power:** 23 kW  
                """)

    # Logic to draw
    if model == "All Models":
        for m in machine_data.keys():
            draw_stick_pack(m)
    else:
        draw_stick_pack(model)
