import streamlit as st
import subprocess
import os
import tempfile
from PIL import Image
import base64
import json
import shutil
import sys
import time
import io
import re

# Set page configuration
st.set_page_config(page_title="Paint by Numbers Generator", layout="wide")

st.title("Paint by Numbers Generator")
st.markdown("Generate paint by number images from any input image.")

# Create a session state to store results
if 'results' not in st.session_state:
    st.session_state.results = None
if 'palette_info' not in st.session_state:
    st.session_state.palette_info = None
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'temp_dir' not in st.session_state:
    st.session_state.temp_dir = tempfile.mkdtemp()

# Function to display SVG
def display_svg(svg_path):
    with open(svg_path, "r") as f:
        svg_content = f.read()
    st.components.v1.html(svg_content, height=600)

# Function to display image
def display_image(image_path):
    image = Image.open(image_path)
    st.image(image, use_column_width=True)

# Create a settings form
with st.expander("Settings", expanded=False):
    col1, col2 = st.columns(2)

    with col1:
        num_colors = st.number_input("Number of colors", min_value=2, max_value=64, value=16)
        min_facet_size = st.number_input("Minimum facet size (pixels)", min_value=1, max_value=100, value=20)
        max_facets = st.number_input("Maximum number of facets", min_value=10, max_value=10000, value=100)

    with col2:
        border_segments = st.number_input("Border segment complexity reduction", min_value=0, max_value=5, value=2)
        cleanup_runs = st.number_input("Narrow pixel cleanup runs", min_value=0, max_value=10, value=3)
        random_seed = st.number_input("Random seed", min_value=0, value=7707)

    color_space = st.radio("Color space", ["RGB", "HSL", "Lab"], horizontal=True)
    color_space_value = {"RGB": 0, "HSL": 1, "Lab": 2}[color_space]

    col1, col2, col3 = st.columns(3)
    with col1:
        show_labels = st.checkbox("Show labels", value=True)
    with col2:
        fill_facets = st.checkbox("Fill facets", value=True)
    with col3:
        show_borders = st.checkbox("Show borders", value=True)

    size_multiplier = st.slider("SVG size multiplier", min_value=1, max_value=10, value=3)
    font_size = st.slider("Label font size", min_value=10, max_value=100, value=50)
    font_color = st.color_picker("Label font color", "#333333")

# Create settings.json file
def create_settings_file():
    settings = {
        "randomSeed": random_seed,
        "kMeansNrOfClusters": num_colors,
        "kMeansMinDeltaDifference": 1,
        "kMeansClusteringColorSpace": color_space_value,
        "kMeansColorRestrictions": [],
        "colorAliases": {
            "A1": [0, 0, 0],
            "A2": [255, 0, 0],
            "A3": [0, 255, 0],
            "A4": [0, 0, 255],
            "B1": [64, 64, 64],
            "B2": [128, 128, 128],
            "B3": [192, 192, 192]
        },
        "removeFacetsSmallerThanNrOfPoints": min_facet_size,
        "removeFacetsFromLargeToSmall": True,
        "maximumNumberOfFacets": max_facets,
        "nrOfTimesToHalveBorderSegments": border_segments,
        "narrowPixelStripCleanupRuns": cleanup_runs,
        "resizeImageIfTooLarge": True,
        "resizeImageWidth": 1024,
        "resizeImageHeight": 1024,
        "outputProfiles": [
            {
                "name": "svg",
                "svgShowLabels": show_labels,
                "svgFillFacets": fill_facets,
                "svgShowBorders": show_borders,
                "svgSizeMultiplier": size_multiplier,
                "svgFontSize": font_size,
                "svgFontColor": font_color,
                "filetype": "svg"
            },
            {
                "name": "png",
                "svgShowLabels": show_labels,
                "svgFillFacets": fill_facets,
                "svgShowBorders": show_borders,
                "svgSizeMultiplier": size_multiplier,
                "svgFontSize": font_size,
                "svgFontColor": font_color,
                "filetype": "png"
            }
        ]
    }

    settings_path = os.path.join(st.session_state.temp_dir, "settings.json")
    with open(settings_path, "w") as f:
        json.dump(settings, f, indent=4)

    return settings_path

