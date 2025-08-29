import cv2
import numpy as np
import random
import math

class ParticleRenderer:
    def update_snow(self, particle, image, w, h):
        """Cập nhật hạt tuyết"""
        particle['y'] += particle['speed']
        particle['x'] += particle['drift'] + math.sin(particle['y'] * 0.01) * 2
        
        # Hiệu ứng lấp lánh
        sparkle_intensity = int(255 * abs(math.sin(particle['y'] * 0.05)))
        cv2.circle(image, (int(particle['x']), int(particle['y'])), 
                  particle['size'], (255, 255, 255), -1)
        cv2.circle(image, (int(particle['x']), int(particle['y'])), 
                  particle['size']//2, (sparkle_intensity, sparkle_intensity, 255), -1)
        
        return not (particle['y'] > h + 50 or particle['x'] < -100 or particle['x'] > w + 100)
    
    def update_cherry(self, particle, image, w, h):
        """Cập nhật hoa anh đào"""
        particle['y'] += particle['speed']
        particle['x'] += math.sin(particle['y'] * 0.02) * 3
        particle['rotation'] += particle['spin_speed']
        
        self.draw_rotating_flower(image, (int(particle['x']), int(particle['y'])), 
                                particle['size'], particle['rotation'])
        
        return particle['y'] <= h + 30
    
    def update_heart(self, particle, image, w, h):
        """Cập nhật trái tim"""
        particle['y'] -= particle['speed']
        particle['pulse'] += 0.2
        pulse_size = particle['size'] + int(5 * math.sin(particle['pulse']))
        
        self.draw_animated_heart(image, (int(particle['x']), int(particle['y'])), pulse_size)
        
        return particle['y'] >= -50
    
    def update_star(self, particle, image, w, h):
        """Cập nhật ngôi sao"""
        particle['twinkle'] += 0.3
        particle['life'] -= 1
        
        if particle['life'] > 0:
            alpha = particle['life'] / 100.0
            twinkle_size = particle['size'] + int(3 * math.sin(particle['twinkle']))
            
            self.draw_star(image, (int(particle['x']), int(particle['y'])), 
                         twinkle_size, alpha)
            return True
        return False
    
    def update_butterfly(self, particle, image, w, h):
        """Cập nhật bướm"""
        dx = particle['target_x'] - particle['x']
        dy = particle['target_y'] - particle['y']
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 5:
            particle['x'] += dx * 0.02
            particle['y'] += dy * 0.02
        else:
            particle['target_x'] = random.randint(0, w)
            particle['target_y'] = random.randint(0, h)
        
        particle['wing_phase'] += 0.5
        self.draw_butterfly(image, (int(particle['x']), int(particle['y'])), 
                          particle['color'], particle['wing_phase'])
        
        return not (particle['x'] < -100 or particle['x'] > w + 100 or 
                   particle['y'] < -100 or particle['y'] > h + 100)
    
    def update_fire(self, particle, image, w, h):
        """Cập nhật lửa"""
        particle['y'] -= particle['speed']
        particle['x'] += random.randint(-2, 2)
        particle['life'] -= 1
        
        if particle['life'] > 0:
            self.draw_fire_particle(image, (int(particle['x']), int(particle['y'])), 
                                  particle['size'], particle['intensity'], particle['life'])
            return True
        return False
    
    def update_rainbow(self, particle, image, w, h):
        """Cập nhật cầu vồng"""
        particle['x'] += particle['speed']
        
        arc_y = particle['y'] + int(50 * math.sin((particle['x'] + particle['arc_offset']) * 0.01))
        cv2.circle(image, (int(particle['x']), arc_y), 8, particle['color'], -1)
        
        return particle['x'] <= w + 50
    
    def draw_rotating_flower(self, image, center, size, rotation):
        """Vẽ hoa xoay"""
        x, y = center
        petals = 5
        
        for i in range(petals):
            angle = rotation + i * (360 / petals)
            petal_x = x + size * math.cos(math.radians(angle))
            petal_y = y + size * math.sin(math.radians(angle))
            cv2.circle(image, (int(petal_x), int(petal_y)), size//3, (255, 182, 193), -1)
        
        # Tâm hoa
        cv2.circle(image, (x, y), size//4, (255, 255, 0), -1)
    
    def draw_animated_heart(self, image, center, size):
        """Vẽ tim với animation"""
        x, y = center
        
        # Gradient heart
        for i in range(3):
            heart_size = size - i * 3
            color_intensity = 255 - i * 50
            
            # Vẽ 2 hình tròn phía trên
            cv2.circle(image, (x - heart_size//3, y - heart_size//3), 
                      heart_size//3, (color_intensity, 105, 180), -1)
            cv2.circle(image, (x + heart_size//3, y - heart_size//3), 
                      heart_size//3, (color_intensity, 105, 180), -1)
            
            # Vẽ tam giác phía dưới
            pts = np.array([[x - heart_size//2, y], [x + heart_size//2, y], 
                           [x, y + heart_size]], np.int32)
            cv2.fillPoly(image, [pts], (color_intensity, 105, 180))
        
        # Highlight
        cv2.circle(image, (x - size//6, y - size//2), size//8, (255, 255, 255), -1)
    
    def draw_star(self, image, center, size, alpha):
        """Vẽ ngôi sao lấp lánh"""
        x, y = center
        
        # Tạo 5 điểm ngôi sao
        points = []
        for i in range(10):
            angle = i * math.pi / 5
            radius = size if i % 2 == 0 else size // 2
            px = x + radius * math.cos(angle)
            py = y + radius * math.sin(angle)
            points.append([int(px), int(py)])
        
        color_intensity = int(255 * alpha)
        cv2.fillPoly(image, [np.array(points)], (color_intensity, color_intensity, 0))
        
        # Tia sáng
        for angle in [0, 45, 90, 135]:
            end_x = int(x + size * 2 * math.cos(math.radians(angle)))
            end_y = int(y + size * 2 * math.sin(math.radians(angle)))
            cv2.line(image, (x, y), (end_x, end_y), 
                    (color_intensity, color_intensity, 255), 1)
    
    def draw_butterfly(self, image, center, color, wing_phase):
        """Vẽ bướm"""
        x, y = center
        
        # Animation cánh
        wing_offset = int(5 * math.sin(wing_phase))
        
        # Thân bướm
        cv2.line(image, (x, y-15), (x, y+15), (139, 69, 19), 3)
        
        # Cánh trên
        wing_top_left = np.array([[x-20, y-10], [x-10-wing_offset, y-20], [x-5, y-5]], np.int32)
        wing_top_right = np.array([[x+20, y-10], [x+10+wing_offset, y-20], [x+5, y-5]], np.int32)
        
        # Cánh dưới
        wing_bot_left = np.array([[x-15, y], [x-8-wing_offset//2, y+15], [x-5, y+5]], np.int32)
        wing_bot_right = np.array([[x+15, y], [x+8+wing_offset//2, y+15], [x+5, y+5]], np.int32)
        
        cv2.fillPoly(image, [wing_top_left], color)
        cv2.fillPoly(image, [wing_top_right], color)
        cv2.fillPoly(image, [wing_bot_left], color)
        cv2.fillPoly(image, [wing_bot_right], color)
        
        # Viền cánh
        cv2.polylines(image, [wing_top_left], True, (0, 0, 0), 1)
        cv2.polylines(image, [wing_top_right], True, (0, 0, 0), 1)
        cv2.polylines(image, [wing_bot_left], True, (0, 0, 0), 1)
        cv2.polylines(image, [wing_bot_right], True, (0, 0, 0), 1)
        
        # Râu bướm
        cv2.line(image, (x-2, y-15), (x-5, y-20), (0, 0, 0), 1)
        cv2.line(image, (x+2, y-15), (x+5, y-20), (0, 0, 0), 1)
    
    def draw_fire_particle(self, image, center, size, intensity, life):
        """Vẽ hạt lửa"""
        x, y = center
        
        # Màu lửa thay đổi theo life
        life_ratio = life / 60.0
        red = int(255 * intensity)
        green = int(255 * intensity * life_ratio)
        blue = 0
        
        # Vẽ lửa với nhiều lớp
        for i in range(3):
            flame_size = size - i * 3
            flame_intensity = intensity - i * 0.2
            if flame_intensity > 0:
                flame_red = int(red * flame_intensity)
                flame_green = int(green * flame_intensity)
                
                cv2.circle(image, (x + random.randint(-2, 2), y + random.randint(-2, 2)), 
                          flame_size, (blue, flame_green, flame_red), -1)