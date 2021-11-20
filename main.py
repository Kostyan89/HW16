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
