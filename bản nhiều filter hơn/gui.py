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
        """Tạo bảng điều khiển với scrollbar"""
        control_panel = tk.Frame(parent, bg='#34495e', width=320)
        control_panel.pack(side="left", fill="y", padx=(0, 10))
        control_panel.pack_propagate(False)
        
        # Title
        control_title = tk.Label(control_panel, text="🎛️ BẢNG ĐIỀU KHIỂN VŨ TRỤ", 
                               font=('Arial', 14, 'bold'), bg='#34495e', fg='#ecf0f1')
        control_title.pack(pady=10)
        
        # Scrollable frame container
        scroll_container = tk.Frame(control_panel, bg='#34495e')
        scroll_container.pack(fill="both", expand=True, padx=10)
        
        # Canvas và scrollbar
        canvas = tk.Canvas(scroll_container, bg='#34495e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#34495e')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas và scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel binding
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Effects frame - CƠ BẢN
        basic_frame = ttk.LabelFrame(scrollable_frame, text="✨ Hiệu ứng cơ bản", 
                                   padding=10, style='Title.TLabelframe')
        basic_frame.pack(fill="x", pady=5)
        
        # Basic Effects Checkboxes
        self.snow_var = tk.BooleanVar()
        ttk.Checkbutton(basic_frame, text="❄️ Bão tuyết Elsa + hiệu ứng băng", 
                       variable=self.snow_var,
                       command=lambda: self.app.toggle_effect('snow')).pack(anchor="w", pady=1)
        
        self.cherry_var = tk.BooleanVar()
        ttk.Checkbutton(basic_frame, text="🌸 Hoa anh đào + gió xuân", 
                       variable=self.cherry_var,
                       command=lambda: self.app.toggle_effect('cherry_blossom')).pack(anchor="w", pady=1)
        
        self.hearts_var = tk.BooleanVar()
        ttk.Checkbutton(basic_frame, text="💖 Tim yêu thương + ánh sáng", 
                       variable=self.hearts_var,
                       command=lambda: self.app.toggle_effect('hearts')).pack(anchor="w", pady=1)
        
        self.stars_var = tk.BooleanVar()
        ttk.Checkbutton(basic_frame, text="⭐ Ngôi sao thiên hà", 
                       variable=self.stars_var,
                       command=lambda: self.app.toggle_effect('stars')).pack(anchor="w", pady=1)
        
        self.rainbow_var = tk.BooleanVar()
        ttk.Checkbutton(basic_frame, text="🌈 Cầu vồng ma thuật", 
                       variable=self.rainbow_var,
                       command=lambda: self.app.toggle_effect('rainbow')).pack(anchor="w", pady=1)
        
        # Effects frame - ĐỘNG VẬT
        animals_frame = ttk.LabelFrame(scrollable_frame, text="🦄 Động vật ma thuật", 
                                     padding=10, style='Title.TLabelframe')
        animals_frame.pack(fill="x", pady=5)
        
        self.butterflies_var = tk.BooleanVar()
        ttk.Checkbutton(animals_frame, text="🦋 Bướm nhiều màu bay múa", 
                       variable=self.butterflies_var,
                       command=lambda: self.app.toggle_effect('butterflies')).pack(anchor="w", pady=1)
        
        self.dragons_var = tk.BooleanVar()
        ttk.Checkbutton(animals_frame, text="🐲 Rồng lửa bay lượn", 
                       variable=self.dragons_var,
                       command=lambda: self.app.toggle_effect('dragons')).pack(anchor="w", pady=1)
        
        self.unicorns_var = tk.BooleanVar()
        ttk.Checkbutton(animals_frame, text="🦄 Kỳ lân sừng vàng", 
                       variable=self.unicorns_var,
                       command=lambda: self.app.toggle_effect('unicorns')).pack(anchor="w", pady=1)
        
        self.phoenixes_var = tk.BooleanVar()
        ttk.Checkbutton(animals_frame, text="🔥 Phượng hoàng lửa thiêng", 
                       variable=self.phoenixes_var,
                       command=lambda: self.app.toggle_effect('phoenixes')).pack(anchor="w", pady=1)
        
        # Effects frame - THIÊN NHIÊN
        nature_frame = ttk.LabelFrame(scrollable_frame, text="🌟 Thiên nhiên huyền bí", 
                                    padding=10, style='Title.TLabelframe')
        nature_frame.pack(fill="x", pady=5)
        
        self.fire_var = tk.BooleanVar()
        ttk.Checkbutton(nature_frame, text="🔥 Lửa rồng + tia lửa", 
                       variable=self.fire_var,
                       command=lambda: self.app.toggle_effect('fire')).pack(anchor="w", pady=1)
        
        self.lightning_var = tk.BooleanVar()
        ttk.Checkbutton(nature_frame, text="⚡ Tia sét thần Zeus", 
                       variable=self.lightning_var,
                       command=lambda: self.app.toggle_effect('lightning')).pack(anchor="w", pady=1)
        
        self.aurora_var = tk.BooleanVar()
        ttk.Checkbutton(nature_frame, text="🌌 Cực quang ma thuật", 
                       variable=self.aurora_var,
                       command=lambda: self.app.toggle_effect('aurora')).pack(anchor="w", pady=1)
        
        self.meteor_var = tk.BooleanVar()
        ttk.Checkbutton(nature_frame, text="☄️ Mưa sao băng", 
                       variable=self.meteor_var,
                       command=lambda: self.app.toggle_effect('meteor')).pack(anchor="w", pady=1)
        
        self.galaxy_var = tk.BooleanVar()
        ttk.Checkbutton(nature_frame, text="🌀 Xoáy thiên hà", 
                       variable=self.galaxy_var,
                       command=lambda: self.app.toggle_effect('galaxy')).pack(anchor="w", pady=1)
        
        # Effects frame - MA THUẬT
        magic_frame = ttk.LabelFrame(scrollable_frame, text="🔮 Phép thuật cổ đại", 
                                   padding=10, style='Title.TLabelframe')
        magic_frame.pack(fill="x", pady=5)
        
        self.crystals_var = tk.BooleanVar()
        ttk.Checkbutton(magic_frame, text="💎 Pha lê phép thuật", 
                       variable=self.crystals_var,
                       command=lambda: self.app.toggle_effect('crystals')).pack(anchor="w", pady=1)
        
        self.runes_var = tk.BooleanVar()
        ttk.Checkbutton(magic_frame, text="🔮 Rune cổ đại phát sáng", 
                       variable=self.runes_var,
                       command=lambda: self.app.toggle_effect('runes')).pack(anchor="w", pady=1)
        
        self.portals_var = tk.BooleanVar()
        ttk.Checkbutton(magic_frame, text="🌀 Cổng thời gian xoáy", 
                       variable=self.portals_var,
                       command=lambda: self.app.toggle_effect('portals')).pack(anchor="w", pady=1)
        
        self.spells_var = tk.BooleanVar()
        ttk.Checkbutton(magic_frame, text="✨ Bùa phép lấp lánh", 
                       variable=self.spells_var,
                       command=lambda: self.app.toggle_effect('spells')).pack(anchor="w", pady=1)
        
        self.energy_var = tk.BooleanVar()
        ttk.Checkbutton(magic_frame, text="⚡ Năng lượng ma thuật", 
                       variable=self.energy_var,
                       command=lambda: self.app.toggle_effect('energy')).pack(anchor="w", pady=1)
        
        # Effects frame - VŨ TRỤ
        cosmic_frame = ttk.LabelFrame(scrollable_frame, text="🌌 Vũ trụ bất tận", 
                                    padding=10, style='Title.TLabelframe')
        cosmic_frame.pack(fill="x", pady=5)
        
        self.planets_var = tk.BooleanVar()
        ttk.Checkbutton(cosmic_frame, text="🪐 Hành tinh bay lơ lửng", 
                       variable=self.planets_var,
                       command=lambda: self.app.toggle_effect('planets')).pack(anchor="w", pady=1)
        
        self.nebula_var = tk.BooleanVar()
        ttk.Checkbutton(cosmic_frame, text="🌫️ Tinh vân màu sắc", 
                       variable=self.nebula_var,
                       command=lambda: self.app.toggle_effect('nebula')).pack(anchor="w", pady=1)
        
        self.blackhole_var = tk.BooleanVar()
        ttk.Checkbutton(cosmic_frame, text="🕳️ Hố đen hút vạn vật", 
                       variable=self.blackhole_var,
                       command=lambda: self.app.toggle_effect('blackhole')).pack(anchor="w", pady=1)
        
        self.constellation_var = tk.BooleanVar()
        ttk.Checkbutton(cosmic_frame, text="🌟 Chòm sao kết nối", 
                       variable=self.constellation_var,
                       command=lambda: self.app.toggle_effect('constellation')).pack(anchor="w", pady=1)
        
        # Status frame
        status_frame = ttk.LabelFrame(scrollable_frame, text="📊 Thông tin hệ thống", 
                                     padding=10, style='Title.TLabelframe')
        status_frame.pack(fill="x", pady=5)
        
        self.fps_label = tk.Label(status_frame, text="🎥 Camera đang khởi động...",
                                 font=("Arial", 9), fg="#95a5a6", bg='white')
        self.fps_label.pack()
        
        self.particles_label = tk.Label(status_frame, text="✨ Particles: 0",
                                       font=("Arial", 9), fg="#3498db", bg='white')
        self.particles_label.pack()
        
        self.effects_count_label = tk.Label(status_frame, text="🔮 Hiệu ứng: 0/18",
                                           font=("Arial", 9), fg="#e74c3c", bg='white')
        self.effects_count_label.pack()
        
        # Buttons frame
        buttons_frame = tk.Frame(scrollable_frame, bg='#34495e')
        buttons_frame.pack(fill="x", pady=10)
        
        # Capture button
        capture_btn = tk.Button(buttons_frame, text="📸 Chụp Ảnh Siêu Đẹp", 
                               command=self.app.capture_from_gui,
                               font=("Arial", 11, 'bold'), bg="#e74c3c", fg="white", 
                               relief="raised", height=2)
        capture_btn.pack(fill="x", pady=2)
        
        # Reset button
        reset_btn = tk.Button(buttons_frame, text="🔄 Reset Toàn Bộ Vũ Trụ", 
                             command=self.app.reset_all_effects,
                             font=("Arial", 10), bg="#f39c12", fg="white", 
                             relief="raised")
        reset_btn.pack(fill="x", pady=2)
        
        # Combo effects buttons
        combo_frame = tk.Frame(scrollable_frame, bg='#34495e')
        combo_frame.pack(fill="x", pady=5)
        
        tk.Label(combo_frame, text="🌟 COMBO HIỆU ỨNG:", 
                font=("Arial", 10, 'bold'), bg='#34495e', fg='#ecf0f1').pack()
        
        combo1_btn = tk.Button(combo_frame, text="❄️ Băng Tuyết Cực Bắc", 
                              command=lambda: self.app.set_combo_effects(['snow', 'aurora', 'crystals']),
                              font=("Arial", 9), bg="#3498db", fg="white", 
                              relief="raised")
        combo1_btn.pack(fill="x", pady=1)
        
        combo2_btn = tk.Button(combo_frame, text="🔥 Địa Ngục Lửa", 
                              command=lambda: self.app.set_combo_effects(['fire', 'dragons', 'phoenixes']),
                              font=("Arial", 9), bg="#e74c3c", fg="white", 
                              relief="raised")
        combo2_btn.pack(fill="x", pady=1)
        
        combo3_btn = tk.Button(combo_frame, text="🌌 Thiên Hà Bất Tận", 
                              command=lambda: self.app.set_combo_effects(['galaxy', 'planets', 'constellation', 'nebula']),
                              font=("Arial", 9), bg="#8e44ad", fg="white", 
                              relief="raised")
        combo3_btn.pack(fill="x", pady=1)
        
        combo4_btn = tk.Button(combo_frame, text="🦄 Thần Thoại Cổ Đại", 
                              command=lambda: self.app.set_combo_effects(['unicorns', 'runes', 'spells', 'energy']),
                              font=("Arial", 9), bg="#f39c12", fg="white", 
                              relief="raised")
        combo4_btn.pack(fill="x", pady=1)
        
        # Info frame
        info_frame = tk.Frame(scrollable_frame, bg='#34495e')
        info_frame.pack(fill="x", pady=5)
        
        info_text = """💡 HƯỚNG DẪN VŨ TRỤ MA THUẬT:
• 18+ hiệu ứng siêu đẹp mắt
• Kết hợp tùy ý để tạo màn hình thần kỳ
• Dùng COMBO có sẵn hoặc tự chọn
• Ngẫu nhiên để khám phá điều bất ngờ
• Chụp ảnh lưu khoảnh khắc ma thuật
• Cuộn chuột để xem hết hiệu ứng"""
        
        info_label = tk.Label(info_frame, text=info_text,
                             font=("Arial", 8), fg="#bdc3c7", bg='#34495e',
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
        # Cơ bản
        self.snow_var.set(False)
        self.cherry_var.set(False)
        self.hearts_var.set(False)
        self.stars_var.set(False)
        self.rainbow_var.set(False)
        
        # Động vật
        self.butterflies_var.set(False)
        self.dragons_var.set(False)
        self.unicorns_var.set(False)
        self.phoenixes_var.set(False)
        
        # Thiên nhiên
        self.fire_var.set(False)
        self.lightning_var.set(False)
        self.aurora_var.set(False)
        self.meteor_var.set(False)
        self.galaxy_var.set(False)
        
        # Ma thuật
        self.crystals_var.set(False)
        self.runes_var.set(False)
        self.portals_var.set(False)
        self.spells_var.set(False)
        self.energy_var.set(False)
        
        # Vũ trụ
        self.planets_var.set(False)
        self.nebula_var.set(False)
        self.blackhole_var.set(False)
        self.constellation_var.set(False)
    
    def update_effects_count(self, count):
        """Cập nhật số hiệu ứng đang hoạt động"""
        try:
            self.effects_count_label.config(text=f"🔮 Hiệu ứng: {count}/18")
        except:
            pass
    
    def set_checkbox_by_name(self, effect_name, value):
        """Set checkbox theo tên hiệu ứng"""
        checkbox_map = {
            'snow': self.snow_var,
            'cherry_blossom': self.cherry_var,
            'hearts': self.hearts_var,
            'stars': self.stars_var,
            'rainbow': self.rainbow_var,
            'butterflies': self.butterflies_var,
            'dragons': self.dragons_var,
            'unicorns': self.unicorns_var,
            'phoenixes': self.phoenixes_var,
            'fire': self.fire_var,
            'lightning': self.lightning_var,
            'aurora': self.aurora_var,
            'meteor': self.meteor_var,
            'galaxy': self.galaxy_var,
            'crystals': self.crystals_var,
            'runes': self.runes_var,
            'portals': self.portals_var,
            'spells': self.spells_var,
            'energy': self.energy_var,
            'planets': self.planets_var,
            'nebula': self.nebula_var,
            'blackhole': self.blackhole_var,
            'constellation': self.constellation_var
        }
        
        if effect_name in checkbox_map:
            checkbox_map[effect_name].set(value)