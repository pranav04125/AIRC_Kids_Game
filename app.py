from flask import Flask, render_template, redirect, request, url_for, session
from dbconfig import cursor

app = Flask(__name__)

# Secret key for session encryption
app.secret_key = "random_secret_key"


@app.route('/')
def homepage():
    """
    Index page, temporarily redirects directly to login
    """
    return redirect(url_for("login"))


@app.route("/login", methods=["POST", "GET"])
def login():
    """
    Login page that redirects to profile if credentials are correct
    """
    if "incorrect_creds" in session:
        incorrect_creds = True  # For display of incorrect credentials message on login page (Only if login retry)
        session.pop("incorrect_creds", None)
    else:
        incorrect_creds = False

    # Redirects to profile page if already logged in
    if "user_id" in session:
        return redirect(url_for("profile"))

    # Logs in and redirects to profile if form is submitted
    if request.method == "POST":
        username = request.form.get("username", None)
        password = request.form.get("password", None)

        cursor.execute(f"SELECT * FROM users WHERE username=%s and password=%s", (username, password))
        user_details = cursor.fetchone()

        if user_details:
            # Set session data if credentials exist in DB
            session["username"] = username
            session["user_id"] = user_details["id"]
            session["user_email"] = user_details["email"]

            return redirect(url_for("profile"))
        else:
            session["incorrect_creds"] = True  # Added to display message on refresh
            return redirect("login")

    return render_template("login.html", incorrect_creds=incorrect_creds)


@app.route("/profile")
def profile():
    """
    Temporary user profile page for testing purposes
    """

    # Check if user is logged in and redirect to login page if not
    if "user_id" not in session:
        return redirect(url_for("login"))

    return f"<h1>Logged in as {session['username']} with email {session["user_email"]} and user id {session["user_id"]}<h1>"


if __name__ == '__main__':
    app.run()
