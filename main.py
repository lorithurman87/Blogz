from flask import Flask, request, redirect, render_template#, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:beproductive@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3Bqwers'


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #deleted = db.Column(db.Boolean)

    def __init__(self, title, body, owner_id):
        self.title = title
        self.body = body
        self.owner = owner
        #self.deleted = False

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    blogs = db.relationship('Post', backref='owner')

    def __init__(self, username, passowrd, blogs):
        self.username = username
        self.password = password
        self.blogs = blogs


@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        # TODO - validate user's data

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/')
        else:

            # TODO - user better response messaging

            return "<h1>Duplicate user</h1>"

    return render_template('register.html')


@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')


@app.route('/newpost', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        post_title = request.form['title']
        post_body = request.form['body']
        # TODO - ******owner_ident = request.form***********?????
        new_post = Post(post_title,post_body)
        error = "Please fill in the body"
        error_2 = "Please fill in the body"
        #body = body
        #title = title
        #prt1 = str(request.form.("error"))
        #prt2 = str(request.form.("error_2"))
        if post_title == "" and post_body == "":
            error = "Please fill in the title"
            error_2 = "Please fill in the body"
            title = request.form["title"]
            body = request.form["body"]
            return (has_an_error(title, body, error, error_2))# + error + error_2) 
            #return redirect("/newpost?error=" + error + error_2)
        if post_title =="": 
            error = "Please fill in the title"
            title = request.form["title"]
            body = request.form["body"]
            return (has_an_error(title, body, error))# + error)
            #return redirect("/newpost?error=" + error)
        if post_body == "":
            """#flash('Please fill in the body')
            error_2 = "Please fill in the body"
            return redirect("/newpost?error=" + error_2 + prt2)"""
            error_2 = "Please fill in the body"
            title = request.form["title"]
            body = request.form["body"]
            return (has_an_error(title, body, error_2))# + error)
            
        else:
            db.session.add(new_post)
            db.session.commit()
            #post_id = request.args.get("id")
            posts = Post.query.filter_by(id=new_post.id).all()
        
            return render_template('blog.html', title="Blog!", posts=posts)
            #return redirect('/blog')

    posts = Post.query.all()
    #blog_posts = Post.query.all()"""
    return render_template('newpost.html', posts=posts)
    #,title="Build a Blog!", blog_posts=blog_posts)"""
    #return redirect('/blog')

@app.route("/newpost?error", methods=['POST'])
def has_an_error(title, body, error="", error_2=""):
    return render_template('newpost.html', title = title, body = (body), error = (error), error_2 = (error_2))    



@app.route('/blog', methods=['POST', 'GET'])
def blog_post():
    """post_id = int(request.form['post-id'])"""
    post_id = request.args.get("id")
    if post_id == "" or post_id == None:
    #post.deleted = True
    #db.session.add(post)
    #db.session.commit()
    

        posts = Post.query.all()

    #blog_posts = Post.query.all()
        return render_template('blog.html',title="Blog!", 
        posts=posts)#, post.id=post.id) #, blog_posts=blog_posts)#, body=body)
    #return redirect('/blog')
    else:
        posts = Post.query.filter_by(id=post_id).all()
        #print(posts, post_id)
        return render_template('blog.html', title="Blog!", posts=posts)

if __name__ == '__main__':
    app.run()
