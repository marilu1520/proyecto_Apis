from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from flask_restful import Api
from models import db, User
import controllers

app = Flask(__name__)

# Configuración de la aplicación
app.config['SECRET_KEY'] = 'clave_secreta_muy_segura_12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:fresa15@localhost/juegos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de SQLAlchemy
db.init_app(app)

# Configuración de Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.session_protection = 'strong'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Registrar Blueprint de Autenticación 
from auth.views import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

# Configurar e Integrar Flask-RESTful para la API
from api.routes import JuegoList, JuegoResource
api = Api(app, prefix='/api')
api.add_resource(JuegoList, '/juegos')
api.add_resource(JuegoResource, '/juegos/<int:id>')

# --- RUTAS WEB EXISTENTES ---
@app.route("/")
@app.route("/juegos")
@login_required
def juegos():
    lista_juegos = controllers.obtener_juegos()
    return render_template("juegos.html", juegos=lista_juegos)

@app.route("/agregar_juego")
@login_required
def formulario_agregar_juego():
    return render_template("agregar_juego.html")

@app.route("/guardar_juego", methods=["POST"])
@login_required
def guardar_juego():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controllers.insertar_juego(nombre, descripcion, precio)
    return redirect(url_for("juegos"))

@app.route("/eliminar_juego", methods=["POST"])
@login_required
def eliminar_juego():
    id = request.form["id"]
    controllers.eliminar_juego(id)
    return redirect(url_for("juegos"))

@app.route("/formulario_editar_juego/<int:id>")
@login_required
def editar_juego(id):
    juego = controllers.obtener_juego_por_id(id)
    return render_template("editar_juego.html", juego=juego)

@app.route("/actualizar_juego", methods=["POST"])
@login_required
def actualizar_juego():
    id = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controllers.actualizar_juego(id, nombre, descripcion, precio)
    return redirect(url_for("juegos"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=8000, debug=True)