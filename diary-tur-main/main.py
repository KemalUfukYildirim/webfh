from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite'ı bağlama
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Veri tabanı oluşturma
db = SQLAlchemy(app)

# Tablo oluşturma
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Card {self.id}>'

# Kullanıcı tablosunu oluşturma
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

# Tablo oluşturma
with app.app_context():
    db.create_all()

# Giriş sayfası
@app.route('/', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        form_login = request.form['email']
        form_password = request.form['password']

        # Kullanıcıyı veritabanından çek
        user = User.query.filter_by(email=form_login).first()

        # Kullanıcıyı ve şifreyi kontrol et
        if user and user.password == form_password:
            return redirect("/index")
        else:
            error = "E-posta veya şifre yanlış"
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

# Kayıt sayfası
@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        login = request.form['email']
        password = request.form['password']
        password1 = request.form['password1']

        # Şifrelerin eşleşip eşleşmediğini kontrol et
        if password != password1:
            error = "Şifreler eşleşmiyor"
            return render_template('registration.html', error=error)

        # Şifreler eşleşiyorsa kullanıcıyı kaydet
        user = User(email=login, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect('/')
    else:    
        return render_template('registration.html')

# Ana sayfa
@app.route('/index')
def index():
    cards = Card.query.order_by(Card.id).all()
    return render_template('index.html', cards=cards)

# Kart detay sayfası
@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)
    return render_template('card.html', card=card)

# Kart oluşturma sayfası
@app.route('/create')
def create():
    return render_template('create_card.html')

# Kart oluşturma formu
@app.route('/form_create', methods=['GET', 'POST'])
def form_create():
    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        text = request.form['text']

        # Veri tabanına gönderilecek bir nesne oluşturma
        card = Card(title=title, subtitle=subtitle, text=text)
        db.session.add(card)
        db.session.commit()
        return redirect('/index')
    else:
        return render_template('create_card.html')

if __name__ == "__main__":
    app.run(debug=True)
