import streamlit as st
import cv2
import numpy as np
from sklearn.cluster import KMeans
import os

def get_dominant_colors(image, k=5):
    # Resize gambar untuk mempercepat proses clustering
    image = cv2.resize(image, (100, 100))
    # Reshape gambar menjadi array dua dimensi
    image = image.reshape((image.shape[0] * image.shape[1], 3))
    
    # Gunakan KMeans untuk menemukan warna dominan
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(image)
    
    # Dapatkan warna dominan
    colors = kmeans.cluster_centers_
    return colors

def clear_upload_folder(upload_folder):
    for filename in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, filename)
        if os.path.isfile(file_path):
            os.unlink(file_path)

st.title("Image Processing with Streamlit")

upload_folder = 'static/uploads/'

# Pastikan folder upload ada
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

# File uploader widget
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Save uploaded file to the upload folder
    file_path = os.path.join(upload_folder, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Baca gambar
    image = cv2.imread(file_path)
    
    # Dapatkan warna dominan
    colors = get_dominant_colors(image)
    
    # Konversi warna ke format yang dapat ditampilkan di HTML
    colors_hex = ['#{:02x}{:02x}{:02x}'.format(int(color[2]), int(color[1]), int(color[0])) for color in colors]
    
    # Tampilkan gambar yang diunggah
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    # Tampilkan warna dominan
    st.write("Dominant Colors:")
    for color in colors_hex:
        st.write(color)
        st.markdown(f"<div style='width: 50px; height: 50px; background-color: {color};'></div>", unsafe_allow_html=True)

# Clear the upload folder (optional, depends on your use case)
# clear_upload_folder(upload_folder)
