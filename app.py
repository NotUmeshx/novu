from flask import Flask, redirect, request, session, url_for
import requests
import os

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

CLIENT_ID = "39c806aa86244e25ac516fbeea850a53"
CLIENT_SECRET = "d141f981d405418bba9cdd4b3990550d"
REDIRECT_URI = "http://localhost:5000/callback"

@app.route("/")
def index():
    return '<a href="/login">Login with Spotify</a>'

@app.route("/login")
def login():
    auth_url = (
        "https://accounts.spotify.com/authorize"
        f"?client_id={CLIENT_ID}"
        "&response_type=code"
        f"&redirect_uri={REDIRECT_URI}"
        "&scope=user-read-playback-state user-modify-playback-state"
    )
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    response = requests.post("https://accounts.spotify.com/api/token", data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    })
    session["token"] = response.json().get("access_token")
    return "Login Successful! ✅ Novu is connected to Spotify!"

if __name__ == "__main__":
    app.run(debug=True)
