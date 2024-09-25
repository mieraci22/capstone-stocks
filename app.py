from flask import Flask, render_template, request
import requests
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for non-interactive plotting
import matplotlib.pyplot as plt
from io import BytesIO
import base64


app = Flask(__name__)

ALPHA_VANTAGE_API_KEY = 'VJI406IR1P9ZNCZA'

# Dummy stock data (ensure symbols are correctly matched with API)
stocks = [
    {'id': 1, 'name': 'Apple', 'symbol': 'AAPL'},
    {'id': 2, 'name': 'Amazon', 'symbol': 'AMZN'},
    {'id': 3, 'name': 'Tesla', 'symbol': 'TSLA'}
]

@app.route('/')
def index():
    return render_template('index.html', stocks=stocks)

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle form submission
        username = request.form['username']
        password = request.form['password']
        # Add authentication logic
        return redirect('/')
    return render_template('login.html')

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