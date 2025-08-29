import mediapipe as mp
import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time
from camera import CameraHandler
from effects import EffectsManager
from gui import GUIManager

class ARFaceFilterApp:
    def __init__(self):
        # Khởi tạo MediaPipe
        self.mp_face_mesh = mp.solutions.face_mesh
        
        # Khởi tạo các component
        self.camera = CameraHandler()
        self.effects = EffectsManager()
        self.gui = GUIManager(self)
        
        # Biến điều khiển
        self.running = True
        self.current_frame = None
        
        # Bắt đầu camera thread
        self.camera_thread = threading.Thread(target=self.camera_loop)
        self.camera_thread.daemon = True
        self.camera_thread.start()
    
    def toggle_effect(self, effect_name):
        """Bật/tắt hiệu ứng"""
        self.effects.toggle_effect(effect_name)
        
        # Cập nhật số hiệu ứng đang hoạt động
        active_count = sum(1 for active in self.effects.effects.values() if active)
        self.gui.update_effects_count(active_count)
        
        print(f"{'✅' if self.effects.effects[effect_name] else '❌'} {effect_name}: {'ON' if self.effects.effects[effect_name] else 'OFF'}")
    
    def reset_all_effects(self):
        """Reset tất cả hiệu ứng"""
        self.effects.reset_all()
        self.gui.reset_checkboxes()
        self.gui.update_effects_count(0)
        print("🔄 Đã reset tất cả hiệu ứng")
    
    def set_combo_effects(self, effect_names):
        """Set combo hiệu ứng có sẵn"""
        self.reset_all_effects()
        
        for effect in effect_names:
            if effect in self.effects.effects:
                self.effects.effects[effect] = True
                self.gui.set_checkbox_by_name(effect, True)
        
        self.gui.update_effects_count(len(effect_names))
        combo_name = {
            ('snow', 'aurora', 'crystals'): "❄️ Băng Tuyết Cực Bắc",
            ('fire', 'dragons', 'phoenixes'): "🔥 Địa Ngục Lửa",
            ('galaxy', 'planets', 'constellation', 'nebula'): "🌌 Thiên Hà Bất Tận",
            ('unicorns', 'runes', 'spells', 'energy'): "🦄 Thần Thoại Cổ Đại"
        }
        combo_key = tuple(effect_names)
        combo_display = combo_name.get(combo_key, f"Combo {len(effect_names)} hiệu ứng")
        print(f"🌟 Kích hoạt combo: {combo_display}")
    
    def capture_from_gui(self):
        """Chụp ảnh từ nút GUI"""
        if self.current_frame is not None:
            self.camera.capture_screenshot(self.current_frame)
            try:
                self.gui.fps_label.config(text=f"📸 Đã lưu ảnh siêu đẹp!")
            except:
                pass
    
    def camera_loop(self):
        """Vòng lặp xử lý camera"""
        fps_counter = 0
        fps_start_time = time.time()
        
        while self.running:
            ret, image = self.camera.video.read()
            if not ret:
                break
            
            self.effects.frame_count += 1
            fps_counter += 1
            
            # Tính FPS
            if fps_counter % 30 == 0:
                fps = 30 / (time.time() - fps_start_time)
                try:
                    self.gui.fps_label.config(text=f"🎥 FPS: {fps:.1f} | Frame: {self.effects.frame_count}")
                    self.gui.particles_label.config(text=f"✨ Particles: {len(self.effects.particles)}")
                except:
                    pass
                fps_start_time = time.time()
            
            # Xử lý ảnh
            image = self.camera.process_frame(image)
            
            # Áp dụng hiệu ứng
            if any(self.effects.effects.values()):
                self.effects.update_particles(image)
                self.effects.draw_screen_border(image)
            
            # Lưu frame hiện tại
            self.current_frame = image.copy()
            
            # Hiển thị trên GUI
            try:
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image_pil = Image.fromarray(image_rgb)
                image_tk = ImageTk.PhotoImage(image_pil)
                
                self.gui.camera_label.configure(image=image_tk)
                self.gui.camera_label.image = image_tk
            except:
                pass
            
            time.sleep(0.03)
    
    def close_app(self):
        """Đóng ứng dụng"""
        print("👋 Cảm ơn bạn đã khám phá Vũ Trụ Ma Thuật!")
        self.running = False
        self.camera.release()
        try:
            self.gui.root.quit()
            self.gui.root.destroy()
        except:
            pass
    
    def run(self):
        """Chạy ứng dụng"""
        print("✨ Khởi động Vũ Trụ Ma Thuật với 18+ hiệu ứng siêu đẹp...")
        print("💡 Camera sẽ hiển thị trực tiếp trên giao diện")
        
        self.gui.root.protocol("WM_DELETE_WINDOW", self.close_app)
        
        try:
            self.gui.root.mainloop()
        except KeyboardInterrupt:
            self.close_app()
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            self.close_app()