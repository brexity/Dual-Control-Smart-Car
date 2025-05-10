import cv2
from cvzone.HandTrackingModule import HandDetector
import serial
import time

# === Update your Bluetooth COM port ===
bluetooth_port = 'COM6'  # Replace with your actual COM port
baud_rate = 9600         # Make sure this matches your device

# Try connecting to the Bluetooth serial port
try:
    bt = serial.Serial(bluetooth_port, baud_rate, timeout=1)
    time.sleep(2)  # Let it connect
    print(f"✅ Connected to Bluetooth on {bluetooth_port}")
except Exception as e:
    print(f"❌ Failed to connect to Bluetooth: {e}")
    bt = None

# Initialize camera and hand detector
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.5, maxHands=1)

while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        print("⚠️ Frame capture failed. Skipping...")
        continue

    # Flip/rotate as needed
    frame = cv2.rotate(frame, cv2.ROTATE_180)
    frame = cv2.flip(frame, -1)

    hands, frame = detector.findHands(frame)
    output = "S"  # Default gesture (Stop)

    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        count = fingers.count(1)

        if count == 1:
            output = "F"
        elif count == 2:
            output = "B"
        elif count == 3:
            output = "L"
        elif count == 4:
            output = "R"
        elif count == 0 or count == 5:
            output = "S"
    else:
        output = "S"

    # Send output every frame
    print(f"➡️ Sending: {output}")
    if bt:
        bt.write(output.encode())

    cv2.imshow("FRAME", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
if bt:
    bt.close()
    print("🔌 Bluetooth connection closed.")

