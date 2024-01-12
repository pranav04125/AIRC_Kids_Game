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

    if "new_user_added" in session:
        new_user_added = True # For display of user added please login message after signup
    else:
        new_user_added = False

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

    return render_template("login.html", incorrect_creds=incorrect_creds, new_user_added=new_user_added)


@app.route("/signup", methods=["POST", "GET"])
def signup():
    """
    SignUp page that checks if username and email already exists and adds to database if it doesn't before redirecting to login Page
    """
    print(session.items(), request.method)
    if "username_alr_exists" in session:
        username_exists = True  # For display of already used credentials message on signup page (Only if signup retry)
        session.pop("username_alr_exists", None)
    else:
        username_exists = False

    if "email_alr_exists" in session:
        email_exists = True
        session.pop("email_alr_exists", None)
    else:
        email_exists = False

    # Redirects to profile page if already logged in
    if "user_id" in session:
        return redirect(url_for("profile"))

    if request.method == "POST":
        username = request.form.get("new_username", None)
        password = request.form.get("new_password", None)
        email = request.form.get("email", None)
        print(username, password, email)
        # Checks for already used email and username before registering (Email has preference on message if both)
        cursor.execute("Select * FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            print("asdf")
            session["email_alr_exists"] = True
            return redirect("signup")

        cursor.execute("Select * FROM users WHERE username=%s", (username,))
        if cursor.fetchone():
            print("asdf")
            session["username_alr_exists"] = True
            return redirect("signup")

        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        session["new_user_added"] = True
        return redirect("login")

    return render_template("signup.html", username_exists=username_exists, email_exists=email_exists)

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
