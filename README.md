# 🌟 VŨ TRỤ MA THUẬT - AR FACE FILTER APP
**Vũ Trụ Ma Thuật** là một ứng dụng camera real-time sử dụng OpenCV và MediaPipe để tạo ra những hiệu ứng visual tuyệt đẹp. Ứng dụng cung cấp 18+ hiệu ứng khác nhau từ cơ bản đến phức tạp, cho phép người dùng tạo ra những video và ảnh ma thuật độc đáo.
### 🎨 **18+ Hiệu ứng đa dạng**
#### 🌸 Hiệu ứng cơ bản
- **❄️ Bão tuyết Elsa**: Hiệu ứng tuyết rơi với ánh sáng lấp lánh
- **🌸 Hoa anh đào**: Cánh hoa bay theo gió xuân
- **💖 Tim yêu thương**: Trái tim bay lên với ánh sáng
- **⭐ Ngôi sao thiên hà**: Sao lấp lánh trên khắp màn hình
- **🌈 Cầu vồng ma thuật**: Cầu vồng động với 7 màu sắc

#### 🦄 Động vật ma thuật
- **🦋 Bướm nhiều màu**: Bướm bay múa theo chuyển động tự nhiên
- **🐲 Rồng lửa bay**: Rồng thần thoại với hiệu ứng lửa
- **🦄 Kỳ lân sừng vàng**: Kỳ lân với ánh sáng ma thuật
- **🔥 Phượng hoàng lửa**: Chim lửa huyền thoại tái sinh

#### 🌟 Thiên nhiên huyền bí
- **🔥 Lửa rồng**: Ngọn lửa bùng cháy mạnh mẽ
- **⚡ Tia sét thần Zeus**: Sấm sét xé toạc bầu trời
- **🌌 Cực quang ma thuật**: Aurora Borealis lung linh
- **☄️ Mưa sao băng**: Thiên thạch rơi với đuôi sáng
- **🌀 Xoáy thiên hà**: Dải ngân hà xoay tròn

#### 🔮 Phép thuật cổ đại
- **💎 Pha lê phép thuật**: Tinh thể phát sáng xoay tròn
- **🔮 Rune cổ đại**: Ký tự rune phát sáng thần bí
- **🌀 Cổng thời gian**: Portal ma thuật xoáy năng lượng
- **✨ Bùa phép lấp lánh**: Phép thuật bay lượn
- **⚡ Năng lượng ma thuật**: Tia năng lượng phép thuật

#### 🌌 Vũ trụ bất tận
- **🪐 Hành tinh bay**: Các hành tinh quay quanh quỹ đạo
- **🌫️ Tinh vân màu sắc**: Tinh vân mờ ảo đẹp mắt
- **🕳️ Hố đen hút**: Hố đen với hiệu ứng hút vật chất
- **🌟 Chòm sao kết nối**: Những chòm sao với đường nối


### 🎪 **4 Combo hiệu ứng đặc biệt**
1. **❄️ Băng Tuyết Cực Bắc**: Snow + Aurora + Crystals
2. **🔥 Địa Ngục Lửa**: Fire + Dragons + Phoenixes  
3. **🌌 Thiên Hà Bất Tận**: Galaxy + Planets + Constellation + Nebula
4. **🦄 Thần Thoại Cổ Đại**: Unicorns + Runes + Spells + Energy

### Phần cứng khuyến nghị
- **Camera**: Webcam tích hợp hoặc camera USB
- **CPU**: Intel i5 hoặc tương đương trở lên
- **RAM**: 4GB trở lên
- **HĐH**: Windows 10/11, macOS, Linux

### 1. Cài đặt dependencies
```bash
pip install opencv-python mediapipe pillow numpy
```

### 2. Chạy ứng dụng
```bash
python main.py
```

## 🚀 Hướng dẫn sử dụng

### Khởi động
1. Chạy lệnh `python main.py`
2. Ứng dụng sẽ tự động mở camera và hiển thị giao diện
3. Camera được hiển thị real-time bên phải màn hình

## 📁 Cấu trúc dự án

```
vu-tru-ma-thuat/
│
├── main.py              # File khởi chạy chính
├── app.py               # Lớp ứng dụng chính
├── camera.py            # Xử lý camera và capture
├── effects.py           # Quản lý hiệu ứng
├── particles.py         # Render các particle effects
├── gui.py               # Giao diện người dùng
└── README.md           # Tài liệu hướng dẫn
```


## 🐛 Xử lý sự cố

### Lỗi thường gặp

**Camera không hoạt động**
```bash
# Kiểm tra camera có được kết nối
# Thử thay đổi camera index trong camera.py
self.video = cv2.VideoCapture(1)  # Thử 1 thay vì 0
```

**FPS thấp**
```bash
# Giảm độ phân giải camera
self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 480)   # Thay vì 640
self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)  # Thay vì 480
```
pip install --upgrade opencv-python mediapipe pillow numpy
```


**🌟 Hãy để Vũ Trụ Ma Thuật biến camera của bạn thành cổng thông tin đến thế giới phép thuật! 🌟**

*Nếu bạn thích dự án này, hãy cho một ⭐ trên GitHub nhé!*
