import streamlit as st
import cv2
import numpy as np
from sklearn.cluster import KMeans
import os

def get_dominant_colors(image, k=5):
    # Resize image to speed up clustering
    image = cv2.resize(image, (100, 100))
    # Reshape image to a 2D array of pixels
    image = image.reshape((image.shape[0] * image.shape[1], 3))
    
    # Use KMeans to find dominant colors
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(image)
    
    # Get the dominant colors
    colors = kmeans.cluster_centers_
    return colors

def clear_upload_folder(upload_folder):
    for filename in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, filename)
        if os.path.isfile(file_path):
            os.unlink(file_path)

# Streamlit app
# st.title("Image Processing with Streamlit")

# Define the upload folder
UPLOAD_FOLDER = 'static/uploads/'
temp_file = ''
# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def showHTML(colors_hex):
    # Display the dominant colors
    html_content = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload and Analyze Image</title>
    <link rel="stylesheet" href="./static/style.css">
</head>
<body style="{'' if colors_hex else 'background-color: #777777;'}">
    <div class="form-inp">
        <h1>Upload and Analyze Image</h1>
'''
    st.write(html_content, unsafe_allow_html=True)

def uploadFile():
    global temp_file
    # File uploader widget
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Clear the upload folder
        clear_upload_folder(UPLOAD_FOLDER)

        # Save uploaded file to a temporary location
        temp_file = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(temp_file, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Read the image
        image = cv2.imread(temp_file)
        
        # Get dominant colors
        colors = get_dominant_colors(image)
        # Convert colors to hex format for HTML display
        colors_hex = ['#{:02x}{:02x}{:02x}'.format(int(color[2]), int(color[1]), int(color[0])) for color in colors]
        showHTML(colors_hex)
        showDominan(colors_hex)
    
    # Display the uploaded image
    # st.image(image, caption='Uploaded Image', use_column_width=True)

def showDominan(colors_hex):
    html_col = f'''
</div>
{'<h2 style="color: ' + colors_hex[1] + ';">Dominant Colors</h2>' if colors_hex else ''}
<div class="palette">
    {"".join(f'<div class="color-box" style="background-color: {color};"></div>' for color in colors_hex)}
</div>
{'<h2 style="color: ' + colors_hex[1] + ';">Uploaded Image</h2>' if colors_hex else ''}
<div class="img" style="background-color: {colors_hex[4]};">
    <img src="file:///{temp_file}" alt="Uploaded Image">
</body>
</html>
'''
    st.write(html_col, unsafe_allow_html=True)

showHTML(False)
uploadFile()