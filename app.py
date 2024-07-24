from flask import Flask, render_template, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de la base de datos
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario = db.Column(db.String(80), nullable=False)
    titulo = db.Column(db.String(120), nullable=False)
    texto = db.Column(db.Text, nullable=False)

# Inicialización de la base de datos
with app.app_context():
    db.create_all()
    print("Base de datos generada")

# Endpoints del frontend
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/')
def index():
    return render_template('blog.html')

# Endpoints del backend
@app.route('/posteos/<usuario>', methods=['GET', 'POST', 'DELETE'])
def post(usuario):
    if request.method == 'GET':
        posts = Post.query.filter_by(usuario=usuario).order_by(Post.id.desc()).limit(3).all()
        datos = [{"titulo": post.titulo, "texto": post.texto} for post in posts]
        return jsonify(datos)
    elif request.method == 'POST':
        titulo = request.form.get('titulo')
        texto = request.form.get('texto')
        nuevo_post = Post(usuario=usuario, titulo=titulo, texto=texto)
        db.session.add(nuevo_post)
        db.session.commit()
        return Response(status=201)
    elif request.method == 'DELETE':
        Post.query.filter_by(usuario=usuario).delete()
        db.session.commit()
        return Response(status=204)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
