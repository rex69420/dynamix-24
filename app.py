import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo

from flask_session import Session

app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = os.urandom(24)
app.config["MONGO_URI"] = (
    "mongodb+srv://rex:5oS0U6qcACS873YZ@cluster0.p7aklfk.mongodb.net/vitalyx"
)
app.config["SESSION_TYPE"] = "filesystem"
app.config["TEMPLATES_AUTO_RELOAD"] = True
Session(app)
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

if app.config["MONGO_URI"] == "mongodb://...":
    raise ValueError("Please set the MONGO_URI in app.py to your MongoDB URI")


@app.route("/")
def index():
    if "username" in session:
        authenticated = True
    else:
        authenticated = False
    return render_template("index.html", auth=authenticated)


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")


@app.route("/patient/shop")
def shop():
    return render_template("patient_shop.html")


@app.route("/patient/dashboard")
def patient_dashboard():
    if "username" not in session:
        return redirect("/patient/login")

    return render_template("patient_dashboard.html", username=session["username"])


@app.route("/patient/activity")
def patient_activity():
    if "username" not in session:
        return redirect("/patient/login")

    return render_template("patient_activity.html", username=session["username"])


@app.route("/patient/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = mongo.db.users.find_one({"email": email})
        username = user.get("username") if user else None
        role = user.get("role") if user else None
        if (
            user
            and bcrypt.check_password_hash(user["password"], password)
            and role == "patient"
        ):
            session["username"] = username
            flash("Login successful", "success")
            return redirect("/patient/dashboard")
        else:
            flash("Login failed. Check your credentials.", "danger")

    if "username" in session:
        return redirect("/patient/dashboard")
    return render_template("patient_login.html")


@app.route("/patient/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("reg_username")
        password = request.form.get("reg_password")
        email = request.form.get("reg_email")
        existing_user = mongo.db.users.find_one({"username": username})
        if existing_user:
            flash(
                "Username already exists. Please choose a different username.", "danger"
            )
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
            mongo.db.users.insert_one(
                {
                    "username": username,
                    "password": hashed_password,
                    "email": email,
                    "role": "patient",
                }
            )
            flash("Registration successful. You can now log in.", "success")
            return redirect("/patient/login")
    return render_template("patient_register.html")


# ALL OF THIS BELOW IS COMMENTED OUT FOR NOW, IT WILL BE CHANGED IN THE LIVE DEMO.


@app.route("/doctor/dashboard")
def doctor_dashboard():
    if "username" not in session:
        return redirect("/doctor/login")

    role = mongo.db.users.find_one({"username": session["username"]}).get("role")
    if role != "doctor":
        return redirect("/doctor/login")

    username = session["username"].replace("Dr.", "").replace("!", "").strip()
    path = f"/static/img/{username}.png"
    # return render_template("doctor_dashboard.html", username="Dr. Whiter")
    return render_template(
        "doctor_dashboard.html",
        username=f"{session['username']}",
        pfp=f"{path.lower()}",
    )


@app.route("/doctor/patientinfo")
def doctor_patientinfo():
    if "username" not in session:
        return redirect("/doctor/login")

    return render_template("doctor_patientinfo.html")


@app.route("/doctor/login")
def doctor_login():
    if "username" in session:
        role = mongo.db.users.find_one({"username": session["username"]}).get("role")
        if role == "doctor":
            return redirect("/doctor/dashboard")
        else:
            return redirect("/logout")

    return render_template("doctor_login.html")
    # return redirect("/doctor/dashboard")


# @app.route("/doctor/prescription")
# def doctor_prescription():
#     # if "username" not in session:
#     # return redirect("/doctor/login")

#     return render_template("doctor_prescription.html")


@app.route("/doctor/schedule")
def doctor_schedule():
    if "username" not in session:
        return redirect("/doctor/login")

    return render_template("doctor_schedule.html")


@app.route("/doctor/technicians")
def doctor_technicians():
    if "username" not in session:
        return redirect("/doctor/login")

    return render_template("doctor_technicians.html")


@app.route("/doctor/api/login", methods=["POST"])
def doctor_login_api():
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        user = mongo.db.users.find_one({"username": username})
        if not user:
            return (
                jsonify({"status": "failed", "message": "Username does not exist."}),
                404,
            )

        if not bcrypt.check_password_hash(user["password"], password):
            return jsonify({"status": "failed", "message": "Incorrect password."}), 401

        if user.get("role") != "doctor":
            return (
                jsonify(
                    {
                        "status": "failed",
                        "message": "Access denied. Doctor role required.",
                    }
                ),
                403,
            )

        session["username"] = username
        return jsonify({"status": "success", "message": "Login successful."}), 200


@app.route("/wip")
def wip():
    return render_template("wip.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("wip.html"), 404


@app.route("/panic")
def panic():
    # if route is called, check if user is logged in. if not, set session["username"] to "Dr. JDX7871!" and redirect to doctor dashboard
    if "username" not in session:
        session["username"] = "Dr. JDX7871!"
        return redirect("/doctor/dashboard")


if __name__ == "__main__":
    app.run(debug=True)
