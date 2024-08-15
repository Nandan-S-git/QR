import cv2
from pyzbar import pyzbar
import requests

def decode_qr(frame):
    qr_codes = pyzbar.decode(frame)
    qr_data_list = []

    for qr_code in qr_codes:
        (x, y, w, h) = qr_code.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        qr_data = qr_code.data.decode('utf-8')
        qr_type = qr_code.type
        text = f'{qr_data} ({qr_type})'
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        qr_data_list.append(qr_data)

    return frame, qr_data_list

def send_to_database(qr_data):
    url = "http://localhost:5000/add_qr"
    response = requests.post(url, json={"qr_data": qr_data})
    if response.status_code == 200:
        print("Data sent successfully")
    else:
        print("Failed to send data")

def fetch_details_from_database(qr_data):
    url = f"http://localhost:5000/get_attendee_by_qr/{qr_data}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"QR Data: {data['qr_data']}, Name: {data['name']}, Image URL: {data['image_url']}, Category: {data['category']}")
    else:
        print("Failed to fetch data")

def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame, qr_data_list = decode_qr(frame)

        if qr_data_list:
            for qr_data in qr_data_list:
                print(f"QR Code Data: {qr_data}")
                send_to_database(qr_data)
                fetch_details_from_database(qr_data)

        cv2.imshow('QR Code Scanner', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if _name_ == '_main_':
    main()