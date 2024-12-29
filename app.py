from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os

# Inisialisasi Flask
app = Flask(__name__)

# Konfigurasi Database (menggunakan nama baru)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payments_new.db'  # Ubah nama database
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

# Inisialisasi Database dan Mail
db = SQLAlchemy(app)
mail = Mail(app)

# Model Database
class Payment(db.Model):
    __tablename__ = 'payments'  # Menentukan nama tabel secara eksplisit
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    spice_level = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    proof_path = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit-payment', methods=['GET', 'POST'])
def submit_payment():
    if request.method == 'POST':
        # Ambil data dari form
        name = request.form['name']
        phone = request.form['phone']
        spice_level = request.form['spice_level']
        address = request.form['address']
        payment_proof = request.files['paymentProof']
        
        # Simpan file bukti pembayaran
        proof_filename = payment_proof.filename
        proof_path = os.path.join(app.config['UPLOAD_FOLDER'], proof_filename)
        payment_proof.save(proof_path)
        
        # Simpan data ke database
        new_payment = Payment(
            name=name,
            phone=phone,
            spice_level=spice_level,
            address=address,
            proof_path=proof_path
        )
        db.session.add(new_payment)
        db.session.commit()
        
        # Kirim Email ke Penjual dengan lampiran bukti pembayaran
        msg = Message(
            'Bukti Pembayaran Baru',
            sender=app.config['MAIL_USERNAME'],
            recipients=['sandipranata1802@gmail.com']
        )
        msg.body = f"""
        Pembayaran baru telah diterima:
        
        Nama : {name}
        Nomor WhatsApp : {phone}
        Level Pedas: {spice_level}
        Catatan : {address}
        Bukti Pembayaran : {proof_filename}
        
        Cek Dompet Digital/ untuk bukti pembayaran.
        """
        
        # Menambahkan file bukti pembayaran sebagai lampiran
        with app.open_resource(proof_path) as fp:
            msg.attach(proof_filename, 'image/jpeg', fp.read())
        
        mail.send(msg)
        
        return f"Pembayaran berhasil disimpan dan email telah dikirim ke sandipranata1802@gmail.com dengan lampiran bukti pembayaran!"
    
    return render_template('form.html')

# Jalankan aplikasi
if __name__ == '__main__':
    with app.app_context():
        db.drop_all()  # Hapus semua tabel yang ada
        db.create_all()  # Buat tabel baru
    app.run(debug=True)