from flask import request, jsonify, session
from flask import current_app as app
from werkzeug.security import generate_password_hash
from models.models import db, ParkingLot, ParkingSpot, ParkingRecord, User
from datetime import datetime


def is_admin():
    return session.get("role") == "admin"

@app.route('/lot', methods=['GET','POST'])
def create_parking_lot():
    # if not is_admin():
    #     return jsonify({"message": "Unauthorized"}), 403
    if request.method == 'GET':
        lots = ParkingLot.query.all()

        data = []
        for lot in lots:
            occupied_spots = []
            for spot in lot.spots:
                if spot.status == 'O':
                    occupied_spots.append(spot.spot_id)
            data.append({
                "id" : lot.lot_id,
                "name" : lot.lot_name,
                "price" : lot.price,
                "address" : lot.address,
                "pin_code" : lot.pin_code,
                "spots" : lot.number_of_spots,
                "a_spots" : lot.number_of_spots - len(occupied_spots),
                "o_spots_ids" : [spot.spot_id for spot in lot.spots if spot.status == 'O'],
                "spot_ids" : [spot.spot_id for spot in lot.spots]
                })
        

        return jsonify(data), 200
    
    if request.method == 'POST':
        data = request.get_json()
        lot = ParkingLot(
            lot_name=data['name'],
            price=data['price'],
            address=data['address'],
            pin_code=data['pin_code'],
            number_of_spots=data['spots']
        )
        db.session.add(lot)
        db.session.commit()

        # Create parking spots
        for i in range(lot.number_of_spots):
            spot = ParkingSpot(spot_id=f"S{lot.lot_id}-{i+1}", lot_id=lot.lot_id)
            db.session.add(spot)
        db.session.commit()

        return jsonify({"message": "Parking lot created"}), 201


@app.route('/admin/lot/<int:lot_id>', methods=['DELETE'])
def delete_parking_lot(lot_id):
    # if not is_admin():
    #     return jsonify({"message": "Unauthorized"}), 403

    lot = ParkingLot.query.get(lot_id)
    if not lot:
        return jsonify({"message": "Lot not found"}), 404

    for spot in lot.spots:
        if spot.status == 'O':
            return jsonify({"message": "Cannot delete lot with occupied spots"}), 400

    db.session.delete(lot)
    db.session.commit()
    return jsonify({"message": "Lot deleted"}), 200

@app.route('/admin/spot/<string:spot_id>', methods=['DELETE'])
def delete_parking_spot(spot_id):
    # if not is_admin():
    #     return jsonify({"message": "Unauthorized"}), 403

    spot = ParkingSpot.query.get(spot_id)
    if not spot:
        return jsonify({"message": "Spot not found"}), 404

    if spot.status == 'O':
        return jsonify({"message": "Cannot delete occupied spot"}), 400
    spot.lot.number_of_spots -= 1
    db.session.delete(spot)
    db.session.commit()
    return jsonify({"message": "Spot deleted"}), 200

@app.route('/admin/lot/<int:lot_id>', methods=['PUT'])
def update_parking_lot(lot_id):
    lot = ParkingLot.query.filter_by(lot_id=lot_id).first()
    if not lot:
        return jsonify({"message": "Lot not found"}), 404

    data = request.get_json()
    new_spots = int(data['spots'])
    current_total_spots = int(lot.number_of_spots)
    occupied_spots = ParkingSpot.query.filter_by(lot_id=lot_id, status='O').count()

    if current_total_spots != new_spots:
        
        if new_spots < current_total_spots and new_spots>=occupied_spots:
            # Reducing spots
            spots_to_delete = current_total_spots - new_spots
            available_spots = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').all()

            for i in range(spots_to_delete):
                db.session.delete(available_spots[i])

        elif new_spots > current_total_spots:
            # Increasing spots
            spots_to_add = int(data['spots']) - len(lot.spots)
            x = len(lot.spots)
            for i in range(spots_to_add):
                spot = ParkingSpot(
                    spot_id=f"s{lot.lot_id}-{x + i + 1}",
                    status='A',
                    lot_id=lot.lot_id
                )
                db.session.add(spot)

        else:
            return jsonify({"message": "Some error occured"}), 401

    # Update other lot details
    lot.lot_name = data['name']
    lot.price = data['price']
    lot.address = data['address']
    lot.pin_code = data['pin_code']
    lot.number_of_spots = new_spots

    db.session.commit()
    return jsonify({"message": "Lot updated"}), 200

@app.route('/reserve/<int:user_id>/<string:spot_id>', methods=['POST'])
def reserve_spot(user_id, spot_id):  
    # user_id = session.get('user_id')
    # if not user_id:
    #     return jsonify({"message": "Not logged in"}), 401

    spot = ParkingSpot.query.get(spot_id)
    if not spot or spot.status != 'A':
        return jsonify({"message": "Spot is not available"}), 400

    # try:
    spot.status = 'O'
    data = request.get_json()
    record = ParkingRecord(
        spot_id=spot_id,
        user_id=user_id,
        vehicle_number=data['vehicle_number'],
        status='O',
        parking_timestamp=datetime.strptime(data['parking_timestamp'],"%Y-%m-%d %H:%M:%S")
    )
    db.session.add(record)
    db.session.commit()
    return jsonify({"message": "Spot reserved"}), 200
    # except Exception as e:
    #     db.session.rollback()
    #     return jsonify({"message": "Failed to reserve spot", "error": str(e)}), 500


