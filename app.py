import json
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from config import Config
import raw_data
from datetime import datetime


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    email = db.Column(db.String(50))
    role = db.Column(db.String(50))
    phone = db.Column(db.String(11))

    def to_dict(self):
        return {
            "id" : self.id,
            "first.name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone
        }


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.Text(70))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return {
            "id" : self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date.strf('%d/%m/%Y'),
            "end_date": self.end_date.strf('%d/%m/%Y'),
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id
        }


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return {
            "id" : self.id,
            "order_id" : self.order_id,
            "executor_id" : self.executor_id
        }


db.drop_all()
db.create_all()

for user_data in raw_data.users:
    new_user = User(
        first_name=user_data['first_name'],
        last_name=user_data['last_name'],
        age=user_data['first_name'],
        email=user_data['first_name'],
        role=user_data['first_name'],
        phone=user_data["phone"]
    )
    db.session.add(new_user)
db.session.commit()

for order in raw_data.orders:
    new_order = Order(
        name=order['name'],
        description=order['description'],
        start_date=datetime.strptime(order['start_date'], '%m/%d/%Y').date(),
        end_date=datetime.strptime(order['end_date'], '%m/%d/%Y').date(),
        address=order['address'],
        price=order['price'],
        customer_id=order['customer_id'],
        executor_id=order['executor_id']
    )
    db.session.add(new_order)
db.session.commit()

for offer in raw_data.offers:
    db.session.add(Offer(**offer))
db.session.commit()


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == "GET":
        result = []
        for u in User.query.all():
            result.append(u.to_dict())
        return jsonify(result)
    if request.method == "POST":
        try:
            new_user = User(
                first_name=request.json["first_name"],
                last_name=request.json["last_name"],
                age=request.json["age"],
                email=request.json["email"],
                role=request.json["role"],
                phone=request.json["phone"]
            )
            db.session.add(new_user)
            db.session.commit()
            return jsonify(new_user.to_dict()), 201
        except KeyError:
            abort(404)


@app.route("/users/<int:user_id>", methods=['GET', 'DELETE', 'PUT'])
def user(user_id):
    if request.method == "GET":
        return jsonify(User.query.get_or_404(user_id).to_dict())
    elif request.method == 'PUT':
        User.query.filter_by(id=user_id).update(request.json)
        db.session.commit()
        return jsonify(User.query.get_or_404(user_id).to_dict())
    elif request.method == 'DELETE':
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return "", 204


@app.route("/orders", methods=['GET', 'POST'])
def orders():
    if request.method == "GET":
        result = []
        for o in Order.query.all():
            result.append(o.to_dict())
        return jsonify(result)
    elif request.method == "POST":
        try:
            new_order = Order(
                name=order["name"],
                description=order["description"],
                start_date=order["start_date"],
                end_date=order["end_date"].strftime('%m/%d/%Y'),
                address=order["address"].strftime('%m/%d/%Y'),
                price=order["price"],
                customer_id=order["customer_id"],
                executor_id=order["executor_id"])
            db.session.add(new_order)
            db.session.commit()
            return jsonify(new_order.to_dict()), 201
        except KeyError:
            abort(404)


@app.route("/orders/<int:order_id>", methods=['GET', 'DELETE', 'PUT'])
def order(order_id):
    if request.method == "GET":
        return jsonify(Order.query.get_or_404(order_id).to_dict()), 200, {'Content-Type':'application/json; charset=UTF-8'}
    elif request.method == 'DELETE':
        order = Order.query.get_or_404(order_id)
        db.session.delete(order)
        db.session.commit()
        return "", 204
    elif request.method == 'PUT':
        Order.query.filter_by(id=order_id.update(request.json))
        db.session.commit()
        return jsonify(Order.query.get_or_404(order_id).to_dict())


@app.route("/offers", methods=['GET', 'POST'])
def offers():
    if request.method == "GET":
        res =[]
        for ofe in Offer.query.all():
            res.append(ofe.to_dict())
        return jsonify(res)
    elif request.method == "POST":
        try:
            new_offer = Offer(
                order_id=request.json("order_id"),
                executor_id=request.json("executor_id"),
            )
            db.session.add(new_offer)
            db.session.commit()
            return jsonify(new_offer.to_dict()), 201
        except KeyError:
            abort(404)


@app.route("/offers/<int:offer_id>", methods=['GET', 'DELETE', 'PUT'])
def offer(offer_id):
    if request.method == "GET":
        return jsonify(Offer.query.get_or_404(offer_id).to_dict()), 200
    elif request.method == 'DELETE':
        offer = Offer.query.get_or_404(offer_id)
        db.session.delete(offer)
        db.session.commit()
        return "", 204
    elif request.method == 'PUT':
        Offer.query.filter_by(id=offer_id).update(request.json)
        db.session.commit()
        return jsonify(Offer.query.get_or_404(offer_id).to_dict())


if __name__ == '__main__':
    app.run()
