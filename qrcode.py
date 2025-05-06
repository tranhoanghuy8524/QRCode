import streamlit as st
import cv2
import numpy as np
from PIL import Image

def run():
    st.header("📌 QR Code Detection")

    tab1, tab2 = st.tabs(["📷 Webcam", "🖼️ Ảnh Upload"])

    qr_detector = cv2.QRCodeDetector()

    # --- Tab 2: Upload ảnh ---
    with tab2:
        uploaded_file = st.file_uploader("Chọn ảnh", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            image = Image.open(uploaded_file).convert("RGB")
            img_np = np.array(image)
            retval, decoded_info, points, _ = qr_detector.detectAndDecodeMulti(img_np)

            st.image(image, caption="Ảnh đã upload", use_container_width=True)

            if retval and decoded_info:
                st.success("✅ QR Code phát hiện:")
                for d in decoded_info:
                    if d:
                        st.code(d)
            else:
                st.warning("⚠️ Không phát hiện QR Code nào.")

    # --- Tab 1: Mở webcam ---
    with tab1:
        start_cam = st.button("▶️ Bắt đầu Webcam")
        stop_cam = st.button("⏹️ Dừng Webcam")
        camera_placeholder = st.empty()

        if start_cam:
            cap = cv2.VideoCapture(0)
            st.info("Đang bật webcam...")

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                retval, decoded_info, points, _ = qr_detector.detectAndDecodeMulti(frame)

                if retval and decoded_info:
                    for s, p in zip(decoded_info, points):
                        if s:
                            p = p.astype(int)
                            frame = cv2.polylines(frame, [p], True, (0, 0, 255), 2)
                            frame = cv2.putText(frame, s, tuple(p[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                camera_placeholder.image(frame_rgb, channels="RGB")

                if stop_cam:
                    cap.release()
                    break

            cap.release()
            camera_placeholder.empty()
