# Importar
from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
# Importando la biblioteca de bases de datos
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Conectando SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Creación de una base de datos
db = SQLAlchemy(app )

#Asignación #1. Crear una tabla de base de datos

class Card(db.Model):
    # Creación de los campos
    # id
    id = db.Column(db.Integer, primary_key=True)
    # Título
    title = db.Column(db.String(100), nullable=False)
    # Descripción
    subtitle = db.Column(db.String(300), nullable=False)
    # Texto
    text = db.Column(db.Text, nullable=False)

    # Salida del objeto y su id
    def _repr_(self):
        return f'<Card {self.id}>'



# Ejecutar la página con contenido
@app.route('/')
def index():
    # Visualización de los objetos de la DB
    # Asignación #2. Mostrar los objetos de la DB en index.html
    cards = Card.query.order_by(Card.id).all()

    return render_template('index.html',
                           #tarjetas = tarjetas
                           cards=cards
                           )

# Ejecutar la página con la tarjeta
@app.route('/card/<int:id>')
def card(id):
    # Asignación #2. Mostrar la tarjeta correcta por su id
    card = Card.query.get(id)

    return render_template('card.html', card=card)

# Ejecutar la página y crear la tarjeta
@app.route('/create')
def create():
    return render_template('create_card.html')

# El formulario de la tarjeta
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']

        # Asignación #2. Crear una forma de almacenar datos en la DB
        card = Card(title=title, subtitle=subtitle, text=text)

        db.session.add(card)
        db.session.commit()

        return redirect('/')
    else:
        return render_template('create_card.html')
    
# Ruta para eliminar una carta
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    # Buscar la carta por su ID
    card = Card.query.get_or_404(id)
    
    # Eliminar la carta de la base de datos
    db.session.delete(card)
    db.session.commit()
    
    # Redirigir al usuario a la página principal
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)