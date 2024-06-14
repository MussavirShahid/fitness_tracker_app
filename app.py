from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from langchain_utils import generate_exercise_diet_plan

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789'

login_manager = LoginManager()
login_manager.init_app(app)

# In-memory user storage
users = {}

class User(UserMixin):
    def __init__(self, username, password, age, height_ft, weight_lbs, gym_days):
        self.id = username
        self.password = password
        self.age = age
        self.height_ft = height_ft
        self.weight_lbs = weight_lbs
        self.gym_days = gym_days

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        age = int(request.form['age'])
        height_ft = float(request.form['height_ft'])  
        weight_lbs = float(request.form['weight_lbs'])
        gym_days = int(request.form['gym_days'])  
        new_user = User(username, password, age, height_ft, weight_lbs, gym_days)
        users[username] = new_user
        flash('Signup successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user = current_user
    exercise_plan, diet_plan, detailed_plan = generate_exercise_diet_plan(
        user.age, user.height_ft, user.weight_lbs, user.gym_days
    )
    return render_template('dashboard.html', exercise_plan=exercise_plan, diet_plan=diet_plan, detailed_plan=detailed_plan)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
