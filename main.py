from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:beproductive@localhost:8889/blogz'
#app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3Bqwers'


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120),nullable=False)
    body = db.Column(db.String(500),nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    
    def __init__(self, title, body, owner_id):
        self.title = title
        self.body = body
        self.owner_id = owner_id


class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50),nullable=False)
    blogs = db.relationship('Post', backref='owner', lazy='joined')
    

    def __init__(self, username, password):
        self.username = username
        self.password = password
        


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog_post', 'blog', 'logout','home', 'all_users']
    if 'username' not in session:
        if request.endpoint not in allowed_routes:
            return redirect('/login')
    else:
        if request.endpoint not in allowed_routes:
            return redirect('/blog')



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']      
        user = User.query.filter_by(username=username).first()
        p_word = User.query.filter_by(password=password).first()
        
        if user:
            if user.password != password:
                error = "User password incorrect"
                return render_template('login.html', error = error)
                
        if user == "" or password == "":
            error = "Cannot be left blank"
            flash("Cannot be left blank")
            return render_template('login.html', error = error)

        if " " in password:
            error = "Please enter a valid password. Passwords must be between 3-20 characters long and cannot include spaces"
            return render_template('login.html', error = error)
        
        if user:
            if user.password == password:
                session['username'] = username
                return redirect('/newpost') 

        if " " in username:
            error = "Please enter a valid username. Usernames must be between 3-20 characters long and cannot include spaces"
            return render_template('login.html', error = error)

        if not user and username != "":
            error = "user does not exist"
            return redirect('/login', error = error)

        if not user and username == "":
            error = "user does not exist"
            return redirect('/login', error = error)
        else:
            error = "user does not exist"
            return redirect('/login', error)
    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        if len(username) > 50 or len(username)< 3:
            error = "Please enter a valid username. Usernames must be between 3-50 characters long and cannot include spaces"
            return render_template('signup.html', error = error)

        if len(password) > 50 or len(password) < 3:
            error = "Please enter a valid password. Passwords must be between 3-50 characters long and cannot include spaces"
            return render_template('signup.html', error = error)

        if " " in username:
            error = "Please enter a valid username. Usernames must be between 3-50 characters long and cannot include spaces"
            return render_template('signup.html', error = error)

        if " " in password:
            error = "Please enter a valid password. Passwords must be between 3-50 characters long and cannot include spaces"
            return render_template('signup.html', error = error)
    
        if verify != password:
            error = "Please enter a valid password. Passwords must match"
            username = request.form["username"]
            return render_template('signup.html', error = error)

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            error ="This Username has already been used, please try a different username"
            return render_template('signup.html', error = error)

    return render_template('signup.html')


@app.route('/logout')
def logout():
    if 'username' in session:
        del session['username']
    return redirect('/blog')


@app.route('/newpost', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        post_title = request.form['title']
        post_body = request.form['body']
        username= session['username'] 
        user_ident = User.query.filter_by(username=username).first()
        new_post = Post(post_title,post_body, user_ident.id)
        error = "Please fill in the body"
        error_2 = "Please fill in the body"
        if post_title == "" and post_body == "":
            error = "Please fill in the title"
            error_2 = "Please fill in the body"
            title = request.form["title"]
            body = request.form["body"]
            return (has_an_error(title, body, error, error_2))
        if post_title =="": 
            error = "Please fill in the title"
            title = request.form["title"]
            body = request.form["body"]
            return (has_an_error(title, body, error))
        if post_body == "":
            """#flash('Please fill in the body')
            error_2 = "Please fill in the body"
            return redirect("/newpost?error=" + error_2 + prt2)"""
            error_2 = "Please fill in the body"
            title = request.form["title"]
            body = request.form["body"]
            return (has_an_error(title, body, error_2))
        else:
            db.session.add(new_post)
            print(new_post)
            db.session.commit()
            posts = Post.query.filter_by(id=User.id).all()
            return render_template('blog.html', title="Blog!", posts=posts)
            

    posts = Post.query.all()
    return render_template('newpost.html', posts=posts)
   


@app.route("/login?error", methods=['POST'])
def has_an_error_login(error=""):
    return render_template('login.html', error = (error))    



@app.route("/newpost?error", methods=['POST'])
def has_an_error(title, body, error="", error_2=""):
    return render_template('newpost.html', title = title, body = (body), error = (error), error_2 = (error_2))    



@app.route('/blog', methods=['POST', 'GET'])
def blog_post():
    post_id = request.args.get("id")
    user =  request.args.get('user_id')
    username = request.args.get('username')
    #owner = User.query.filter_by(username=Post.owner.username).first()
    #owner = User.query.filter_by(username=user).first()
    if "user_id" in request.args:
        
        owner = User.query.filter_by(username=username).first()
        #owner = User.query.filter_by(post_id=post.owner.username).first()
        posts = Post.query.filter_by(owner_id=user).all()
        return render_template('individual.html', title="Blog!", posts=posts)#, owner=owner)

    if post_id == "" or post_id == None:
        posts = Post.query.all()
        user = User.query.filter_by(username=post_id).first()
        return render_template('blog.html',title="Blog!", posts=posts, user=user)

    else:
        posts = Post.query.filter_by(id=post_id).all()
        user = User.query.filter_by(username=User.username).first()
        return render_template('blog.html', title="Blog!", posts=posts)#, owner=owner)    
    

@app.route("/")
def all_users():
    users = User.query.filter_by(username=User.username).all()
    return render_template('home.html', users=users)

    


if __name__ == '__main__':
    app.run()
