from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    # Dummy stock data (replace this with actual data later)
    stocks = [
        {'name': 'Apple', 'value': 150},
        {'name': 'Amazon', 'value': 3200},
        {'name': 'Tesla', 'value': 720}
    ]
    return render_template('index.html', stocks=stocks)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data and handle authentication
        username = request.form['username']
        password = request.form['password']
        
        # Basic example authentication logic (replace with actual logic)
        if username == 'admin' and password == 'password':  # Replace with real authentication
            return redirect('/')
        else:
            # Add a message to inform the user of invalid credentials
            error = "Invalid username or password"
            return render_template('login.html', error=error)
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)