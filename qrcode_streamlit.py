import cv2

qrc = cv2.QRCodeDetector()
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if ret:
        ret_qr, decoded_infor, points, _ = qrc.detectAndDecodeMulti(frame)
        if ret_qr:
            for s, p in zip(decoded_infor, points):
                if s:
                    cv2.putText(frame, s, (100,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 1, cv2.LINE_AA)
                else:
                    pass
                frame = cv2.polylines(frame, [p.astype(int)], True, (0,0,255), 8)
        cv2.imshow('QRcode', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
