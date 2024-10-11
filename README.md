# Stock Price Tracker - Flask Web Application

This Flask-based web application provides real-time financial news and displays stock prices for major companies like Apple, Amazon, and Tesla. It also includes a login system for user authentication and a search bar to find additional stocks.

## Features

- **Home Page**: Displays the top 3 stocks with a button to view stock prices.
- **Search Bar**: Allows users to search for other stocks by symbol.
- **Stock Price Page**: Shows real-time stock prices fetched using Alpha Vantage API.
- **Login System**: Authenticates users to access additional functionalities.
- **Chart Visualization**: Uses Matplotlib to render stock price charts.
- **User Authentication**: Secure login using Flask-Login and Flask-Bcrypt.

## Getting Started

To get the application running locally, follow the instructions below.

### Prerequisites

You will need the following installed:

- Python 3.7+
- pip
- virtualenv

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/mieraci22/capstone-stocks.git
    cd capstone-stocks
    ```

2. Create a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file for environment variables, and set your API key for Alpha Vantage (replace `YOUR_API_KEY` with your actual key):

    ```
    ALPHA_VANTAGE_API_KEY=YOUR_API_KEY
    ```

5. Run the Flask development server:

    ```bash
    python3 app.py
    ```

6. The application should now be running at `http://127.0.0.1:5000`.

## Deployment

The app can be deployed to services like Render.com. Follow these steps to get the app up and running on a production server.

### Setup

- Ensure the environment variable `PORT` is correctly set.
- Run the application using Gunicorn for production:

    ```bash
    gunicorn app:app --bind 0.0.0.0:$PORT
    ```

## Technologies Used

- Flask
- SQLAlchemy
- Alpha Vantage API
- Matplotlib
- Flask-Bcrypt (for password hashing)
- Flask-Login (for user authentication)
- Gunicorn (for production deployment)
- HTML/CSS/Bootstrap (for frontend)

## Author

- **Michael Ieraci**  
  GitHub: [mieraci22](https://github.com/mieraci22)

Feel free to contribute by opening issues or pull requests!