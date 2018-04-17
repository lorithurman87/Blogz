from flask import Flask, request, redirect, render_template#, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:beproductive@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3Bqwer'


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    #deleted = db.Column(db.Boolean)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        #self.deleted = False


@app.route('/newpost', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        post_title = request.form['title']
        post_body = request.form['body']
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
