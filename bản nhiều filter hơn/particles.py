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
    
    # ===== DRAWING FUNCTIONS =====
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
    
    def draw_dragon(self, image, center, size, wing_beat):
        """Vẽ rồng lửa"""
        x, y = center
        
        # Thân rồng
        cv2.ellipse(image, (x, y), (size, size//2), 0, 0, 360, (139, 0, 0), -1)
        
        # Đầu rồng
        head_x = x + size//2
        cv2.circle(image, (head_x, y), size//3, (200, 0, 0), -1)
        
        # Mắt
        cv2.circle(image, (head_x + 5, y - 5), 3, (255, 255, 0), -1)
        
        # Cánh với animation
        wing_flap = int(10 * math.sin(wing_beat))
        wing_top = np.array([[x-size//2, y-10], [x-size, y-20-wing_flap], [x-size//3, y]], np.int32)
        wing_bottom = np.array([[x-size//2, y+10], [x-size, y+20+wing_flap], [x-size//3, y]], np.int32)
        
        cv2.fillPoly(image, [wing_top], (100, 0, 100))
        cv2.fillPoly(image, [wing_bottom], (100, 0, 100))
        
        # Đuôi
        tail_points = np.array([[x-size, y], [x-size*1.5, y-10], [x-size*1.3, y], [x-size*1.5, y+10]], np.int32)
        cv2.fillPoly(image, [tail_points], (139, 0, 0))
    
    def draw_unicorn(self, image, center, horn_glow):
        """Vẽ kỳ lân"""
        x, y = center
        
        # Thân
        cv2.ellipse(image, (x, y), (25, 15), 0, 0, 360, (255, 255, 255), -1)
        
        # Đầu
        cv2.circle(image, (x, y-10), 12, (255, 255, 255), -1)
        
        # Sừng với ánh sáng
        horn_glow_intensity = int(100 + 155 * abs(math.sin(horn_glow)))
        cv2.line(image, (x, y-22), (x, y-35), (255, horn_glow_intensity, 0), 3)
        
        # Mắt
        cv2.circle(image, (x-3, y-12), 2, (0, 0, 0), -1)
        cv2.circle(image, (x+3, y-12), 2, (0, 0, 0), -1)
        
        # Bờm
        for i in range(5):
            mane_x = x - 10 + i * 4
            cv2.line(image, (mane_x, y-15), (mane_x-2, y-25), (255, 192, 203), 2)
        
        # Chân
        for i in range(4):
            leg_x = x - 15 + i * 10
            cv2.line(image, (leg_x, y+15), (leg_x, y+25), (255, 255, 255), 3)
    
    def draw_phoenix(self, image, center, wing_phase):
        """Vẽ phượng hoàng"""
        x, y = center
        
        # Thân phượng hoàng
        cv2.ellipse(image, (x, y), (20, 12), 0, 0, 360, (255, 100, 0), -1)
        
        # Đầu
        cv2.circle(image, (x+15, y-5), 8, (255, 150, 0), -1)
        
        # Mắt
        cv2.circle(image, (x+18, y-7), 2, (255, 255, 0), -1)
        
        # Mỏ
        beak = np.array([[x+23, y-5], [x+28, y-3], [x+23, y-1]], np.int32)
        cv2.fillPoly(image, [beak], (255, 200, 0))
        
        # Cánh lửa với animation
        wing_offset = int(8 * math.sin(wing_phase))
        
        # Cánh trái
        wing_left = np.array([[x-10, y], [x-25, y-15-wing_offset], [x-20, y-5], [x-15, y+5]], np.int32)
        cv2.fillPoly(image, [wing_left], (255, 50, 0))
        
        # Cánh phải
        wing_right = np.array([[x-5, y-10], [x-15, y-25-wing_offset], [x-10, y-15], [x-5, y-5]], np.int32)
        cv2.fillPoly(image, [wing_right], (255, 80, 0))
        
        # Đuôi lửa
        tail_flames = [
            np.array([[x-20, y+5], [x-35, y+10], [x-30, y+15], [x-25, y+12]], np.int32),
            np.array([[x-18, y+8], [x-32, y+15], [x-28, y+20], [x-22, y+15]], np.int32),
            np.array([[x-15, y+10], [x-30, y+18], [x-25, y+25], [x-20, y+18]], np.int32)
        ]
        
        colors = [(255, 0, 0), (255, 100, 0), (255, 200, 0)]
        for i, tail_part in enumerate(tail_flames):
            cv2.fillPoly(image, [tail_part], colors[i])
    
    def draw_crystal(self, image, center, size, rotation, glow_intensity):
        """Vẽ pha lê ma thuật"""
        x, y = center
        
        # Tạo hình pha lê 6 cạnh
        points = []
        for i in range(6):
            angle = rotation + i * 60
            px = x + (size//2) * math.cos(math.radians(angle))
            py = y + (size//2) * math.sin(math.radians(angle))
            points.append([int(px), int(py)])
        
        # Vẽ pha lê với gradient
        cv2.fillPoly(image, [np.array(points)], (glow_intensity, 0, glow_intensity))
        
        # Viền sáng
        cv2.polylines(image, [np.array(points)], True, (255, glow_intensity, 255), 2)
        
        # Trung tâm sáng
        cv2.circle(image, (x, y), size//4, (255, 255, 255), -1)
        
        # Tia sáng
        for i in range(0, 360, 45):
            end_x = int(x + size * math.cos(math.radians(i)))
            end_y = int(y + size * math.sin(math.radians(i)))
            cv2.line(image, (x, y), (end_x, end_y), 
                    (glow_intensity//2, 0, glow_intensity//2), 1)
    
    def update_rainbow(self, particle, image, w, h):
        """Cập nhật cầu vồng"""
        particle['x'] += particle['speed']
        
        arc_y = particle['y'] + int(50 * math.sin((particle['x'] + particle['arc_offset']) * 0.01))
        cv2.circle(image, (int(particle['x']), arc_y), 8, particle['color'], -1)
        
        return particle['x'] <= w + 50
    
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
    
    # ===== ĐỘNG VẬT MA THUẬT =====
    def update_dragon(self, particle, image, w, h):
        """Cập nhật rồng lửa"""
        particle['x'] += particle['speed']
        particle['wing_beat'] += 0.2
        
        # Di chuyển theo target_y
        if abs(particle['y'] - particle['target_y']) > 5:
            particle['y'] += 1 if particle['target_y'] > particle['y'] else -1
        
        # Vẽ rồng
        self.draw_dragon(image, (int(particle['x']), int(particle['y'])), 
                        particle['size'], particle['wing_beat'])
        
        # Thêm flame trail
        particle['flame_trail'].append((int(particle['x']), int(particle['y'])))
        if len(particle['flame_trail']) > 10:
            particle['flame_trail'].pop(0)
            
        for i, (fx, fy) in enumerate(particle['flame_trail']):
            intensity = i / len(particle['flame_trail'])
            cv2.circle(image, (fx, fy), int(5 * intensity), (0, int(100*intensity), int(255*intensity)), -1)
        
        return particle['x'] <= w + 100
    
    def update_unicorn(self, particle, image, w, h):
        """Cập nhật kỳ lân"""
        particle['y'] -= particle['speed']
        particle['horn_glow'] += 0.1
        
        # Vẽ kỳ lân
        self.draw_unicorn(image, (int(particle['x']), int(particle['y'])), particle['horn_glow'])
        
        # Sparkle trail
        if random.randint(1, 3) == 1:
            particle['sparkle_trail'].append({
                'x': particle['x'] + random.randint(-20, 20),
                'y': particle['y'] + random.randint(10, 30),
                'life': 20
            })
        
        for sparkle in particle['sparkle_trail'][:]:
            sparkle['life'] -= 1
            if sparkle['life'] > 0:
                alpha = sparkle['life'] / 20.0
                cv2.circle(image, (int(sparkle['x']), int(sparkle['y'])), 
                          3, (int(255*alpha), int(255*alpha), 0), -1)
            else:
                particle['sparkle_trail'].remove(sparkle)
        
        return particle['y'] >= -50
    
    def update_phoenix(self, particle, image, w, h):
        """Cập nhật phượng hoàng"""
        # Di chuyển về target
        dx = particle['target_x'] - particle['x']
        dy = particle['target_y'] - particle['y']
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 10:
            particle['x'] += dx * 0.03
            particle['y'] += dy * 0.03
        else:
            particle['target_x'] = random.randint(0, w)
            particle['target_y'] = random.randint(0, h//2)
        
        particle['wing_phase'] += 0.3
        particle['rebirth_timer'] -= 1
        
        # Vẽ phượng hoàng
        self.draw_phoenix(image, (int(particle['x']), int(particle['y'])), particle['wing_phase'])
        
        # Fire trail
        particle['fire_trail'].append((int(particle['x']), int(particle['y'])))
        if len(particle['fire_trail']) > 15:
            particle['fire_trail'].pop(0)
            
        for i, (fx, fy) in enumerate(particle['fire_trail']):
            intensity = i / len(particle['fire_trail'])
            size = int(8 * intensity)
            cv2.circle(image, (fx, fy), size, (0, int(150*intensity), int(255*intensity)), -1)
        
        return particle['rebirth_timer'] > 0
    
    # ===== THIÊN NHIÊN HUYỀN BÍ =====
    def update_lightning(self, particle, image, w, h):
        """Cập nhật tia sét"""
        particle['life'] -= 1
        
        if particle['life'] > 0:
            # Vẽ tia sét chính
            cv2.line(image, (int(particle['x']), int(particle['y'])), 
                    (int(particle['x']) + random.randint(-20, 20), int(particle['end_y'])), 
                    (255, 255, 255), 3)
            
            # Vẽ các nhánh sét
            for _ in range(3):
                branch_x = particle['x'] + random.randint(-30, 30)
                branch_y = random.randint(particle['y'], particle['end_y'])
                cv2.line(image, (int(branch_x), int(branch_y)), 
                        (int(branch_x) + random.randint(-15, 15), int(branch_y) + 20), 
                        (200, 200, 255), 2)
            
            return True
        return False
    
    def update_aurora(self, particle, image, w, h):
        """Cập nhật cực quang"""
        particle['wave_phase'] += 0.1
        
        # Vẽ cực quang như sóng
        points = []
        for i in range(particle['width']):
            x = particle['x'] + i - particle['width']//2
            wave_offset = int(20 * math.sin((i + particle['wave_phase']) * 0.1))
            y = particle['y'] + wave_offset
            points.append([int(x), int(y)])
        
        if len(points) > 2:
            points_array = np.array(points, np.int32)
            cv2.polylines(image, [points_array], False, particle['color'], 8)
            
            # Hiệu ứng mờ
            for i in range(3):
                offset_points = [[p[0], p[1] + i*3] for p in points]
                offset_array = np.array(offset_points, np.int32)
                alpha_color = tuple(int(c * (0.7 - i*0.2)) for c in particle['color'])
                cv2.polylines(image, [offset_array], False, alpha_color, 5)
        
        return True  # Aurora tồn tại lâu
    
    def update_meteor(self, particle, image, w, h):
        """Cập nhật sao băng"""
        particle['x'] += particle['speed_x']
        particle['y'] += particle['speed_y']
        
        # Thêm trail
        particle['trail'].append((int(particle['x']), int(particle['y'])))
        if len(particle['trail']) > 8:
            particle['trail'].pop(0)
        
        # Vẽ trail
        for i, (tx, ty) in enumerate(particle['trail']):
            intensity = i / len(particle['trail'])
            size = int(particle['size'] * intensity)
            if size > 0:
                cv2.circle(image, (tx, ty), size, (0, int(150*intensity), int(255*intensity)), -1)
        
        # Vẽ meteor chính
        cv2.circle(image, (int(particle['x']), int(particle['y'])), 
                  particle['size'], (255, 255, 255), -1)
        
        return particle['x'] >= -50 and particle['x'] <= w + 50 and particle['y'] <= h + 50
    
    def update_galaxy(self, particle, image, w, h):
        """Cập nhật xoáy thiên hà"""
        particle['angle'] += particle['speed']
        
        # Tính toán vị trí xoáy
        x = particle['center_x'] + particle['radius'] * math.cos(particle['angle'])
        y = particle['center_y'] + particle['radius'] * math.sin(particle['angle'])
        
        cv2.circle(image, (int(x), int(y)), 3, particle['color'], -1)
        
        # Giảm dần radius để tạo hiệu ứng hút vào
        particle['radius'] *= 0.999
        
        return particle['radius'] > 10
    
    # ===== PHÉP THUẬT CỔ ĐẠI =====
    def update_crystal(self, particle, image, w, h):
        """Cập nhật pha lê"""
        particle['y'] -= particle['speed']
        particle['rotation'] += particle['spin_speed']
        particle['glow_phase'] += 0.1
        
        glow_intensity = int(100 + 155 * abs(math.sin(particle['glow_phase'])))
        
        # Vẽ pha lê
        self.draw_crystal(image, (int(particle['x']), int(particle['y'])), 
                         particle['size'], particle['rotation'], glow_intensity)
        
        return particle['y'] >= -50
    
    def update_rune(self, particle, image, w, h):
        """Cập nhật rune"""
        particle['life'] -= 1
        particle['glow_intensity'] += particle['pulse_speed']
        
        if particle['life'] > 0:
            alpha = particle['life'] / 200.0
            glow = int(255 * abs(math.sin(particle['glow_intensity'])) * alpha)
            
            # Vẽ rune với font đặc biệt
            cv2.putText(image, particle['symbol'], 
                       (int(particle['x']), int(particle['y'])), 
                       cv2.FONT_HERSHEY_COMPLEX, 2, (glow, glow, 255), 3)
            
            return True
        return False
    
    def update_portal(self, particle, image, w, h):
        """Cập nhật cổng thời gian"""
        particle['life'] -= 1
        particle['rotation'] += 5
        
        if particle['life'] > 0:
            # Mở rộng portal
            if particle['radius'] < particle['max_radius']:
                particle['radius'] += 2
            
            # Vẽ vòng tròn xoáy
            for i in range(5):
                radius = particle['radius'] - i * 10
                if radius > 0:
                    intensity = (5 - i) / 5.0
                    color = (int(255*intensity), 0, int(255*intensity))
                    cv2.circle(image, (int(particle['x']), int(particle['y'])), 
                              int(radius), color, 2)
            
            # Particles bên trong portal
            if random.randint(1, 3) == 1:
                angle = random.uniform(0, math.pi * 2)
                r = random.randint(0, particle['radius'])
                px = particle['x'] + r * math.cos(angle)
                py = particle['y'] + r * math.sin(angle)
                particle['particles_inside'].append({
                    'x': px, 'y': py, 'life': 20
                })
            
            for p in particle['particles_inside'][:]:
                p['life'] -= 1
                if p['life'] > 0:
                    cv2.circle(image, (int(p['x']), int(p['y'])), 2, (255, 255, 0), -1)
                else:
                    particle['particles_inside'].remove(p)
            
            return True
        return False
    
    def update_spell(self, particle, image, w, h):
        """Cập nhật bùa phép"""
        # Di chuyển về target
        dx = particle['target_x'] - particle['x']
        dy = particle['target_y'] - particle['y']
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 5:
            particle['x'] += dx * 0.1
            particle['y'] += dy * 0.1
        else:
            particle['target_x'] = random.randint(0, w)
            particle['target_y'] = random.randint(0, h)
        
        # Trail ma thuật
        particle['trail'].append((int(particle['x']), int(particle['y'])))
        if len(particle['trail']) > 10:
            particle['trail'].pop(0)
        
        for i, (tx, ty) in enumerate(particle['trail']):
            intensity = i / len(particle['trail'])
            cv2.circle(image, (tx, ty), int(3 * intensity), 
                      (int(255*intensity), 0, int(255*intensity)), -1)
        
        # Sparkles
        if random.randint(1, 2) == 1:
            particle['sparkles'].append({
                'x': particle['x'] + random.randint(-10, 10),
                'y': particle['y'] + random.randint(-10, 10),
                'life': 15
            })
        
        for s in particle['sparkles'][:]:
            s['life'] -= 1
            if s['life'] > 0:
                alpha = s['life'] / 15.0
                cv2.circle(image, (int(s['x']), int(s['y'])), 2, 
                          (int(255*alpha), int(255*alpha), 0), -1)
            else:
                particle['sparkles'].remove(s)
        
        return True
    
    def update_energy(self, particle, image, w, h):
        """Cập nhật năng lượng ma thuật"""
        particle['x'] += particle['speed_x']
        particle['y'] += particle['speed_y']
        particle['life'] -= 1
        
        if particle['life'] > 0:
            alpha = particle['life'] / 80.0
            intensity = int(255 * particle['intensity'] * alpha)
            
            cv2.circle(image, (int(particle['x']), int(particle['y'])), 
                      5, (intensity, 0, intensity), -1)
            
            # Tia sáng
            for angle in [0, 90, 180, 270]:
                end_x = int(particle['x'] + 15 * math.cos(math.radians(angle)))
                end_y = int(particle['y'] + 15 * math.sin(math.radians(angle)))
                cv2.line(image, (int(particle['x']), int(particle['y'])), 
                        (end_x, end_y), (intensity//2, 0, intensity//2), 1)
            
            return True
        return False
    
    # ===== VŨ TRỤ BẤT TẬN =====
    def update_planet(self, particle, image, w, h):
        """Cập nhật hành tinh"""
        particle['angle'] += particle['orbit_speed']
        
        # Tính vị trí quỹ đạo
        particle['x'] = particle['orbit_center_x'] + particle['orbit_radius'] * math.cos(particle['angle'])
        particle['y'] = particle['orbit_center_y'] + particle['orbit_radius'] * math.sin(particle['angle'])
        
        # Vẽ hành tinh
        cv2.circle(image, (int(particle['x']), int(particle['y'])), 
                  particle['size'], particle['color'], -1)
        
        # Vẽ quỹ đạo mờ
        if random.randint(1, 10) == 1:
            cv2.circle(image, (particle['orbit_center_x'], particle['orbit_center_y']), 
                      particle['orbit_radius'], (50, 50, 50), 1)
        
        return True
    
    def update_nebula(self, particle, image, w, h):
        """Cập nhật tinh vân"""
        particle['x'] += particle['drift_x']
        particle['y'] += particle['drift_y']
        
        # Vẽ tinh vân với hiệu ứng mờ
        overlay = image.copy()
        cv2.circle(overlay, (int(particle['x']), int(particle['y'])), 
                  particle['size'], particle['color'], -1)
        cv2.addWeighted(image, 1 - particle['alpha'], overlay, particle['alpha'], 0, image)
        
        return particle['x'] >= -100 and particle['x'] <= w + 100
    
    def update_blackhole(self, particle, image, w, h):
        """Cập nhật hố đen"""
        particle['rotation'] += 5
        particle['life'] -= 1
        
        if particle['life'] > 0:
            # Vẽ event horizon
            cv2.circle(image, (int(particle['x']), int(particle['y'])), 
                      particle['event_horizon'], (0, 0, 0), -1)
            
            # Vẽ vùng hút
            for i in range(3):
                radius = particle['event_horizon'] + i * 20
                intensity = 100 - i * 30
                cv2.circle(image, (int(particle['x']), int(particle['y'])), 
                          radius, (intensity, intensity, 0), 2)
            
            # Tạo matter spirals
            if random.randint(1, 5) == 1:
                angle = random.uniform(0, math.pi * 2)
                spiral_r = random.randint(particle['event_horizon'], particle['max_pull_radius'])
                spiral_x = particle['x'] + spiral_r * math.cos(angle)
                spiral_y = particle['y'] + spiral_r * math.sin(angle)
                particle['matter_spirals'].append({
                    'x': spiral_x, 'y': spiral_y, 'angle': angle, 'radius': spiral_r
                })
            
            # Cập nhật matter spirals
            for spiral in particle['matter_spirals'][:]:
                spiral['radius'] -= 2
                spiral['angle'] += 0.1
                spiral['x'] = particle['x'] + spiral['radius'] * math.cos(spiral['angle'])
                spiral['y'] = particle['y'] + spiral['radius'] * math.sin(spiral['angle'])
                
                if spiral['radius'] > particle['event_horizon']:
                    cv2.circle(image, (int(spiral['x']), int(spiral['y'])), 3, (255, 100, 0), -1)
                else:
                    particle['matter_spirals'].remove(spiral)
            
            return True
        return False
    
    def update_constellation(self, particle, image, w, h):
        """Cập nhật chòm sao"""
        particle['life'] -= 1
        particle['twinkle_phase'] += 0.2
        
        if particle['life'] > 0:
            alpha = particle['life'] / 300.0
            twinkle = int(100 + 155 * abs(math.sin(particle['twinkle_phase'])) * alpha)
            
            # Vẽ các ngôi sao
            for i, (sx, sy) in enumerate(particle['stars']):
                cv2.circle(image, (sx, sy), 4, (twinkle, twinkle, 0), -1)
                
                # Vẽ tia sáng
                for angle in [0, 45, 90, 135]:
                    end_x = int(sx + 12 * math.cos(math.radians(angle)))
                    end_y = int(sy + 12 * math.sin(math.radians(angle)))
                    cv2.line(image, (sx, sy), (end_x, end_y), (twinkle//2, twinkle//2, 0), 1)
            
            # Vẽ đường kết nối giữa các sao
            for i in range(len(particle['stars']) - 1):
                cv2.line(image, particle['stars'][i], particle['stars'][i+1], 
                        (twinkle//3, twinkle//3, 0), 1)
            
            return True
        return False
    
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