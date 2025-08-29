import tkinter as tk
from tkinter import ttk

class GUIManager:
    def __init__(self, app):
        self.app = app
        self.create_gui()
    
    def create_gui(self):
        """Tạo giao diện người dùng"""
        self.root = tk.Tk()
        self.root.title("✨ Vũ Trụ Ma Thuật - Camera Live ✨")
        self.root.geometry("1000x600")
        self.root.configure(bg='#2c3e50')
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabelframe.Label', font=('Arial', 12, 'bold'))
        
        # Header
        header = tk.Label(self.root, text="✨ VŨ TRỤ MA THUẬT - CAMERA LIVE ✨", 
                         font=('Arial', 16, 'bold'), bg='#2c3e50', fg='#ecf0f1')
        header.pack(pady=5)
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Left panel - Control panel
        self.create_control_panel(main_frame)
        
        # Right panel - Camera display  
        self.create_camera_panel(main_frame)
    
    def create_control_panel(self, parent):
        """Tạo bảng điều khiển"""
        control_panel = tk.Frame(parent, bg='#34495e', width=300)
        control_panel.pack(side="left", fill="y", padx=(0, 10))
        control_panel.pack_propagate(False)
        
        # Title
        control_title = tk.Label(control_panel, text="🎛️ BẢNG ĐIỀU KHIỂN", 
                               font=('Arial', 14, 'bold'), bg='#34495e', fg='#ecf0f1')
        control_title.pack(pady=10)
        
        # Effects frame
        particle_frame = ttk.LabelFrame(control_panel, text="✨ Vũ trụ ma thuật", 
                                       padding=15, style='Title.TLabelframe')
        particle_frame.pack(fill="x", padx=10, pady=5)
        
        # Checkboxes
        self.snow_var = tk.BooleanVar()
        ttk.Checkbutton(particle_frame, text="❄️ Bão tuyết Elsa + hiệu ứng băng", 
                       variable=self.snow_var,
                       command=lambda: self.app.toggle_effect('snow')).pack(anchor="w", pady=2)
        
        self.cherry_var = tk.BooleanVar()
        ttk.Checkbutton(particle_frame, text="🌸 Hoa anh đào + gió xuân", 
                       variable=self.cherry_var,
                       command=lambda: self.app.toggle_effect('cherry_blossom')).pack(anchor="w", pady=2)
        
        self.hearts_var = tk.BooleanVar()
        ttk.Checkbutton(particle_frame, text="💖 Tim yêu thương + ánh sáng", 
                       variable=self.hearts_var,
                       command=lambda: self.app.toggle_effect('hearts')).pack(anchor="w", pady=2)
        
        self.stars_var = tk.BooleanVar()
        ttk.Checkbutton(particle_frame, text="⭐ Ngôi sao thiên hà", 
                       variable=self.stars_var,
                       command=lambda: self.app.toggle_effect('stars')).pack(anchor="w", pady=2)
        
        self.butterflies_var = tk.BooleanVar()
        ttk.Checkbutton(particle_frame, text="🦋 Bướm nhiều màu bay múa", 
                       variable=self.butterflies_var,
                       command=lambda: self.app.toggle_effect('butterflies')).pack(anchor="w", pady=2)
        
        self.fire_var = tk.BooleanVar()
        ttk.Checkbutton(particle_frame, text="🔥 Lửa rồng + tia lửa", 
                       variable=self.fire_var,
                       command=lambda: self.app.toggle_effect('fire')).pack(anchor="w", pady=2)
        
        self.rainbow_var = tk.BooleanVar()
        ttk.Checkbutton(particle_frame, text="🌈 Cầu vồng ma thuật", 
                       variable=self.rainbow_var,
                       command=lambda: self.app.toggle_effect('rainbow')).pack(anchor="w", pady=2)
        
        # Status frame
        status_frame = ttk.LabelFrame(control_panel, text="📊 Thông tin", 
                                     padding=10, style='Title.TLabelframe')
        status_frame.pack(fill="x", padx=10, pady=5)
        
        self.fps_label = tk.Label(status_frame, text="🎥 Camera đang khởi động...",
                                 font=("Arial", 9), fg="#95a5a6", bg='white')
        self.fps_label.pack()
        
        self.particles_label = tk.Label(status_frame, text="✨ Particles: 0",
                                       font=("Arial", 9), fg="#3498db", bg='white')
        self.particles_label.pack()
        
        # Buttons frame
        buttons_frame = tk.Frame(control_panel, bg='#34495e')
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        # Capture button
        capture_btn = tk.Button(buttons_frame, text="📸 Chụp Ảnh", 
                               command=self.app.capture_from_gui,
                               font=("Arial", 12, 'bold'), bg="#e74c3c", fg="white", 
                               relief="raised", height=2)
        capture_btn.pack(fill="x", pady=2)
        
        # Reset button
        reset_btn = tk.Button(buttons_frame, text="🔄 Reset Tất Cả", 
                             command=self.app.reset_all_effects,
                             font=("Arial", 10), bg="#f39c12", fg="white", 
                             relief="raised")
        reset_btn.pack(fill="x", pady=2)
        
        # Info frame
        info_frame = tk.Frame(control_panel, bg='#34495e')
        info_frame.pack(fill="x", padx=10, pady=5)
        
        info_text = """💡 HƯỚNG DẪN:
• Tick chọn hiệu ứng để kích hoạt
• Kết hợp nhiều hiệu ứng cùng lúc
• Nhấn 'Chụp Ảnh' để lưu khoảnh khắc
• Đóng cửa sổ để thoát"""
        
        info_label = tk.Label(info_frame, text=info_text,
                             font=("Arial", 9), fg="#ecf0f1", bg='#34495e',
                             justify="left")
        info_label.pack()
    
    def create_camera_panel(self, parent):
        """Tạo panel hiển thị camera"""
        camera_panel = tk.Frame(parent, bg='#2c3e50')
        camera_panel.pack(side="right", fill="both", expand=True)
        
        camera_title = tk.Label(camera_panel, text="📹 CAMERA TRỰC TIẾP", 
                               font=('Arial', 14, 'bold'), bg='#2c3e50', fg='#ecf0f1')
        camera_title.pack(pady=5)
        
        # Camera display label
        self.camera_label = tk.Label(camera_panel, bg='#2c3e50')
        self.camera_label.pack(expand=True, fill="both", padx=10, pady=10)
    
    def reset_checkboxes(self):
        """Reset tất cả checkbox"""
        self.snow_var.set(False)
        self.cherry_var.set(False)
        self.hearts_var.set(False)
        self.stars_var.set(False)
        self.butterflies_var.set(False)
        self.fire_var.set(False)
        self.rainbow_var.set(False)