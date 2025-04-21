function updateSlotStatus(slotId, status) {
    const slotButton = document.getElementById(`slot_${slotId}`).getElementsByTagName('button')[0];
    slotButton.innerText = `Slot ${slotId + 1} - ${status}`;
}

function registerEntry() {
    const vehiclePlate = document.getElementById('vehicle_plate').value;
    const freeSlot = getFreeSlot();
    if (freeSlot !== null && vehiclePlate) {
        fetch('/assign_vehicle', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `slot_id=${freeSlot}&vehicle_plate=${vehiclePlate}`
        }).then(response => response.json()).then(data => {
            if (data.status === 'success') {
                updateSlotStatus(freeSlot, 'Occupied');
            }
        });
    }
}

function manualExit() {
    const vehiclePlate = document.getElementById('vehicle_plate').value;
    fetch('/manual_exit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `vehicle_plate=${vehiclePlate}`
    }).then(response => response.json()).then(data => {
        if (data.status === 'success') {
            const slotId = data.message.split(' ')[4] - 1; // Extract slot number from message
            updateSlotStatus(slotId, 'Free');
        }
    });
}

function getFreeSlot() {
    for (let i = 0; i < 16; i++) {
        if (document.getElementById(`slot_${i}`).getElementsByTagName('button')[0].innerText.includes("Free")) {
            return i;
        }
    }
    return null;
}

function exportLogs() {
    fetch('/export_logs')
        .then(response => response.json())
        .then(data => alert(data.message));
}
