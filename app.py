from flask import Flask, render_template, redirect, request, url_for, session
from dbconfig import cursor

app = Flask(__name__)

# Secret key for session encryption
app.secret_key = "random_secret_key"


@app.route('/')
def welcome():
    """
    Index page, temporarily redirects directly to login
    """
    return render_template("index.html")



@app.route("/home")
def home():
    return render_template("login.html")

@app.route("/account")
def account():
    return render_template("account.html")



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
    

    # Check if the user is logged in by verifying the presence of session data.
    if not session.get("user_id"):
        return redirect(url_for("login"))

    return render_template("homepage.html")

@app.route("/logout")
def logout():
    """
    Logout the user by clearing the session.
    """
    # Clear all data stored in session
    session.clear()
    
    # Redirect to the login page
    return redirect(url_for("login"))

@app.route("/game")
def game():
    return render_template("game.html")

if __name__ == '__main__':
    app.run()
