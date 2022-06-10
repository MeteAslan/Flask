
from flask import Flask,render_template,request,redirect, url_for, flash
from form import AddProduct, RegisterForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from flask_login import UserMixin
from flask_login import login_user, current_user, logout_user, login_required
from flask_login import LoginManager

from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = "mysecret_key" 
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://sql11498889:LB59UbCtrN@sql11.freemysqlhosting.net:3306/sql11498889" 

bcrypt = Bcrypt(app)

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(id):
    return user_db.query.get(int(id))

class store_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_db = db.Column(db.String(200))
    email_db = db.Column(db.String(200))
    price_db = db.Column(db.Float)
    category_db = db.Column(db.String(200))
    picture_link_db = db.Column(db.String(200))
    
    record_time_db = db.Column(db.DateTime, default=datetime.utcnow)
      
    def __repr__(self):
        return '<Name %r>' % self.id

class user_db(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key = True)
  username_db = db.Column(db.String(200), nullable=False, unique=True)
  email_db = db.Column(db.String(100), nullable=False)
  password_db = db.Column(db.String(100), nullable=False)

  def __repr__(self):
        return '<Name %r>' % self.id


@app.route("/")
@app.route("/index")
def index():
  return render_template("index.html")

@app.route("/phones")
def phones():
  phones_record = store_db.query.filter_by(category_db='phones').all()
  
  return render_template("phones.html",phones=phones_record)

@app.route("/computers")
def computers():
  computers_record = store_db.query.filter_by(category_db='computers').all()
  return render_template("computers.html",computers=computers_record)

@app.route("/cameras")
def cameras():
  cameras_record = store_db.query.filter_by(category_db='cameras').all()
  return render_template("cameras.html",cameras=cameras_record)    

# Ürün Kayıt Olma
@app.route("/addProduct", methods = ["GET","POST"])
def add_product():
  form = AddProduct()

  if request.method == "POST":
    if form.validate_on_submit():
      new_record = store_db(
        name_db = form.name.data,
        email_db = form.email.data,
        price_db = form.price.data,
        category_db = form.category.data, 
        picture_link_db = form.picture_link.data)
      
      try:
        db.session.add(new_record)
        db.session.commit()
        flash("Product is successfully added.")
      except:
        flash("Hata")    
      
      return redirect(url_for(form.category.data))
  
  return render_template("addproduct.html", form=form)

@app.route('/delete_item/<int:id>/<category>')
def delete_item(id,category):
    try:
      item_to_delete = store_db.query.filter_by(id=id).first()
      db.session.delete(item_to_delete)
      db.session.commit() 
      flash("Product is successfully deleted.")
    except:
      flash("Hata")      
      
    return redirect(url_for(category))
          
@app.route('/update_item/<int:id>/<string:category>', methods=["GET", "POST"]) 
def update_item(id,category): 

    item_to_update = store_db.query.filter_by(id=id).first()
    form = AddProduct()
    
    if request.method == "POST":
        
        item_to_update.name_db = form.name.data   
        item_to_update.email_db = form.email.data
        item_to_update.price_db = form.price.data
        item_to_update.category_db = form.category.data
        item_to_update.picture_link_db = form.picture_link.data
        try:
            db.session.commit()
            flash("The product information has been successfully updated.")
            return redirect(url_for(category)) 
        except:
            flash("Hata")
            
        
       

    if request.method == "GET":
        print("Get girdi")
        form.name.data = store_db.name_db
        form.email.data = store_db.email_db
        form.price.data = store_db.price_db
        form.category.data = store_db.category_db
        form.picture_link.data = store_db.picture_link_db
        

        return render_template("update.html", item = item_to_update, form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
  form = LoginForm()

  if form.validate_on_submit():
      user = user_db.query.filter_by(username_db=form.username.data).first()
      if user:
        password_check = bcrypt.check_password_hash(user.password_db, form.password.data)
        if password_check:
          login_user(user)
          flash("Congratulations! You Logged in")
          return redirect(url_for('index'))
  return render_template("login.html", form=form)


@app.route("/logout", methods=['GET','POST']) 
@login_required
def logout():
  logout_user()
  flash("Congratulations! You Logged Out")
  return redirect(url_for('login'))


@app.route("/register", methods=['GET', 'POST'])
def register():
  form = RegisterForm()

  if request.method == 'POST':
    print("POST İŞLEMİ")
    if form.validate_on_submit():
      hashed_password = bcrypt.generate_password_hash(form.password.data)
      new_user = user_db(
        username_db = form.username.data,
        email_db = form.email.data,
        password_db = hashed_password
      )
      try:
        db.session.add(new_user)
        db.session.commit()
        flash("Congratulations! You Signed Up")
        return redirect(url_for('login'))
      except:
        flash("Hata")      


  return render_template("register.html", form=form)
        
if __name__ == "__main__":
    app.run(debug=True)
