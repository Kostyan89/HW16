import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import raw_data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///table.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.url_map.strict_slashes = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    email = db.Column(db.String(50))
    role = db.Column(db.String(50))
    phone = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "first.name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone
        }


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(50))
    description = db.Column(db.Text(200))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.Text(70))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return {
            "id":self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id
        }


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
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
        id=user_data['id'],
        first_name=user_data['first_name'],
        last_name=user_data['last_name'],
        age=user_data['first_name'],
        email=user_data['first_name'],
        role=user_data['first_name'],
        phone=user_data["phone"]
    )
    db.session.add(new_user)
    db.session.commit()


for order_data in raw_data.orders:
    new_order = Order(
        id=order_data['id'],
        name=order_data['name'],
        description=order_data['description'],
        start_date=order_data['start_date'],
        end_date=order_data['end_date'],
        address=order_data['address'],
        price=order_data['price'],
        customer_id=order_data['customer_id'],
        executor_id=order_data['executor_id']
    )
    db.session.add(new_order)
    db.session.commit()

for offer_data in raw_data.offers:
    new_offer = Offer(
        id=offer_data['id'],
        order_id=offer_data['order_id'],
        executor_id=offer_data['executor_id'],
    )
    db.session.add(new_offer)
    db.session.commit()


@app.route("/user/<int:id>", methods=['GET','POST', 'DELETE', 'PUT'])
def user(id):
    if request.method == "GET":
        return json.dumps(User.query.get(id).to_dict()), 200,{'Content-Type':'application/json; charset=UTF-8'}




if __name__ == '__main__':
    app.run()
