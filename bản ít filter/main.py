from app import ARFaceFilterApp

if __name__ == "__main__":
    print("")
    
    try:
        app = ARFaceFilterApp()
        app.run()
    except KeyboardInterrupt:
        print("\n👋 Tạm biệt!")
    except Exception as e:
        print(f"\n❌ Lỗi khởi động: {e}")
        print("💡 Hãy đảm bảo webcam đã được kết nối và cài đặt đầy đủ thư viện!")
        print("   pip install opencv-python mediapipe pillow")