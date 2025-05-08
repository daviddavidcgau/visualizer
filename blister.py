import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import pandas as pd
import os

def blister_visualizer():
    product_data = {
        "Capsule 0": 420,
        "Capsule 1": 450,
        "Capsule 2": 500,
        "Capsule 3": 400,
        "Tablet Round": 500,
        "Tablet Elong.": 300
    }

    material_data = {
        "Alu/Alu": 85,
        "Alu/PVC": 150
    }

    packaging_data = {
        "Model": ["DPP140", "DPP250", "DPP300", "DPP500", "DPH260", "DPH270", "DPH300", "DPH370"],
        "W": [160, 240, 280, 480, 160, 270, 320, 335],
        "H": [110, 160, 160, 160, 110, 260, 270, 270]
    }

    df_models = pd.DataFrame(packaging_data)

    spec_data = {
        "DPH260": {"Type": "Platen-Roller", "Output": "150 cuts/min", "Area": "260x270 mm", "Depth": "12 mm", "Material Width": "262 mm", "Dimensions": "2.9x0.5x1.7 m", "Weight": "2000 kg", "Power": "17-22 kW"},
        "DPH270": {"Type": "Platen-Roller", "Output": "150 cuts/min", "Area": "250x270 mm", "Depth": "12 mm", "Material Width": "270 mm", "Dimensions": "5.1x1.2x2.0 m", "Weight": "3500 kg", "Power": "26.5 kW"},
        "DPH300": {"Type": "Platen-Roller", "Output": "200 cuts/min", "Area": "270x320 mm", "Depth": "12 mm", "Material Width": "320 mm", "Dimensions": "5.8x1.5x2.0 m", "Weight": "5000 kg", "Power": "35 kW"},
        "DPH370": {"Type": "Platen-Roller", "Output": "230 cuts/min", "Area": "270x335 mm", "Depth": "12 mm", "Material Width": "380 mm", "Dimensions": "5.5x1.3x2.0 m", "Weight": "3500 kg", "Power": "27.5 kW"},
        "DPP140": {"Type": "Platen-Platen", "Output": "20-35 cuts/min", "Area": "110x160 mm", "Depth": "30 mm", "Material Width": "100-150 mm", "Dimensions": "2.2x0.6x1.6 m", "Weight": "1050 kg", "Power": "4.8-5.1 kW"},
        "DPP250": {"Type": "Platen-Platen", "Output": "20-35 cuts/min", "Area": "160x240 mm", "Depth": "30 mm", "Material Width": "250 mm", "Dimensions": "", "Weight": "", "Power": ""},
        "DPP300": {"Type": "Platen-Platen", "Output": "20-35 cuts/min", "Area": "160x280 mm", "Depth": "30 mm", "Material Width": "300 mm", "Dimensions": "", "Weight": "", "Power": ""},
        "DPP500": {"Type": "Platen-Platen", "Output": "15-30 cuts/min", "Area": "160x480 mm", "Depth": "30 mm", "Material Width": "500 mm", "Dimensions": "4.6x2.9x1.7 m", "Weight": "2800 kg", "Power": "15 kW"}
    }

    ASSET_DIR = "assets"
    MACHINE_IMAGE_DIR = "machine_images"

    def load_image_safe(path, placeholder_color=(255, 255, 255)):
        if os.path.exists(path):
            return Image.open(path)
        else:
            st.warning(f"Image not found: {path}")
            return Image.new("RGB", (100, 100), placeholder_color)

    blister_landscape_img = load_image_safe(os.path.join(ASSET_DIR, "blank_landscape.png"))
    blister_portrait_img = load_image_safe(os.path.join(ASSET_DIR, "blank_portrait.png"))
    dose_img = load_image_safe(os.path.join(ASSET_DIR, "dose.png"))

    def draw_dose_images(ax, x, y, small_width, small_height, doses_x, doses_y):
        spacing_margin = 0.1
        usable_width = small_width * (1 - 2 * spacing_margin)
        usable_height = small_height * (1 - 2 * spacing_margin)

        img_aspect = dose_img.width / dose_img.height

        max_dose_w = usable_width / (doses_x + 1)
        max_dose_h = usable_height / (doses_y + 1)

        if img_aspect > max_dose_w / max_dose_h:
            dose_w = max_dose_w
            dose_h = dose_w / img_aspect
        else:
            dose_h = max_dose_h
            dose_w = dose_h * img_aspect

        total_dose_width = doses_x * dose_w
        total_dose_height = doses_y * dose_h

        gap_x = (usable_width - total_dose_width) / (doses_x + 1)
        gap_y = (usable_height - total_dose_height) / (doses_y + 1)

        start_x = x + small_width * spacing_margin
        start_y = y + small_height * spacing_margin

        for i in range(doses_x):
            for j in range(doses_y):
                dx = start_x + gap_x * (i + 1) + dose_w * i
                dy = start_y + gap_y * (j + 1) + dose_h * j
                ax.imshow(dose_img, extent=(dx, dx + dose_w, dy, dy + dose_h))

    def draw_blister_background(ax, x, y, w, h, blister_img):
        ax.imshow(blister_img, extent=(x, x + w, y, y + h), zorder=0)

    def calculate_and_visualize_rectangles(big_width, big_height, small_width, small_height, doses_x, doses_y, model_name, use_landscape=True):
        spacing = 5
        edge_spacing = 2.5

        effective_big_width = big_width - 2 * edge_spacing
        effective_big_height = big_height - 2 * edge_spacing
        effective_small_width = small_width + spacing
        effective_small_height = small_height + spacing

        num_across = int(effective_big_width // effective_small_width)
        num_down = int(effective_big_height // effective_small_height)

        remaining_width = effective_big_width - (num_across * effective_small_width)
        remaining_height = effective_big_height - (num_down * effective_small_height)

        start_x = edge_spacing + (remaining_width / 2)
        start_y = edge_spacing + (remaining_height / 2)

        total_rectangles = num_across * num_down

        fig, ax = plt.subplots()
        ax.set_xlim(0, big_width)
        ax.set_ylim(0, big_height)
        ax.set_aspect('equal', adjustable='box')
        ax.grid(True, which='both', color='lightgray', linestyle='--', linewidth=0.5)
        ax.set_xticks(range(0, big_width + 1, 20))
        ax.set_yticks(range(0, big_height + 1, 20))
        ax.set_xticklabels(range(0, big_width + 1, 20), rotation=90)

        for i in range(num_across):
            for j in range(num_down):
                x = start_x + i * effective_small_width
                y = start_y + j * effective_small_height
                draw_blister_background(ax, x, y, small_width, small_height, blister_landscape_img if use_landscape else blister_portrait_img)
                draw_dose_images(ax, x, y, small_width, small_height, doses_x, doses_y)

        ax.set_title(f"Blister Packs per Forming Plate: {total_rectangles} ({model_name})")
        return fig, total_rectangles

    def calculate_packs_per_minute(product_type, doses_per_row, rows):
        speed = product_data[product_type]
        return (speed / doses_per_row) * rows

    def calculate_packs_per_minute_material(material_type, rows):
        speed = material_data[material_type]
        return speed * rows

    selected_model = st.selectbox("Model", options=['All', 'All DPP', 'All DPH'] + df_models['Model'].tolist(), index=4)
    pack_width = st.number_input("Pack Width (mm)", value=78)
    pack_height = st.number_input("Pack Height (mm)", value=56)
    doses_per_row = st.number_input("Doses per Row", value=6)
    doses_per_column = st.number_input("Doses per Column", value=2)
    product_type = st.selectbox("Product Type", options=list(product_data.keys()), index=2)
    material_type = st.selectbox("Material Type", options=list(material_data.keys()), index=1)

    if st.button("Reset"):
        st.rerun()

    models_to_show = df_models.copy()
    if selected_model == "All DPP":
        models_to_show = df_models[df_models['Model'].str.startswith("DPP")]
    elif selected_model == "All DPH":
        models_to_show = df_models[df_models['Model'].str.startswith("DPH")]
    elif selected_model != "All":
        models_to_show = df_models[df_models['Model'] == selected_model]

    for _, row in models_to_show.iterrows():
        model_name = row['Model']
        width = row['W']
        height = row['H']

        num_rows_landscape = int(height // (pack_height + 5))
        num_rows_portrait = int(height // (pack_width + 5))

        ppm_feed_landscape = calculate_packs_per_minute(product_type, doses_per_row, num_rows_landscape)
        ppm_mat_landscape = calculate_packs_per_minute_material(material_type, num_rows_landscape)

        ppm_feed_portrait = calculate_packs_per_minute(product_type, doses_per_column, num_rows_portrait)
        ppm_mat_portrait = calculate_packs_per_minute_material(material_type, num_rows_portrait)

        machine_image_path = os.path.join(MACHINE_IMAGE_DIR, f"{model_name}.jpg")

        st.markdown(f"### Model: {model_name}")

        # Landscape Orientation
        st.markdown(f"**Landscape Orientation:**")
        if ppm_feed_landscape <= ppm_mat_landscape:
            st.markdown(f"<b>Packs per minute (Feeding): {ppm_feed_landscape:.2f}</b>", unsafe_allow_html=True)
            st.markdown(f"<span style='font-size: 0.75em;'>Packs per minute (Material): {ppm_mat_landscape:.2f}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<b>Packs per minute (Material): {ppm_mat_landscape:.2f}</b>", unsafe_allow_html=True)
            st.markdown(f"<span style='font-size: 0.75em;'>Packs per minute (Feeding): {ppm_feed_landscape:.2f}</span>", unsafe_allow_html=True)

        fig1, _ = calculate_and_visualize_rectangles(width, height, pack_width, pack_height, doses_per_row, doses_per_column, model_name, use_landscape=True)
        col1, col2 = st.columns([3, 2])
        with col2:
            if os.path.exists(machine_image_path):
                st.image(machine_image_path, caption=f"{model_name} Machine", use_container_width=True)
            else:
                st.warning(f"Image not found for {model_name}")

            # Show machine specifications
            if model_name in spec_data:
                spec = spec_data[model_name]
                st.markdown("<br>".join([f"**{k}:** {v}" for k, v in spec.items()]), unsafe_allow_html=True)

        with col1:
            st.pyplot(fig1)

        # Portrait Orientation
        st.markdown(f"**Portrait Orientation:**")
        if ppm_feed_portrait <= ppm_mat_portrait:
            st.markdown(f"<b>Packs per minute (Feeding): {ppm_feed_portrait:.2f}</b>", unsafe_allow_html=True)
            st.markdown(f"<span style='font-size: 0.75em;'>Packs per minute (Material): {ppm_mat_portrait:.2f}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<b>Packs per minute (Material): {ppm_mat_portrait:.2f}</b>", unsafe_allow_html=True)
            st.markdown(f"<span style='font-size: 0.75em;'>Packs per minute (Feeding): {ppm_feed_portrait:.2f}</span>", unsafe_allow_html=True)

        fig2, _ = calculate_and_visualize_rectangles(width, height, pack_height, pack_width, doses_per_column, doses_per_row, model_name, use_landscape=False)
        col3, _ = st.columns([3, 2])
        with col3:
            st.pyplot(fig2)
