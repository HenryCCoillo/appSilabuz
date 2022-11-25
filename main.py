from flask import render_template, flash, redirect, url_for, request,Blueprint
from flask_login import (
    LoginManager,
    logout_user,
    login_required,
    current_user,
    login_user,
)


from werkzeug.urls import url_parse
from app import create_app
from app.forms import LoginForm, EditProfileForm, PostForm
from app.db import db

from app.models.usuarios import AnonymousUser, User
from app.models.posts import Post
from app.utils.utils import Permission
from app.utils.decorator import admin_required,permission_required, permission_required_rest 
from flask import g, jsonify

# from app.routes.index import ruta_index
from app.routes.index import index_p


app = create_app()

login = LoginManager(app)
login.login_view = "login"
login.anonymous_user = AnonymousUser

@index_p.route("/")
@login_required
def index():
    posts = Post.query.all()
    return render_template("indexCss.html", posts=posts)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template("index.html", form=form, posts=posts, WRITE=Permission.WRITE)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("no_existe"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        print(type(next_page))

        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index.index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)



@app.route("/no-existe")
def no_existe():
    return render_template("nouser.html")


@app.route("/admin")
@login_required
@admin_required
def for_admins_only():
    return "Para administradores!"


@app.route("/moderate")
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    return "Para moderadores!"


@app.route("/insert")
def insert():
    u = User(username="henry", email="henry@mail1.com")
    u.set_password("1234")
    db.session.add(u)
    db.session.commit()
    return "Insertado"


@app.route('/usuario/<username>')
@login_required
def user(username):

    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm() #
    if form.validate_on_submit(): #validar si el usuario no dejo campos vacios
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data

        db.session.add(current_user._get_current_object())
        db.session.commit()

        flash('Tu perfil se actualizó correctamente.')
        return redirect(url_for('.user', username=current_user.username))

    #Mostrarle el formulario armado
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    
    return render_template('edit_profile.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@app.route('/postJson/', methods=['POST'])
@auth.login_required
@permission_required_rest(Permission.WRITE)
def new_post():
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, {'Location': url_for('post_detail', id=post.id)}

@app.route('/post_detail')
def post_detail():
    return "post_detail"

@auth.verify_password
def verify_password(email, password):
    if email == '':
        return False
    user = User.query.filter_by(email = email).first()
    if not user:
        return False
    print(user.email)
    g.current_user = user
    print(g.current_user)
    return user.check_password(password)


db.init_app(app)
with app.app_context():
    db.create_all()

import unittest
from pybase64 import b64decode
from app.models.roles import Role
import json
class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client(use_cookies=True)

    def get_api_headers(self, username, password):
        return {
            'Authorization':
            'Basic ' + b64decode(
            (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def test_post(self):
        r = Role.query.filter_by(name='User').first()
        self.assertIsNotNone(r)
        u = User(username = "marc", email='marc@example.com', role=r)
        u.set_password("password")
        self.assertIsNotNone(u)
        db.session.add(u)
        db.session.commit()
        response = self.client.post(
            '/postJson/',
            headers=self.get_api_headers('henry@mail1.com', '1234'),
            data=json.dumps({'body': 'body of the *blog* post'}))

        self.assertEqual(response.status_code, 201)

if __name__ == "__main__":
    app.run()
