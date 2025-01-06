from flask import Flask, render_template, redirect, url_for, request
import email_system 

app = Flask(__name__)

@app.route('/')
def index():
    # Render index.html
    return render_template('index.html')


@app.route('/authenticate')
def authenticate():
    # Call authenticate() after rendering index.html
    auth_result = email_system.authenticate()
    if auth_result:
        email, password, server = auth_result
        # Render 'authenticated.html' and pass authentication info
        return render_template('authenticated.html', email=email, password=password, server=server)
    else:
        # If authentication fails, redirect to the index route
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
