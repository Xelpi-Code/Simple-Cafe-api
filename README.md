# Cafe API

A simple RESTful API built with Flask and SQLAlchemy to manage a database of cafes, allowing users to view, add, update, and delete cafes.

## Features

- GET /random - Get a random cafe from the database.
- GET /all - Get a list of all cafes.
- GET /search?loc=<location> - Get cafes based on location.
- POST /add - Add a new cafe.
- PATCH /update-price/<cafe_id>?new_price=<price> - Update the coffee price of a specific cafe.
- DELETE /delete/<cafe_id> - Delete a cafe (requires API key).

## Installation

1. Clone the repository:
   git clone https://github.com/yourusername/cafe-api.git
   cd cafe-api

2. Create a virtual environment and activate it:
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Run the application:
   python app.py

## API Endpoints

### Get a Random Cafe
GET /random

Returns a random cafe from the database.

### Get All Cafes
GET /all

Returns a list of all cafes.

### Search Cafes by Location
GET /search?loc=<location>

Returns cafes that match the specified location.

### Add a New Cafe
POST /add

Form Data Required:
- name
- map_url
- img_url
- location
- seats
- has_sockets (1 or 0)
- has_toilet (1 or 0)
- has_wifi (1 or 0)
- can_take_calls (1 or 0)
- coffee_price (optional)

### Update Cafe Coffee Price
PATCH /update-price/<cafe_id>?new_price=<price>

Updates the price of coffee for a specific cafe.

### Delete a Cafe
DELETE /delete/<cafe_id>

Headers Required:
- x-api-key: TopSecretKey

Deletes a cafe from the database if the correct API key is provided.

## Technologies Used

- Flask
- Flask-SQLAlchemy
- SQLite
- Python 3

## License

This project is licensed under the MIT License.
