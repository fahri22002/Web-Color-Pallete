import streamlit as st
from flask import Flask, render_template, request, redirect, url_for
import cv2
import numpy as np
from sklearn.cluster import KMeans
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Pastikan folder upload ada
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

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

def clear_upload_folder():
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.isfile(file_path):
            os.unlink(file_path)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        clear_upload_folder()
        # Simpan file yang diunggah
        file = request.files['file']
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Baca gambar
        image = cv2.imread(filepath)
        
        # Dapatkan warna dominan
        colors = get_dominant_colors(image)
        
        # Konversi warna ke format yang dapat ditampilkan di HTML
        colors_hex = ['#{:02x}{:02x}{:02x}'.format(int(color[2]), int(color[1]), int(color[0])) for color in colors]
        
        # Buat jalur URL untuk gambar yang diunggah
        image_url = url_for('static', filename=f'uploads/{filename}')
        
        return render_template('index.html', colors=colors_hex, image_url=image_url)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
