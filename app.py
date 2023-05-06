# Greets user

# from flask import Flask, render_template, request

# app = Flask(__name__)


# @app.route("/")
# def index():
#     return render_template("index.html", name=request.args.get("name", "world"))

# if __name__ == "__main__":
#     app.run(debug=True)
# .....................................................................

# from flask import Flask, render_template, request

# app = Flask(__name__)


# @app.route("/")
# def index():
#     return render_template("index.html")
# ...........................................................

# # Switches to POST

# from flask import Flask, render_template, request

# app = Flask(__name__)


# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route("/greet", methods=["POST"])
# def greet():
#     return render_template("greet.html", name=request.form.get("name", "world"))
# ............................................................................

# # Uses a single route

# from flask import Flask, render_template, request

# app = Flask(__name__)


# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         return render_template("greet.html", name=request.form.get("name", "world"))
#     return render_template("index.html")
# .....................................................................................

from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'seyiolad@gmail.com'
app.config['MAIL_PASSWORD'] = ''

mail = Mail(app)

@app.route('/send-mail')
def send_mail():
    msg = Message('Test Email',
                  sender='seyiolad@gmail.com',
                  recipients=['seyiolad@gmail.com'])
    msg.body = "This is a test email sent from Flask using Gmail app password"
    mail.send(msg)
    return "Mail sent successfully"

if __name__ == '__main__':
    app.run(debug=True)
