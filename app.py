from flask import Flask, render_template, request, jsonify
import random
import datetime
import json

app = Flask(__name__)

# Smart Parking System
total_slots = 16
slot_status = ["Free"] * total_slots
vehicle_data = {}
activity_log = []

# Route for main page
@app.route('/')
def index():
    return render_template('index.html', slots=total_slots, slot_status=slot_status)

# Route for assigning a vehicle
@app.route('/assign_vehicle', methods=['POST'])
def assign_vehicle():
    slot_id = int(request.form['slot_id'])
    plate = request.form['vehicle_plate']
    
    if slot_status[slot_id] == "Free":
        vehicle_data[plate] = slot_id
        slot_status[slot_id] = "Occupied"
        log(f"Manual Entry: Vehicle {plate} assigned to Slot {slot_id + 1}")
        return jsonify({'status': 'success', 'message': f"Vehicle {plate} assigned to Slot {slot_id + 1}"})
    else:
        return jsonify({'status': 'error', 'message': 'This slot is already occupied.'})

# Route for manual exit
@app.route('/manual_exit', methods=['POST'])
def manual_exit():
    plate = request.form['vehicle_plate']
    if plate in vehicle_data:
        slot_id = vehicle_data.pop(plate)
        slot_status[slot_id] = "Free"
        log(f"Manual Exit: Vehicle {plate} left from Slot {slot_id + 1}")
        return jsonify({'status': 'success', 'message': f"Vehicle {plate} left from Slot {slot_id + 1}"})
    else:
        return jsonify({'status': 'error', 'message': 'Vehicle not found in system.'})

# Route for simulating IoT data (auto-assign vehicles or free up slots)
@app.route('/simulate_iot', methods=['POST'])
def simulate_iot():
    index = random.randint(0, total_slots - 1)
    if slot_status[index] == "Free":
        plate = f"IOT-{random.randint(1000,9999)}"
        slot_status[index] = "Occupied"
        vehicle_data[plate] = index
        log(f"IoT Entry: Vehicle {plate} auto-assigned to Slot {index + 1}")
    elif random.random() < 0.5:
        plate_to_remove = None
        for plate, idx in vehicle_data.items():
            if idx == index:
                plate_to_remove = plate
                break
        if plate_to_remove:
            vehicle_data.pop(plate_to_remove)
            slot_status[index] = "Free"
            log(f"IoT Exit: Vehicle {plate_to_remove} exited from Slot {index + 1}")
    return jsonify({'status': 'success'})

# Route for exporting logs
@app.route('/export_logs', methods=['GET'])
def export_logs():
    filename = f"logs/parking_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump({"logs": activity_log}, f, indent=4)
    return jsonify({'status': 'success', 'message': f"Logs exported as {filename}"})

def log(msg):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] {msg}"
    activity_log.append(log_entry)

if __name__ == '__main__':
    app.run(debug=True)
