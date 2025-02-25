from http.client import responses

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, func
from random import choice

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()

def make_bool(val: int) -> bool:
    """
    Takes in a numeric value and converts to boolean

    :param val: Expecting number
    :return: Boolean
    """
    return bool(int(val))

def convert_cafe_object_to_json_format(cafe):
    """
    Takes in a cafe object gotten from the Cafe table and converts its data into json format
    :param cafe:
    :return:
    """
    return {
        "id": cafe.id,
        "name": cafe.name,
        "map_url": cafe.map_url,
        "img_url": cafe.img_url,
        "location": cafe.location,

        "amenities": {
            "seats": cafe.seats,
            "has_toilet": cafe.has_toilet,
            "has_wifi": cafe.has_wifi,
            "has_sockets": cafe.has_sockets,
            "can_take_calls": cafe.can_take_calls,
            "coffee_price": cafe.coffee_price,
        }
    }

def convert_cafe_list_to_json_format(cafes):
    """
    Takes in a list gotten from the Cafe table and converts it into json format for the jsonify() function
    eg: cafes = db.session.execute(db.select(Cafe)).scalars().all()
        return jsonify(convert_cafe_list_to_json_format(cafes))
    :param cafes:
    :return:
    """
    json = []
    for cafe in cafes:
        json.append(convert_cafe_object_to_json_format(cafe))
    return json

@app.route("/")
def home():
    return render_template("index.html")

# HTTP GET - Read Record
@app.route("/random")
def random():
    cafes = db.session.execute(db.select(Cafe)).scalars().all()
    random_cafe = choice(cafes)
    return jsonify(convert_cafe_object_to_json_format(random_cafe))

@app.route("/all")
def all_cafes():
    cafes = db.session.execute(db.select(Cafe)).scalars().all()
    return jsonify(convert_cafe_list_to_json_format(cafes))


@app.route("/search")
def search_cafe():
    location = request.args.get("loc")
    cafes = db.session.execute(db.select(Cafe).where(Cafe.location==location)).scalars()
    return jsonify(convert_cafe_list_to_json_format(cafes))


# HTTP POST - Create Record

@app.route("/add", methods=["POST"])
def add_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        has_sockets=make_bool(request.form.get("has_sockets")),
        has_toilet=make_bool(request.form.get("has_toilet")),
        has_wifi=make_bool(request.form.get("has_wifi")),
        can_take_calls=make_bool(request.form.get("can_take_calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


# HTTP PUT/PATCH - Update Record

@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    new_price = request.args.get("new_price")
    cafe = Cafe.query.get_or_404(cafe_id)

    if new_price:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully changed listed price"})

    return jsonify(response={"error": "Missing new_price"}), 400

# HTTP DELETE - Delete Record

@app.route("/delete/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.headers.get("x-api-key")
    if api_key != "TopSecretKey":
        return jsonify(response={"error": "Invalid api-key"}), 404

    cafe_to_delete =db.session.get(Cafe, cafe_id)
    if cafe_to_delete is None:
        return jsonify(response={"error": "Cafe not found"}), 404

    db.session.delete(cafe_to_delete)
    db.session.commit()
    return jsonify(response={"success": "Successfully deleted cafe"})



if __name__ == '__main__':
    app.run(debug=True)
