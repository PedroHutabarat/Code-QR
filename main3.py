import cv2
from pyzbar.pyzbar import decode
import pandas as pd
import ast
from datetime import datetime

def decode_qr_code(frame):
    decoded_objects = decode(frame)

    decoded_data = None

    for obj in decoded_objects:
        decoded_data = obj.data.decode("utf-8")
        print(f'{decoded_data}')
    
    return decoded_data

# Camera Initialization
cam = cv2.VideoCapture(0)  # kamera utama (indeks 0)
cam.set(3, 320)
cam.set(4, 240)

known_serialcode = []
df = pd.DataFrame(columns=["Crate type", "Product", "Serial code", "Time"])


while True:
    success, frame = cam.read()

    # Calling The Decode fuction
    qr_code_information = decode_qr_code(frame)

    if qr_code_information is not None:
        serialcode = int(qr_code_information[-5:-1])
        
        if not serialcode in known_serialcode:
            known_serialcode.append(serialcode)

            current_date = datetime.now()
            formatted_date_time = current_date.strftime('%H:%M.%S %d-%m-%Y')

            data_list = list(ast.literal_eval(qr_code_information[1:-1]))
            data_list.append(formatted_date_time)
            df.loc[len(df)] = data_list

    # Shows The Camera Frame
    cv2.imshow("QR Code Scanner", frame)

    # Wait for 1 MiliSecond to take another picture
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close Camera and Window
cam.release()
cv2.destroyAllWindows()

# Saving Data to CSV with a Unique Name Based on Timestamp
csv_filename = f"Testing In {datetime.now().strftime('%H-%M-%S %d-%m-%Y')}.csv"
df.to_csv(csv_filename, index=False)