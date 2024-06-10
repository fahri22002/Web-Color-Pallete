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
<body style="{'' if colors_hex else 'background-color: #777777;'} text-align: center;">
    <div class="form-inp" style="text-align: center;">
        
'''
    st.write(html_content, unsafe_allow_html=True)
    st.markdown(
        """
        <head>
            <style>
                [data-testid="stFileUploader"]{
                    background-color: #fefe;
                    border-radius: 20px;
                    text-align: center;
                    justify-items: center;
                    display: block;
                }
                [data-testid="stWidgetLabel"]{
                    text-align: center;
                    justify-items: center;
                }
                [data-testid="stMarkdownContainer"]{
                    text-align: center;
                    justify-items: center;
                    display: block;
                    
                }
            </style>
        </head>
        """,
        unsafe_allow_html=True
    )
    

def uploadFile():
    global temp_file
    # File uploader widget
    uploaded_file = st.file_uploader("Upload and Analyze Image", type=["jpg", "jpeg", "png"])
    st.markdown(
        """
        <head>
            <style>
                [data-testid="stFileUploader"] p{
                    font-family: "Source Sans Pro", sans-serif;
    font-weight: 600;
    padding: 1rem 0px;
    line-height: 1.2;
    font-size: calc(1.35rem + 1.2vw);
    display: block;
    text-align: center;
    margin-left: 40px;

                }
            </style>
        </head>
        """,
        unsafe_allow_html=True
    )
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
        # showHTML(colors_hex)
        showDominan(colors_hex)
    
    # Display the uploaded image
    # st.image(image, caption='Uploaded Image', use_column_width=True)

def showDominan(colors_hex):
    html_col = f'''
</div style="text-align: center;">
{'<h2 style="color: ' + colors_hex[1] + '; text-align: center; text-shadow: -1px -1px 0 #000,   1px -1px 0 #000,-1px  1px 0 #000, 1px  1px 0 #000;">Dominant Colors</h2>' if colors_hex else ''}
<div class="palette" style="display: flex; justify-content: center; background-color: #e9e9e9;
    width: 450px;
    margin: auto;
    height: 140px;
    padding: 30px;
    border-radius: 20px; text-align: center">
    {"".join(f'<div style="justify-items: center;"><div class="color-box" style="background-color: {color};width: 70px;height: 70px;margin: 0 5px;border: 1px solid #000;"></div><div style="color: {color};font-weight: bold;  text-shadow: -1px -1px 0 #000,   1px -1px 0 #000,-1px  1px 0 #000, 1px  1px 0 #000;">{color}</div></div>' for color in colors_hex)}
</div>
{'<h2 style="color: ' + colors_hex[1] + ';text-align: center;text-shadow: -1px -1px 0 #000,   1px -1px 0 #000,-1px  1px 0 #000, 1px  1px 0 #000;">Uploaded Image</h2>' if colors_hex else ''}
<div class="img" >'''
    st.write(html_col, unsafe_allow_html=True)
    st.image(temp_file, use_column_width=True)
    html_col = f'''
</div>
</body>
</html>
'''
    st.write(html_col, unsafe_allow_html=True)
    st.markdown(
        f"""
        <head>
            <style>
                [data-testid="stApp"]{{
                    background-color: {colors_hex[0]};
                }}
                .st-emotion-cache-1v0mbdj{{
                    background-color: {colors_hex[4]};
                    border: 10px solid {colors_hex[4]};
                }}
            </style>
        </head>
        """,
        unsafe_allow_html=True
    )
    
showHTML(False)
uploadFile()