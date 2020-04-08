from random import randint
from pymongo import MongoClient
from flask import Flask, request, render_template, url_for, redirect, session

# UNTUK ROUTING & SESSION
app = Flask(__name__)
app.secret_key = "terserah"

# UNTUK AKSES CLOUD DATABASE
client = MongoClient("mongodb+srv://"RAHASIA":"RAHASIA"@forusers-3aig6.mongodb.net/test?retryWrites=true&w=majority")
db = client.test        # AMBIL DATABASE test
collection = db.kantin  # AMBIL COLLECTION kantin

@app.route('/', methods=["POST", "GET"])   # LAMAN LOGIN
def index():
  if request.method == "POST":
    if request.form['nama'] == "admin" and request.form['pwd'] == "admin":
      session['masuk'] = True
      return redirect('dashboard')
    else:
      return render_template('landing_page.html', pesan = "Nama pengguna atau sandi lewat salah")

  return render_template("landing_page.html")

@app.route('/dashboard')   # LAMAN DASHBOARD
def dashboard():
  if 'masuk' in session:
    cursor = collection.find()
    data = []
  
    for i, item in enumerate(cursor):
      data.append(list(item.values()))
      data[i].append(i+1)
  
    return render_template('main_page.html', data = data)
  else:
    return "<h1>Login dulu</h1>"

@app.route('/tambah-data', methods=['GET','POST'])   # MENAMBAH DATA - CREATE
def tambah_data():
  if 'masuk' in session:
    if request.method == "POST":
      collection.insert_one(
        { "_id": randint(100, 1001),
          "nama_warung" : request.form['nama_warung'],
          "menu" : request.form['menu'],
          "harga" : request.form['harga']
        }
      )
      return redirect(url_for('dashboard'))

    return render_template('create.html')
  else:
    return "<h1>Login dulu</h1>"

@app.route('/hapus-data/<id>')   # MENGHAPUS DATA - DELETE
def hapus_data(id):
  if 'masuk' in session:
    collection.delete_one(
      { "_id": int(id) }
    )
    return redirect(url_for('dashboard'))
  else:
    return "<h1>Login dulu</h1>"

@app.route('/keluar')   # LOG OUT
def keluar():
  if 'masuk' in session:
    session.pop('masuk')
    return redirect('/')
  else:
    return redirect('/')

@app.route('/edit-data/<id>', methods=['GET', 'POST'])   # MEMPERBARUI DATA - UPDATE
def edit_data(id):
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
      return redirect(url_for('dashboard'))

    return render_template('update.html', data=data)
  else:
    return "<h1>Login dulu</h1>"

#app.run(debug=True)