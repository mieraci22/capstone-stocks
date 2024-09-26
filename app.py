from flask import render_template, request, redirect, url_for, flash
import requests
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for non-interactive plotting
import matplotlib.pyplot as plt
from io import BytesIO
import base64

from __init__ import create_app, db, bcrypt, login_manager
from models import User  # Import the User model
from flask_login import login_user, login_required, logout_user, current_user

app = create_app()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

ALPHA_VANTAGE_API_KEY = 'VJI406IR1P9ZNCZA'

# Dummy stock data
stocks = [
    {'id': 1, 'name': 'Apple', 'symbol': 'AAPL'},
    {'id': 2, 'name': 'Amazon', 'symbol': 'AMZN'},
    {'id': 3, 'name': 'Tesla', 'symbol': 'TSLA'}
]

# Define the routes
@app.route('/')
def index():
    return render_template('index.html', stocks=stocks)

# Other routes (register, login, logout, stock, etc.)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Add the user to the database
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Find the user by username
        user = User.query.filter_by(username=username).first()
        
        # Check if user exists and the password matches
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Check username and password.', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Dynamic route for company pages
@app.route('/company/<int:company_id>')
def company(company_id):
    # Find the company by its ID
    company = next((stock for stock in stocks if stock['id'] == company_id), None)
    if company is None:
        return "Company not found", 404

    return render_template('company.html', company=company)

# Route to display the stock price graph
@app.route('/stock/<symbol>')
def stock(symbol):
    # Fetch stock data from Alpha Vantage
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url).json()

    if "Time Series (Daily)" not in response:
        return "Error retrieving data or stock not found"

    # Parse stock data
    stock_data = response['Time Series (Daily)']
    dates = list(stock_data.keys())[:30]  # Get the last 30 days
    closing_prices = [float(stock_data[date]['4. close']) for date in dates]

    # Reverse to get correct order
    dates.reverse()
    closing_prices.reverse()

    # Plot the data
    plt.figure(figsize=(10,5))
    plt.plot(dates, closing_prices, label='Closing Price', marker='o')
    plt.xticks(rotation=45)
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.title(f'{symbol} Stock Price (Last 30 Days)')
    plt.tight_layout()

    # Save the plot to a bytes buffer
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_url = base64.b64encode(buf.getvalue()).decode('utf-8')

    return render_template('stock.html', symbol=symbol, plot_url=plot_url)

@app.route('/news/<symbol>')
def news(symbol):
    # Example using Finnhub API for company news
    url = f'https://finnhub.io/api/v1/company-news?symbol={symbol}&from=2023-01-01&to=2023-12-31&token=your_finnhub_token'
    response = requests.get(url).json()

    return render_template('news.html', news=response)

if __name__ == '__main__':
    app.run(debug=True)