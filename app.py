from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os

# Inisialisasi Flask
app = Flask(__name__)

# Konfigurasi Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Konfigurasi Folder Upload
app.config['UPLOAD_FOLDER'] = 'uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Konfigurasi Email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'sandipranata1802@gmail.com' 
app.config['MAIL_PASSWORD'] = 'jbxi cjuh skdk augz' 

# Inisialisasi Database dan Mail c
db = SQLAlchemy(app)
mail = Mail(app)

# Model Database
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    proof_path = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Endpoint Form dan Penyimpanan
@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit-payment', methods=['GET', 'POST'])
def submit_payment():
    if request.method == 'POST':
        # Ambil data dari form
        name = request.form['name']
        address = request.form['address']
        payment_proof = request.files['paymentProof']
        
        # Simpan file bukti pembayaran
        proof_filename = payment_proof.filename
        proof_path = os.path.join(app.config['UPLOAD_FOLDER'], proof_filename)
        payment_proof.save(proof_path)
        
        # Simpan data ke database
        new_payment = Payment(name=name, address=address, proof_path=proof_path)
        db.session.add(new_payment)
        db.session.commit()
        
        # Kirim Email ke Penjual dengan lampiran bukti pembayaran
        msg = Message(
            'Bukti Pembayaran Baru',
            sender=app.config['MAIL_USERNAME'],
            recipients=['sandipranata1802@gmail.com']  # Email Anda
        )
        msg.body = f"""
        Pembayaran baru telah diterima:
        
        Nama: {name}
        Alamat: {address}
        Bukti Pembayaran: {proof_filename}
        
        Cek folder uploads/ untuk bukti pembayaran.
        """
        
        # Menambahkan file bukti pembayaran sebagai lampiran
        with app.open_resource(proof_path) as fp:
            msg.attach(proof_filename, 'image/jpeg', fp.read())  # Menyesuaikan jenis MIME dengan file yang diunggah
        
        mail.send(msg)
        
        return f"Pembayaran berhasil disimpan dan email telah dikirim ke sandipranata1802@gmail.com dengan lampiran bukti pembayaran!"
    
    return render_template('form.html')

# Jalankan aplikasi
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Membuat tabel database jika belum ada
    app.run(debug=True)
