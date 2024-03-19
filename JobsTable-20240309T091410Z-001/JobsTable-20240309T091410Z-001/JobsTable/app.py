# app.py

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask import abort
from flask_login import LoginManager, login_user, logout_user, login_required,current_user

from models import db, Job, User, Application, Department
from itsdangerous import URLSafeTimedSerializer, BadSignature
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'nkosingiphilebhekithemba@gmail.com'  # Your Gmail address
app.config['MAIL_PASSWORD'] = 'mrkj vyyo lyws ubqd'  # Your Gmail password

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# Initialize Flask-Mail

mail = Mail(app)

# Initialize URLSafeTimedSerializer with a secret key
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

db.init_app(app)

with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    # Replace this with your actual user loading logic
    return User.query.get(int(user_id))


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/about')
def about_page():
    return render_template('about.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        username = request.form['email']  # Use email as username
        email = request.form['email']
        student_number = request.form['student_number']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validate form data
        if password != confirm_password:
            flash("Passwords do not match. Please try again.", 'error')
            return redirect(url_for('signup'))

        # Check if the username or email already exists in the database
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("Username or email already exists. Please choose a different one.", 'error')
            return redirect(url_for('signup'))

        # Create a new user instance and save it to the database
        new_user = User(username=username, email=email, student_number=student_number,
                        first_name=first_name, last_name=last_name)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        print("worked")
        flash("Signup successful! Please log in.", 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']
        # Find user by username in the database

        user = User.query.filter_by(username=username).first()

        if username == 'admin@gmail.com' and password == 'admin':
            session['admin_logged_in'] = True
            login_user(user)
            flash('Admin logged in Successful !', 'success')

            return redirect(url_for('Admin', username='admin@gmail.com'))

        # Check if user exists and password is correct

        if user and User.is_active and user.check_password(password):
            login_user(user)
            # Implement login logic, e.g., session management
            flash("Login successful!", 'success')
            return redirect(url_for('vacancies'))
        else:
            flash("Invalid username or password. Please try again.", 'error')
            return render_template('login.html')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    # Logout the current user
    logout_user()

    flash('Logout Successful', 'success')

    return redirect(url_for('login'))


@app.route('/Admin')
@login_required
def Admin():
    jobs = Job.query.all()
    return render_template('Admin.html', jobs=jobs)


@app.route('/vacancies')
@login_required
def vacancies():
    jobs = Job.query.all()
    return render_template('User.html', jobs=jobs)


# app.py
@app.route('/submit_application', methods=['POST'])
@login_required
def submit_application():
    student_number = request.form['student_number']
    name = request.form['name']
    surname = request.form['surname']
    id_number = request.form['id_number']
    email = request.form['email']
    course = request.form['course']
    academic_background = request.form['academic_background']
    experience = request.form['experience']
    skills = request.form['skills']

    application = Application(student_number=student_number, name=name, surname=surname,
                              id_number=id_number, email=email, course=course,
                              academic_background=academic_background, experience=experience,
                              skills=skills)
    db.session.add(application)
    db.session.commit()

    return redirect(url_for('track'))


# ... (previous code) ...

@app.route('/apply', methods=['POST', 'GET'])
@login_required
def apply():
    return render_template('Apply.html')


# ... (previous code) ...


# ... (previous code) ...

@app.route('/delete_job/<int:job_id>', methods=['POST'])
@login_required
def delete_job(job_id):
    job = Job.query.get(job_id)

    if not job:
        abort(404)  # Handle job not found

    db.session.delete(job)
    db.session.commit()

    return redirect(url_for('index'))


# ... (rest of the code) ...


# ... (rest of the code) ...


# app.py

# ... (previous code) ...

@app.route('/update_job/<int:job_id>', methods=['GET', 'POST'])
@login_required
def update_job(job_id):
    job = Job.query.get(job_id)

    if request.method == 'POST':
        job.title = request.form['title']
        job.description = request.form['description']
        job.requirements = request.form['requirements']
        job.hours = request.form['hours']

        db.session.commit()

        return redirect(url_for('index'))

    return render_template('update_job.html', job=job)


@app.route('/update_profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def update_profile():
    user = User.query.get(all)

    if request.method == 'POST':
        user.name = request.form['name']
        user.description = request.form['description']
        user.requirements = request.form['requirements']
        user.hours = request.form['hours']

        db.session.commit()

        return redirect(url_for(''))

    return render_template('update_profile.html', user=user)


# ... (rest of the code) ...


@app.route('/post_job', methods=['GET', 'POST'])
@login_required
def post_job():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        requirements = request.form['requirements']
        hours = request.form['hours']
        deadline = request.form['deadline']
        department_name = request.form['department_name']
        department_id = request.form['department_id']

        new_job = Job(title=title, description=description, requirements=requirements, hours=hours, deadline=deadline,
                      department_name=department_name, department_id=department_id)

        db.session.add(new_job)
        db.session.commit()

        return redirect(url_for('Admin'))

    depart = Department.query.all()
    return render_template('post_job.html', depart=depart)


@app.route('/add_department', methods=['POST', 'GET'])
@login_required
def add_department():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        faculty = request.form['faculty']

        # Create a new Department object
        new_department = Department(name=name, email=email, faculty=faculty)

        # Add the new department to the database
        db.session.add(new_department)
        db.session.commit()

        # Redirect to a success page or another route
        return redirect(url_for('department_details'))

        # If it's a GET request, render the HTML form
    return render_template('add_department.html')


# edit routing
@app.route('/<int:student_id>/edit/', methods=('GET', 'POST'))
def edit(student_id):
    student = Application.query.get_or_404(student_id)

    if request.method == 'POST':
        status = request.form["status"]
        student.status = status
        db.session.commit()
        return redirect(url_for('applications'))
    else:

        return render_template('edit.html', student=student)


@app.route('/applications', methods=['POST', 'GET'])
@login_required
def applications():
    application = Application.query.all()
    return render_template('applications.html', application=application)


@app.route('/profile')
@login_required
def profile():
    user = current_user  # Assuming current_user is imported correctly
    update_user_profile_url = url_for('update_user_profile')  # Get URL for update_user_profile route
    return render_template('profile.html', user=user, update_user_profile_url=update_user_profile_url)

@app.route('/update_department/<int:department_id>', methods=['GET', 'POST'])
@login_required
def update_department(department_id):
    department = Department.query.get(department_id)

    if request.method == 'POST':
        department.name = request.form['name']
        department.email = request.form['email']
        department.faculty = request.form['faculty']

        db.session.commit()

        return redirect(url_for('department_details'))

    return render_template('update_department.html', department=department)


@app.route('/delete_department/<int:department_id>', methods=['POST'])
@login_required
def delete_department(department_id):
    department = Department.query.get(department_id)

    if not department:
        abort(404)  # Handle job not found

    db.session.delete(department)
    db.session.commit()

    return redirect(url_for('department_details'))


@app.route('/department_details', methods=['POST', 'GET'])
@login_required
def department_details():
    departments = Department.query.all()
    return render_template('department_details.html', departments=departments)


@app.route('/track_application', methods=['POST', 'GET'])
@login_required
def track_application():
        user = User.query.filter_by(id=current_user.id).first()
        application = Application.query.filter_by(email=user.email).all()
        if application:
            return render_template('track_application.html',applications=application)
        else:
            print(user.email)

@app.route('/track', methods=['POST', 'GET'])
@login_required
def track():
    user = User.query.filter_by(id=current_user.id).first()
    application = Application.query.filter_by(email=user.email).all()
    if application:
        return render_template('track_application.html',applications=application)
    else:
        print(user.email)
    

@app.route('/update_user_profile', methods=['POST'])
@login_required
def update_user_profile():
    if request.method == 'POST':
        # Assuming you have a form in the HTML with input fields for the user profile data
        # Retrieve the updated profile data from the form
        username = request.form['username']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        
        # Update the user's profile in the database
        current_user.username = username
        current_user.email = email
        current_user.first_name = first_name
        current_user.last_name = last_name
        db.session.commit()
        
        # Redirect the user to the profile page after updating
        return redirect(url_for('profile'))
    
# Define the route for forgot password
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()

        if user:
            # Generate a token for password reset
            token = serializer.dumps(email, salt='password-reset')

            # Send the password reset link to the user via email
            reset_link = url_for('reset_password', token=token, _external=True)

            # Send email
            msg = Message(subject="Password Reset Request",
                          recipients=[email],
                          body=f"Hi {user.username},\n\n"
                               f"Please follow this link to reset your password: {reset_link}\n\n"
                               f"If you didn't request this, please ignore this email.",
                          sender="mlungisimnembe075@gmail.com")  # Change this to your email address
            mail.send(msg)

            flash("Password reset link has been sent to your email.", 'success')
            return redirect(url_for('login'))
        else:
            flash("Email address not found. Please try again.", 'error')
            return redirect(url_for('forgot_password'))

    return render_template('forgot_password.html')

# Define the route for resetting password
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        # Add password reset logic here
        return redirect(url_for('login'))  # Redirect to login after resetting password

    # Render a form for resetting password
    return render_template('reset_password.html')

if __name__ == '__main__':
    app.run(debug=True)