@app.route('/release/<int:user_id>/<string:spot_id>', methods=['POST'])
def release_spot(user_id, spot_id):
    # user_id = session.get('user_id')
    # print(user_id)
    spot = ParkingSpot.query.get(spot_id)
    if not spot or spot.status != 'O':
        return jsonify({"message": "Spot is not occupied"}), 400

    record = ParkingRecord.query.filter_by(spot_id=spot.spot_id, user_id=user_id,status='O').first()
    if not record:
        return jsonify({"message": "No active reservation found"}), 404

    record.leaving_timestamp = datetime.now()
    duration = (record.leaving_timestamp - record.parking_timestamp).total_seconds() / 3600  # minutes
    record.parking_cost = round(duration * spot.lot.price, 2)
    spot.status = 'A'
    record.status = 'A'
    db.session.commit()

    return jsonify({
        "message": "Spot released"}), 200

#route to fetch user
@app.route('/admin/users', methods=['GET'])
def get_users():
    # if not is_admin():
    #     return jsonify({"message": "Unauthorized"}), 403

    users = User.query.filter_by(role='user').all()
    data = []

    for user in users:
        data.append({
        "user_id": user.user_id,
        "email": user.email,
        "name": user.name,
        "address": user.address,
        "pin_code": user.pin_code
        })

    return jsonify(data), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    
    user = User.query.get(user_id)

    return jsonify({
        "user_id": user.user_id,
        "email": user.email,
        "password": "",
        "name": user.name,
        "contact_number": user.contact_number,
        "vehicle_number": user.vehicle_number,
        "address": user.address,
        "pin_code": user.pin_code
    }), 200

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    
    data = request.get_json()
    
    user = User.query.get(user_id)

    user.name = data['name']
    if data['password'].strip():
        user.password = generate_password_hash(data['password'])
    user.contact_number = data['contact_number']
    user.vehicle_number = data['vehicle_number']
    user.address = data['address']
    user.pin_code = data['pin_code']
    
    db.session.commit()
    
    return jsonify({"message": "User updated"}), 200



# route to fetch record of parking
@app.route('/records/<int:user_id>', methods=['GET'])
def get_records(user_id):
        
    records = ParkingRecord.query.filter_by(user_id=user_id).all()

    data = []
    for record in records:
        data.append({
            "record_id": record.record_id,
            "spot_id": record.spot_id,
            "spot_status": record.spot.status,
            "user_id": record.user_id,
            "lot_id": record.spot.lot_id,
            "lot_name": record.spot.lot.lot_name,
            "parking_price": record.spot.lot.price,
            "vehicle_number": record.vehicle_number,
            "parking_timestamp": record.parking_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "leaving_timestamp": record.leaving_timestamp.strftime("%Y-%m-%d %H:%M:%S") if record.leaving_timestamp else None,
            "parking_cost": record.parking_cost
        })

    return jsonify(data), 200

#route to get spot details of a spot
@app.route('/spot/detail/<string:spot_id>', methods=['GET'])
def get_spot_details(spot_id):
    spot = ParkingSpot.query.get(spot_id)
    if not spot:
        return jsonify({"message": "Spot not found"}), 404
    record = ParkingRecord.query.filter_by(spot_id=spot_id, status='O').first()
    
    if not record or spot.status == 'A':
        return jsonify({
            "lot_id": spot.lot.lot_id,
            "spot_id": spot.spot_id,
            "vehicle_number": None,
            "parking_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }), 200
    
    return jsonify({
        "lot_id": spot.lot.lot_id,
        "spot_id": spot.spot_id,
        "customer_id": record.user_id,
        "vehicle_number": record.vehicle_number,
        "parking_timestamp": record.parking_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "leaving_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "parking_cost": round((datetime.now() - record.parking_timestamp).total_seconds() / 3600 * spot.lot.price,2)
    })


# route for search functionality in admin page
@app.route('/search', methods=['GET'])
def search():
    search_term = request.args.get('searchTerm')
    lots = ParkingLot.query.filter(ParkingLot.lot_name.contains(search_term)).all()
    data = []
    for lot in lots:
        data.append({
            "id" : lot.lot_id,
            "name" : lot.lot_name,
            "price" : lot.price,
            "address" : lot.address,
            "pin_code" : lot.pin_code,
            "spots" : lot.number_of_spots,
            "a_spots" : lot.number_of_spots - len(lot.spots.filter_by(status='O').all()),
            "o_spots_ids" : [spot.spot_id for spot in lot.spots if spot.status == 'O'],
            "spot_ids" : [spot.spot_id for spot in lot.spots]
            })

    return jsonify(data), 200