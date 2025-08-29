from app import ARFaceFilterApp

if __name__ == "__main__":
    
    try:
        app = ARFaceFilterApp()
        app.run()
    except KeyboardInterrupt:
        print("\n👋 Tạm biệt! Hẹn gặp lại trong vũ trụ ma thuật!")
    except Exception as e:
        print(f"\n❌ Lỗi khởi động: {e}")
        print("   pip install opencv-python mediapipe pillow")