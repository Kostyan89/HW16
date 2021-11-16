import json
from models import User, Order, Offer
from flask import Flask, request, jsonify
from setup_db import db
app = Flask(__name__)
app.config.from_object()
app.url_map.strict_slashes = False
JSON_AS_ASCII = False


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == "GET":
        result = []
        for u in User.query.all():
            result.append(u.to_dict())
        return jsonify(result), 200, {'Content-Type':'application/json; charset=UTF-8'}
    if request.method == "POST":
        json.loads(request.json)
        new_user = User(
            id=request.json("id"),
            first_name=request.json("first_name"),
            last_name=request.json("last_name"),
            age=request.json("age"),
            email=request.json("email"),
            role=request.json("role"),
            phone=request.json("phone")
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user, 201


@app.route("/users/<int:id>", methods=['GET', 'DELETE', 'PUT'])
def user(id):
    if not id:
        return "id not found", 401
    elif request.method == "GET":
        return jsonify(User.query.get(id).to_dict), 200, {'Content-Type':'application/json; charset=UTF-8'}
    elif request.method == 'PUT':
        new_user = json.loads(request.data)
        usr = User.query.get(id)
        usr.id = new_user["id"],
        usr.first_name = new_user["first_name"],
        usr.last_name = new_user["last_name"],
        usr.age = new_user["age"],
        usr.email = new_user["email"],
        usr.role = new_user["role"],
        usr.phone = new_user["phone"],
        db.session.add(new_user)
        db.session.commit()
        return new_user, 200
    elif request.method == 'DELETE':
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return "", 204

@app.route("/orders", methods=['GET', 'POST'])
def orders():
    if request.method == "GET":
        res =[]
        for ord in Order.query.all():
            res.append(ord.to_dict())
        return jsonify(res), 200,{'Content-Type':'application/json; charset=UTF-8'}
    elif request.method == "POST":
        json.loads(request.data)
        new_order = Order(
            id=order["id"],
            name=order["name"],
            description=order["description"],
            start_date=order["start_date"],
            end_date=order["end_date"],
            address=order["address"],
            price=order["price"],
            customer_id=order["customer_id"],
            executor_id=order["executor_id"],
        )
        return new_order, 201


@app.route("/orders/<int:id>", methods=['GET', 'DELETE', 'PUT'])
def order(id):
    if request.method == "GET":
        return jsonify(Order.query.get(id).to_dict()), 200, {'Content-Type':'application/json; charset=UTF-8'}
    elif request.method == 'DELETE':
        order = Order.query.get(id)
        db.session.delete(order)
        db.session.commit()
        return "", 204
    elif request.method == 'PUT':
        order = json.loads(request.data)
        ord = Order.query.get(id)
        ord.id = order["id"],
        ord.name = order["name"],
        ord.description = order["description"],
        ord.start_date = order["start_date"],
        ord.end_date = order["end_date"],
        ord.address = order["address"],
        ord.price = order["price"],
        ord.customer_id = order["customer_id"],
        ord.executor_id = order["executor_id"]
        db.session.add(ord)
        db.session.commit()
        return order, 204


@app.route("/offers", methods=['GET', 'POST'])
def offers():
    if request.method == "GET":
        res =[]
        for ofe in Offer.query.all():
            res.append(ofe.to_dict())
        return jsonify(res), 200,{'Content-Type':'application/json; charset=UTF-8'}
    elif request.method == "POST":
        offer = json.loads(request.json)
        new_offer = Offer(
            id=request.json("id"),
            order_id=request.json("order_id"),
            executor_id=request.json("executor_id"),
        )
        db.session.add(new_offer)
        db.session.commit()
        return new_offer, 201


@app.route("/offer/<int:id>", methods=['GET', 'DELETE', 'PUT'])
def offer(id):
    if request.method == "GET":
        return jsonify(Offer.query.get(id).to_dict()), 200
    elif request.method == 'DELETE':
        offer = Offer.query.get(id)
        db.session.delete(offer)
        db.session.commit()
        return "",204
    elif request.method == 'PUT':
        offer = json.loads(request.data)
        off = Offer.query.get(id)
        off.id = offer["id"],
        off.order_id = offer["order_id"],
        off.executor_id = offer["executor_id"]
        db.session.add(off)
        db.session.commit()
        return offer, 200, {'Content-Type':'application/json; charset=UTF-8'}


if __name__ == '__main__':
    app.run()
