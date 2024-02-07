from flask import Flask, render_template, request, redirect, url_for, send_file
from pymongo import MongoClient
from bson import ObjectId
import io

app = Flask(__name__)
client = MongoClient('mongodb+srv://hacrjit1:Hacrjit1@cluster0.b5gcbwu.mongodb.net/?retryWrites=true&w=majority')
db = client['file_sharing_app']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/files')
def file_list():
    files = db.fs.files.find()
    return render_template('file_list.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file_id = db.fs.files.insert_one({
        'filename': file.filename,
        'data': file.read()
    }).inserted_id
    return redirect('/files')

@app.route('/download/<file_id>')
def download_file(file_id):
    file_data = db.fs.files.find_one({'_id': ObjectId(file_id)})
    if file_data:
        return send_file(
            io.BytesIO(file_data['data']),
            mimetype='application/octet-stream',
            attachment_filename=file_data['filename'],
            as_attachment=True
        )
    else:
        return "File not found", 404

@app.route('/delete/<file_id>')
def delete_file(file_id):
    db.fs.files.delete_one({'_id': ObjectId(file_id)})
    return redirect('/files')

if __name__ == '__main__':
    app.run(debug=True)

