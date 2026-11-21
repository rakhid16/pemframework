from random import randint
from pymongo import MongoClient
from flask import Flask, request, render_template, url_for, redirect, session

# Konfigurasi aplikasi dan sesi
app = Flask(__name__)
app.secret_key = "terserah"

# Koneksi ke database cloud
client = MongoClient("mongodb+srv://RAHASIA:RAHASIA@forusers-3aig6.mongodb.net/test?retryWrites=true&w=majority")
db = client.test
collection = db.kantin

@app.route('/', methods=["POST", "GET"])  # Halaman login
def index():
  if request.method == "POST":
    if request.form['nama'] == "admin" and request.form['pwd'] == "admin":
      session['masuk'] = True
      return redirect(url_for('dashboard', npm = 17081010068, nama = "Radical Rakhman Wahid"))
    else:
      return render_template('landing_page.html', pesan="Nama pengguna atau kata sandi salah")

  return render_template("landing_page.html")

@app.route('/dashboard/<npm>/<nama>')  # Halaman dashboard
def dashboard(npm, nama):
  if 'masuk' in session:
    cursor = collection.find()
    data = []
  
    for i, item in enumerate(cursor):
      data.append(list(item.values()))
      data[i].append(i+1)
  
    return render_template('main_page.html', data = data)
  else:
    return "<h1>Login dulu</h1>"

@app.route('/tambah-data/<npm>/<nama>', methods=['GET', 'POST'])  # Tambah data
def tambah_data(npm, nama):
  if 'masuk' in session:
    if request.method == "POST":
      collection.insert_one(
        { "_id": randint(100, 1001),
          "nama_warung" : request.form['nama_warung'],
          "menu" : request.form['menu'],
          "harga" : request.form['harga']
        }
      )
      return redirect(url_for('dashboard', npm=17081010068, nama = 'Radical Rakhman Wahid'))

    return render_template('create.html')
  else:
    return "<h1>Login dulu</h1>"

@app.route('/hapus-data/<npm>/<nama>/<id>')  # Hapus data
def hapus_data(id, npm, nama):
  if 'masuk' in session:
    collection.delete_one(
      { "_id": int(id) }
    )
    return redirect(url_for('dashboard', npm=17081010068, nama = 'Radical Rakhman Wahid'))
  else:
    return "<h1>Login dulu</h1>"

@app.route('/keluar')  # Keluar
def keluar():
  if 'masuk' in session:
    session.pop('masuk')
    return redirect('/')
  else:
    return redirect('/')

@app.route('/edit-data/<npm>/<nama>/<id>', methods=['GET', 'POST'])  # Perbarui data
def edit_data(npm, nama, id):
  if 'masuk' in session:
    data = collection.find_one( {"_id" : int(id)} )

    if request.method == "POST":
      collection.update_one(
        { "_id": int(id) },
        { "$set": {
          "nama_warung": request.form['nama_warung'],
          "menu" : request.form['menu'],
          "harga" : request.form['harga']
          }
        }
      )
      return redirect(url_for('dashboard', npm = 17081010068, nama = 'Radical Rakhman Wahid'))

    return render_template('update.html', data=data)
  else:
    return "<h1>Login dulu</h1>"

#app.run(debug=True)