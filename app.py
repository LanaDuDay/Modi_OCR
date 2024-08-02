import os
import shutil
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
import fitz  # PyMuPDF
from PIL import Image
from image_preprocessing import preprocess_image #Import the preprocessing function

app = Flask(__name__)
UPLOAD_FOLDER = 'temp'
THUMBNAIL_FOLDER = 'temp/thumbnails'

# Ensure the folders exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(THUMBNAIL_FOLDER):
    os.makedirs(THUMBNAIL_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['THUMBNAIL_FOLDER'] = THUMBNAIL_FOLDER

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/store', methods=['POST'])
def store_pdf():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and file.filename.endswith('.pdf'):
        # Clear the upload folder
        clear_upload_folder()

        filename = 'uploaded.pdf'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        create_thumbnails(filepath)
        return redirect(url_for('select_pages'))
    return redirect(request.url)

@app.route('/select')
def select_pages():
    thumbnails = [f for f in os.listdir(app.config['THUMBNAIL_FOLDER']) if f.endswith('.png')]
    thumbnails.sort()
    return render_template('select.html', thumbnails=thumbnails)

@app.route('/convert', methods=['POST'])
def convert_pdf():
    selected_pages = request.form.getlist('pages')
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded.pdf')
    if os.path.exists(pdf_path):
        convert_selected_pages_to_images(pdf_path, selected_pages)
        return redirect(url_for('download_images'))
    return redirect(url_for('upload_file'))

def clear_upload_folder():
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        shutil.rmtree(app.config['UPLOAD_FOLDER'])
    os.makedirs(app.config['UPLOAD_FOLDER'])
    os.makedirs(app.config['THUMBNAIL_FOLDER'])

def create_thumbnails(pdf_path):
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        thumbnail_path = os.path.join(app.config['THUMBNAIL_FOLDER'], f'page{page_num}.png')
        img.thumbnail((200, 200))
        img.save(thumbnail_path, 'PNG')

def convert_selected_pages_to_images(pdf_path, selected_pages):
    doc = fitz.open(pdf_path)
    for page_num in selected_pages:
        page = doc.load_page(int(page_num))
        pix = page.get_pixmap()
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], f'page{page_num}.png')
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        #img = preprocess_image(img)
        img.save(img_path, 'PNG')

@app.route('/images')
def download_images():
    images = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.png') and 'page' in f]
    images.sort()
    return render_template('images.html', images=images)

@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/thumbnails/<filename>')
def get_thumbnail(filename):
    return send_from_directory(app.config['THUMBNAIL_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
