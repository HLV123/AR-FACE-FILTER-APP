import cv2
import time

class CameraHandler:
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    def process_frame(self, image):
        """Xử lý frame cơ bản"""
        # Lật ảnh và tăng độ sáng
        image = cv2.flip(image, 1)
        image = cv2.convertScaleAbs(image, alpha=1.1, beta=10)
        return image
    
    def capture_screenshot(self, image):
        """Chụp ảnh màn hình"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"magic_universe_{timestamp}.jpg"
        
        try:
            cv2.imwrite(filename, image)
            print(f"📸 Đã chụp ảnh: {filename}")
        except Exception as e:
            print(f"❌ Lỗi khi chụp ảnh: {e}")
    
    def release(self):
        """Giải phóng camera"""
        try:
            self.video.release()
        except:
            pass