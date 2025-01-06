from flask import Flask, render_template, redirect, url_for, request
import email_system 

app = Flask(__name__)

@app.route('/')
def index():
    # Render index.html
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