# Function to process the image using the web interface
def process_image_web(input_path):
    # This function simulates processing by directly using the web interface
    # In a real implementation, you would need to integrate with the JavaScript code
    st.warning("This is a simulation of the processing. In a real deployment, you would need to integrate with the JavaScript code.")

    # Simulate processing steps with progress bars
    steps = ["K-means clustering", "Facet building", "Small facet pruning",
             "Border detection", "Border segmentation", "Label placement", "SVG generation"]

    progress_bar = st.progress(0)
    status_text = st.empty()

    for i, step in enumerate(steps):
        status_text.text(f"Processing: {step}")
        for j in range(10):
            time.sleep(0.1)  # Simulate processing time
            progress_bar.progress((i * 10 + j + 1) / (len(steps) * 10))

    status_text.text("Processing complete!")
    progress_bar.progress(100)

    # Return simulated results
    return {
        "svg_path": input_path,  # Just return the input image for demonstration
        "png_path": input_path,
        "palette_info": [
            {"color": [255, 0, 0], "areaPercentage": 0.25, "index": 1},
            {"color": [0, 255, 0], "areaPercentage": 0.25, "index": 2},
            {"color": [0, 0, 255], "areaPercentage": 0.25, "index": 3},
            {"color": [255, 255, 0], "areaPercentage": 0.25, "index": 4}
        ]
    }

# File uploader
uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])

# Example images
st.markdown("### Or try an example image:")
col1, col2 = st.columns(2)
with col1:
    if st.button("Small Example"):
        # Check if the example image exists
        example_path = "src-cli/testinput.png"
        if os.path.exists(example_path):
            shutil.copy(example_path, os.path.join(st.session_state.temp_dir, "example.png"))
            uploaded_file = os.path.join(st.session_state.temp_dir, "example.png")
        else:
            st.error(f"Example image not found at {example_path}")
with col2:
    if st.button("Medium Example"):
        # Check if the example image exists
        example_path = "src-cli/testinputmedium.png"
        if os.path.exists(example_path):
            shutil.copy(example_path, os.path.join(st.session_state.temp_dir, "example.png"))
            uploaded_file = os.path.join(st.session_state.temp_dir, "example.png")
        else:
            st.error(f"Example image not found at {example_path}")

if uploaded_file is not None:
    # Save the uploaded file to the temp directory
    if isinstance(uploaded_file, str):
        input_path = uploaded_file
    else:
        input_path = os.path.join(st.session_state.temp_dir, "input.png")
        with open(input_path, "wb") as f:
            f.write(uploaded_file.getvalue())

    # Display the original image
    st.subheader("Original Image")
    display_image(input_path)

    # Process button
    if st.button("Generate Paint by Numbers"):
        st.session_state.processing = True
        with st.spinner("Processing image... This may take a while depending on the image size and settings."):
            # Create settings file
            settings_path = create_settings_file()

            # Process the image using the web interface
            results = process_image_web(input_path)

            st.session_state.results = results
            st.session_state.palette_info = results["palette_info"]
            st.session_state.processing = False

            st.success("Processing complete!")
            st.experimental_rerun()

# Display results if available
if st.session_state.results is not None and not st.session_state.processing:
    st.subheader("Paint by Numbers Result")

    # Display the processed image
    display_image(st.session_state.results["svg_path"])

    # Display palette information
    st.subheader("Color Palette")

    # Create a grid of color swatches
    palette_html = "<div style='display: flex; flex-wrap: wrap;'>"
    for color_info in st.session_state.palette_info:
        color = color_info["color"]
        percentage = color_info["areaPercentage"] * 100
        index = color_info["index"]

        hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"

        palette_html += f"""
        <div style='margin: 10px; text-align: center;'>
            <div style='width: 50px; height: 50px; background-color: {hex_color}; margin: 0 auto;'></div>
            <div>Color {index}</div>
            <div>{hex_color}</div>
            <div>{percentage:.1f}%</div>
        </div>
        """

    palette_html += "</div>"
    st.components.v1.html(palette_html, height=200)

    # Download buttons
    col1, col2 = st.columns(2)
    with col1:
        with open(st.session_state.results["svg_path"], "rb") as file:
            btn = st.download_button(
                label="Download SVG",
                data=file,
                file_name="paintbynumbers.svg",
                mime="image/svg+xml"
            )

    with col2:
        with open(st.session_state.results["png_path"], "rb") as file:
            btn = st.download_button(
                label="Download PNG",
                data=file,
                file_name="paintbynumbers.png",
                mime="image/png"
            )
