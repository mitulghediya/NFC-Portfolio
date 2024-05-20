from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
# from flask_ngrok import run_with_ngrok
import requests
from sqlalchemy.exc import IntegrityError

import secrets
secret_key = secrets.token_hex(16)  # 16 bytes = 32 hex characters


# Initialize Flask app
app = Flask(__name__, static_folder='static')
# run_with_ngrok(app)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/your database name'

app.config['SECRET_KEY'] = 'add your key here'

db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100))
    bio = db.Column(db.String(240))
    photo = db.Column(db.String(100))
    profilephoto = db.Column(db.String(100))
    password = db.Column(db.String(50), nullable=False)
    con_password = db.Column(db.String(50), nullable=False)
    facebook = db.relationship('Facebook', backref='user', uselist=False)
    instagram = db.relationship('Instagram', backref='user', uselist=False)
    linkedin = db.relationship('LinkedIn', backref='user', uselist=False)
    youtube = db.relationship('YouTube', backref='user', uselist=False)

class Facebook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    facebook_input = db.Column(db.String(100), nullable=False)

class Instagram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    instagram_input = db.Column(db.String(100), nullable=False)

class YouTube(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    youtube_input = db.Column(db.String(100), nullable=False)

class LinkedIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    linkedin_input = db.Column(db.String(100), nullable=False)

class Twitter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    twitter_input = db.Column(db.String(100), nullable=False)

class WhatsApp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    whatsapp_input = db.Column(db.String(100), nullable=False)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    loc_input = db.Column(db.String(100), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    msg_input = db.Column(db.String(100), nullable=False)

class Skype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    skype_input = db.Column(db.String(100), nullable=False)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        user = User(
            name=request.form['name'],
            mobile=request.form['mobile'],
            email=request.form['email'],
            address=request.form['address'],
            bio=request.form['bio'],
            password=request.form['password'],
            con_password=request.form['con_password']
        )

        # Save uploaded files
        user.photo = save_file(request.files['photo'])
        user.profilephoto = save_file(request.files['profilephoto'])
        print(f"User Photo Path: {user.photo}")

        # Validate passwords match
        if user.password != user.con_password:
            return render_template('create_user.html', error="Passwords do not match")

        db.session.add(user)
        db.session.commit()

        try:
            # The line causing the connection error
            response = requests.get('http://localhost:4040/api/tunnels')

            # Continue with the rest of your code handling the response
            # ...

        except requests.exceptions.ConnectionError as e:
            # Handle the connection error
            print(f"ConnectionError: {e}")
            # Add any additional error handling or logging as needed

        # Redirect to search_user route with the user ID
        return redirect(url_for('icon_page', user_id=user.id))

    return render_template('create_user.html')

def check_credentials(email, password):
    # Your authentication logic here
    # For example, check the credentials against a database
    return True  # Replace with your authentication logic

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle POST request for login
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate the email and password
        # Query the user based on email and password
        user = User.query.filter_by(email=email, password=password).first()

        if user:
            # If user exists, redirect to the index page with user details
            return redirect(url_for('icon_page', user_id=user.id))
        else:
            # If login fails, you might want to show an error message or redirect to the login page
            return redirect(url_for('login'))  # Adjust as needed
    else:
        # Handle GET request for showing the login form
        # You can render the login form template or redirect to another page
        return render_template('login.html')

@app.route('/search_user')
def search_user():
    # Get the user ID passed from create_user route
    user_id = request.args.get('user_id', None)

    # Fetch the user from the database using the ID
    user = User.query.get(user_id)
    instagrams = Instagram.query.filter_by(user_id=user_id).all()
    
    yotubes = YouTube.query.filter_by(user_id=user_id).all()
    
    fb = Facebook.query.filter_by(user_id=user_id).all()
    
    link = LinkedIn.query.filter_by(user_id=user_id).all()

    tk = Twitter.query.filter_by(user_id=user_id).all()

    wa = WhatsApp.query.filter_by(user_id=user_id).all()

    loc = Location.query.filter_by(user_id=user_id).all()

    msg = Message.query.filter_by(user_id=user_id).all()

    sp = Skype.query.filter_by(user_id=user_id).all()

    return render_template('search_user.html', user=user, instagrams=instagrams, yotubes=yotubes, fb=fb, link=link, tk=tk,
                           wa=wa, loc=loc, msg=msg, sp=sp)

@app.route('/index')
def index():
    user_id = request.args.get('user_id', None)
    user = User.query.get(user_id)
    print(user)  # Add this line to check if user data is available
    return render_template('index.html', user=user)

def save_file(file):
    if file:
        file_path = f"static/{file.filename}"
        file.save(file_path)
        return file_path
    return None

@app.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    user = db.session.query(User).get(user_id)

    if request.method == 'POST':
        # Update user details
        user.name = request.form['name']
        user.mobile = request.form['mobile']
        user.email = request.form['email']
        user.address = request.form['address']
        user.bio = request.form['bio']
        
        # Save uploaded files if new files are provided
        if 'photo' in request.files and request.files['photo'].filename != '':
            user.photo = save_file(request.files['photo'])
        if 'profilephoto' in request.files and request.files['profilephoto'].filename != '':
            user.profilephoto = save_file(request.files['profilephoto'])
        
        db.session.commit()

        # Redirect to search_user route with the updated user ID
        return redirect(url_for('search_user', user_id=user.id))

    return render_template('update_user.html', user=user)

@app.route('/icon_page')
def icon_page():
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    return render_template('icon.html', user=user)

@app.route('/store_data', methods=['POST'])
def store_data():
    try:
        # Get data from the request
        user_id = request.form.get('userId')
        social_input = request.form.get('socialInput')
        social_type = request.form.get('socialType')

        # Find the user based on user_id
        user = User.query.get(user_id)

        # Check if the user exists, if not, create a new user
        if not user:
            user = User(id=user_id)
            db.session.add(user)

        # Check the social type and handle accordingly
        social_entry = None

        if social_type == 'Facebook':
            social_entry = Facebook.query.filter_by(user_id=user.id).first()
        elif social_type == 'Instagram':
            social_entry = Instagram.query.filter_by(user_id=user.id).first()
        elif social_type == 'YouTube':
            social_entry = YouTube.query.filter_by(user_id=user.id).first()
        elif social_type == 'LinkedIn':
            social_entry = LinkedIn.query.filter_by(user_id=user.id).first()
        elif social_type == 'Twitter':
            social_entry = Twitter.query.filter_by(user_id=user.id).first()
        elif social_type == 'WhatsApp':
            social_entry = WhatsApp.query.filter_by(user_id=user.id).first()
        elif social_type == 'Location':
            social_entry = Location.query.filter_by(user_id=user.id).first()
        elif social_type == 'Message':
            social_entry = Message.query.filter_by(user_id=user.id).first()
        elif social_type == 'Skype':
            social_entry = Skype.query.filter_by(user_id=user.id).first()

        
        if social_entry:
            # Check if the provided input is different
            if getattr(social_entry, social_type.lower() + '_input') != social_input:
                # If different, create a new entry
                new_social_entry = create_social_entry(user.id, social_type, social_input)
                db.session.add(new_social_entry)
            else:
                # If the input is the same, update the existing entry
                setattr(social_entry, social_type.lower() + '_input', social_input)

        else:
            # Create a new entry if it doesn't exist
            new_social_entry = create_social_entry(user.id, social_type, social_input)
            db.session.add(new_social_entry)

        db.session.commit()

        # Return a success response
        return jsonify({'status': 'success', 'message': 'Data stored successfully'})

    except IntegrityError as e:
        # Handle IntegrityError separately to check for 'NULL' value violation
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'{social_type} input cannot be null'})

    except Exception as e:
        # Log the exception or handle errors appropriately
        print(f"Error: {str(e)}")
        return jsonify({'status': 'error', 'message': 'An error occurred while storing data'})

def create_social_entry(user_id, social_type, social_input):
    if social_type == 'Facebook':
        return Facebook(user_id=user_id, facebook_input=social_input)
    elif social_type == 'Instagram':
        return Instagram(user_id=user_id, instagram_input=social_input)
    elif social_type == 'YouTube':
        return YouTube(user_id=user_id, youtube_input=social_input)
    elif social_type == 'LinkedIn':
        return LinkedIn(user_id=user_id, linkedin_input=social_input)
    elif social_type == 'Twitter':
        return Twitter(user_id=user_id, twitter_input=social_input)
    elif social_type == 'WhatsApp':
        return WhatsApp(user_id=user_id, whatsapp_input=social_input)
    elif social_type == 'Location':
        return Location(user_id=user_id, loc_input=social_input)
    elif social_type == 'Message':
        return Message(user_id=user_id, msg_input=social_input)
    elif social_type == 'Skype':
        return Skype(user_id=user_id, skype_input=social_input)
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # app.debug = True
    app.run(debug=True, port=5002)