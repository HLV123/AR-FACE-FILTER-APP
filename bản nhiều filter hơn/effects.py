import cv2
import numpy as np
import random
import math
from particles import ParticleRenderer

class EffectsManager:
    def __init__(self):
        self.effects = {
            # Cơ bản
            'snow': False,
            'cherry_blossom': False,
            'hearts': False,
            'stars': False,
            'rainbow': False,
            
            # Động vật ma thuật
            'butterflies': False,
            'dragons': False,
            'unicorns': False,
            'phoenixes': False,
            
            # Thiên nhiên huyền bí
            'fire': False,
            'lightning': False,
            'aurora': False,
            'meteor': False,
            'galaxy': False,
            
            # Phép thuật cổ đại
            'crystals': False,
            'runes': False,
            'portals': False,
            'spells': False,
            'energy': False,
            
            # Vũ trụ bất tận
            'planets': False,
            'nebula': False,
            'blackhole': False,
            'constellation': False
        }
        
        self.particles = []
        self.frame_count = 0
        self.animation_offset = 0
        self.renderer = ParticleRenderer()
    
    def toggle_effect(self, effect_name):
        """Bật/tắt hiệu ứng"""
        self.effects[effect_name] = not self.effects[effect_name]
        self.particles = []
    
    def reset_all(self):
        """Reset tất cả hiệu ứng"""
        for effect in self.effects:
            self.effects[effect] = False
        self.particles = []
    
    def update_particles(self, image):
        """Cập nhật và vẽ particles"""
        h, w, _ = image.shape
        self.animation_offset += 1
        
        # Thêm particles mới
        if self.frame_count % 2 == 0:
            self._add_new_particles(w, h)
        
        # Cập nhật và vẽ particles
        for particle in self.particles[:]:
            if not self._update_particle(particle, image, w, h):
                self.particles.remove(particle)
    
    def _add_new_particles(self, w, h):
        """Thêm particles mới"""
        # CƠ BẢN
        if self.effects['snow']:
            for _ in range(3):
                self.particles.append({
                    'type': 'snow',
                    'x': random.randint(-50, w + 50),
                    'y': random.randint(-50, -10),
                    'speed': random.randint(1, 4),
                    'size': random.randint(3, 8),
                    'drift': random.uniform(-1, 1)
                })
        
        if self.effects['cherry_blossom']:
            for _ in range(2):
                self.particles.append({
                    'type': 'cherry',
                    'x': random.randint(-30, w + 30),
                    'y': random.randint(-30, -10),
                    'speed': random.randint(1, 3),
                    'size': random.randint(4, 10),
                    'rotation': random.randint(0, 360),
                    'spin_speed': random.uniform(-5, 5)
                })
        
        if self.effects['hearts']:
            for _ in range(2):
                self.particles.append({
                    'type': 'heart',
                    'x': random.randint(0, w),
                    'y': h + random.randint(10, 50),
                    'speed': random.randint(2, 5),
                    'size': random.randint(15, 30),
                    'pulse': random.uniform(0, math.pi)
                })
        
        if self.effects['stars']:
            for _ in range(4):
                self.particles.append({
                    'type': 'star',
                    'x': random.randint(0, w),
                    'y': random.randint(0, h),
                    'speed': random.randint(1, 3),
                    'size': random.randint(2, 6),
                    'twinkle': random.uniform(0, math.pi),
                    'life': random.randint(50, 100)
                })
        
        if self.effects['rainbow']:
            if self.frame_count % 10 == 0:
                for i in range(7):
                    colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), 
                            (0, 0, 255), (75, 0, 130), (148, 0, 211)]
                    self.particles.append({
                        'type': 'rainbow',
                        'x': -50,
                        'y': h//2 + i * 5,
                        'color': colors[i],
                        'speed': 5,
                        'arc_offset': i * 10
                    })
        
        # ĐỘNG VẬT MA THUẬT
        if self.effects['butterflies']:
            if random.randint(1, 20) == 1:
                self.particles.append({
                    'type': 'butterfly',
                    'x': random.randint(-50, w + 50),
                    'y': random.randint(50, h - 50),
                    'target_x': random.randint(0, w),
                    'target_y': random.randint(0, h),
                    'wing_phase': 0,
                    'color': random.choice([(255, 0, 255), (0, 255, 255), (255, 255, 0)])
                })
        
        if self.effects['dragons']:
            if random.randint(1, 40) == 1:
                self.particles.append({
                    'type': 'dragon',
                    'x': -100,
                    'y': random.randint(h//4, 3*h//4),
                    'target_y': random.randint(h//4, 3*h//4),
                    'speed': random.randint(3, 6),
                    'size': random.randint(30, 50),
                    'flame_trail': [],
                    'wing_beat': 0
                })
        
        if self.effects['unicorns']:
            if random.randint(1, 60) == 1:
                self.particles.append({
                    'type': 'unicorn',
                    'x': random.randint(0, w),
                    'y': h + 20,
                    'speed': random.randint(2, 4),
                    'horn_glow': 0,
                    'sparkle_trail': []
                })
        
        if self.effects['phoenixes']:
            if random.randint(1, 50) == 1:
                self.particles.append({
                    'type': 'phoenix',
                    'x': random.randint(-50, w + 50),
                    'y': random.randint(h//2, h),
                    'target_x': random.randint(0, w),
                    'target_y': random.randint(0, h//2),
                    'fire_trail': [],
                    'wing_phase': 0,
                    'rebirth_timer': random.randint(200, 400)
                })
        
        # THIÊN NHIÊN HUYỀN BÍ
        if self.effects['fire']:
            for _ in range(5):
                self.particles.append({
                    'type': 'fire',
                    'x': random.randint(0, w),
                    'y': h + random.randint(0, 20),
                    'speed': random.randint(3, 7),
                    'size': random.randint(8, 20),
                    'intensity': random.uniform(0.5, 1.0),
                    'life': random.randint(30, 60)
                })
        
        if self.effects['lightning']:
            if random.randint(1, 30) == 1:
                self.particles.append({
                    'type': 'lightning',
                    'x': random.randint(0, w),
                    'y': 0,
                    'end_y': h,
                    'branches': [],
                    'life': random.randint(5, 15),
                    'intensity': random.uniform(0.7, 1.0)
                })
        
        if self.effects['aurora']:
            if self.frame_count % 5 == 0:
                for _ in range(2):
                    self.particles.append({
                        'type': 'aurora',
                        'x': random.randint(-50, w + 50),
                        'y': random.randint(0, h//2),
                        'width': random.randint(100, 200),
                        'height': random.randint(50, 150),
                        'wave_phase': random.uniform(0, math.pi * 2),
                        'color': random.choice([(0, 255, 100), (100, 0, 255), (255, 0, 150)])
                    })
        
        if self.effects['meteor']:
            if random.randint(1, 25) == 1:
                self.particles.append({
                    'type': 'meteor',
                    'x': random.randint(-50, w + 50),
                    'y': random.randint(-50, 0),
                    'speed_x': random.randint(-3, 3),
                    'speed_y': random.randint(5, 10),
                    'trail': [],
                    'size': random.randint(3, 8)
                })
        
        if self.effects['galaxy']:
            if self.frame_count % 8 == 0:
                center_x, center_y = w//2, h//2
                for i in range(5):
                    angle = random.uniform(0, math.pi * 2)
                    radius = random.randint(50, 200)
                    self.particles.append({
                        'type': 'galaxy',
                        'center_x': center_x,
                        'center_y': center_y,
                        'angle': angle,
                        'radius': radius,
                        'speed': random.uniform(0.02, 0.05),
                        'color': random.choice([(255, 100, 255), (100, 255, 255), (255, 255, 100)])
                    })
        
        # PHÉP THUẬT CỔ ĐẠI
        if self.effects['crystals']:
            if random.randint(1, 35) == 1:
                self.particles.append({
                    'type': 'crystal',
                    'x': random.randint(0, w),
                    'y': h + 20,
                    'speed': random.randint(1, 3),
                    'size': random.randint(20, 40),
                    'rotation': random.randint(0, 360),
                    'spin_speed': random.uniform(1, 3),
                    'glow_phase': random.uniform(0, math.pi * 2)
                })
        
        if self.effects['runes']:
            if random.randint(1, 40) == 1:
                self.particles.append({
                    'type': 'rune',
                    'x': random.randint(50, w - 50),
                    'y': random.randint(50, h - 50),
                    'symbol': random.choice(['ᚠ', 'ᚢ', 'ᚦ', 'ᚨ', 'ᚱ', 'ᚲ', 'ᚷ', 'ᚹ']),
                    'glow_intensity': 0,
                    'life': random.randint(100, 200),
                    'pulse_speed': random.uniform(0.05, 0.1)
                })
        
        if self.effects['portals']:
            if random.randint(1, 80) == 1:
                self.particles.append({
                    'type': 'portal',
                    'x': random.randint(100, w - 100),
                    'y': random.randint(100, h - 100),
                    'radius': 0,
                    'max_radius': random.randint(50, 100),
                    'rotation': 0,
                    'particles_inside': [],
                    'life': random.randint(150, 300)
                })
        
        if self.effects['spells']:
            for _ in range(2):
                self.particles.append({
                    'type': 'spell',
                    'x': random.randint(0, w),
                    'y': random.randint(0, h),
                    'target_x': random.randint(0, w),
                    'target_y': random.randint(0, h),
                    'trail': [],
                    'sparkles': []
                })
        
        if self.effects['energy']:
            if self.frame_count % 3 == 0:
                for _ in range(3):
                    self.particles.append({
                        'type': 'energy',
                        'x': random.randint(0, w),
                        'y': random.randint(0, h),
                        'speed_x': random.uniform(-2, 2),
                        'speed_y': random.uniform(-2, 2),
                        'life': random.randint(30, 80),
                        'intensity': random.uniform(0.3, 1.0)
                    })
        
        # VŨ TRỤ BẤT TẬN
        if self.effects['planets']:
            if random.randint(1, 100) == 1:
                self.particles.append({
                    'type': 'planet',
                    'x': random.randint(-100, w + 100),
                    'y': random.randint(-100, h + 100),
                    'orbit_center_x': w//2,
                    'orbit_center_y': h//2,
                    'orbit_radius': random.randint(100, 300),
                    'orbit_speed': random.uniform(0.01, 0.03),
                    'angle': random.uniform(0, math.pi * 2),
                    'size': random.randint(15, 35),
                    'color': random.choice([(255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 100)])
                })
        
        if self.effects['nebula']:
            if self.frame_count % 6 == 0:
                for _ in range(4):
                    self.particles.append({
                        'type': 'nebula',
                        'x': random.randint(-50, w + 50),
                        'y': random.randint(-50, h + 50),
                        'size': random.randint(80, 150),
                        'color': random.choice([(255, 0, 100), (100, 0, 255), (0, 255, 150)]),
                        'alpha': random.uniform(0.1, 0.3),
                        'drift_x': random.uniform(-0.5, 0.5),
                        'drift_y': random.uniform(-0.5, 0.5)
                    })
        
        if self.effects['blackhole']:
            if random.randint(1, 200) == 1:
                self.particles.append({
                    'type': 'blackhole',
                    'x': random.randint(w//4, 3*w//4),
                    'y': random.randint(h//4, 3*h//4),
                    'event_horizon': 30,
                    'max_pull_radius': 150,
                    'rotation': 0,
                    'matter_spirals': [],
                    'life': random.randint(200, 400)
                })
        
        if self.effects['constellation']:
            if random.randint(1, 60) == 1:
                # Tạo chòm sao với nhiều ngôi sao kết nối
                stars_count = random.randint(4, 8)
                constellation_stars = []
                center_x = random.randint(100, w - 100)
                center_y = random.randint(100, h - 100)
                
                for i in range(stars_count):
                    angle = (i / stars_count) * math.pi * 2
                    radius = random.randint(30, 80)
                    star_x = center_x + radius * math.cos(angle)
                    star_y = center_y + radius * math.sin(angle)
                    constellation_stars.append((int(star_x), int(star_y)))
                
                self.particles.append({
                    'type': 'constellation',
                    'stars': constellation_stars,
                    'life': random.randint(150, 300),
                    'twinkle_phase': 0
                })
    
    def _update_particle(self, particle, image, w, h):
        """Cập nhật một particle"""
        particle_type = particle['type']
        
        # Cơ bản
        if particle_type == 'snow':
            return self.renderer.update_snow(particle, image, w, h)
        elif particle_type == 'cherry':
            return self.renderer.update_cherry(particle, image, w, h)
        elif particle_type == 'heart':
            return self.renderer.update_heart(particle, image, w, h)
        elif particle_type == 'star':
            return self.renderer.update_star(particle, image, w, h)
        elif particle_type == 'rainbow':
            return self.renderer.update_rainbow(particle, image, w, h)
        
        # Động vật ma thuật
        elif particle_type == 'butterfly':
            return self.renderer.update_butterfly(particle, image, w, h)
        elif particle_type == 'dragon':
            return self.renderer.update_dragon(particle, image, w, h)
        elif particle_type == 'unicorn':
            return self.renderer.update_unicorn(particle, image, w, h)
        elif particle_type == 'phoenix':
            return self.renderer.update_phoenix(particle, image, w, h)
        
        # Thiên nhiên huyền bí
        elif particle_type == 'fire':
            return self.renderer.update_fire(particle, image, w, h)
        elif particle_type == 'lightning':
            return self.renderer.update_lightning(particle, image, w, h)
        elif particle_type == 'aurora':
            return self.renderer.update_aurora(particle, image, w, h)
        elif particle_type == 'meteor':
            return self.renderer.update_meteor(particle, image, w, h)
        elif particle_type == 'galaxy':
            return self.renderer.update_galaxy(particle, image, w, h)
        
        # Phép thuật cổ đại
        elif particle_type == 'crystal':
            return self.renderer.update_crystal(particle, image, w, h)
        elif particle_type == 'rune':
            return self.renderer.update_rune(particle, image, w, h)
        elif particle_type == 'portal':
            return self.renderer.update_portal(particle, image, w, h)
        elif particle_type == 'spell':
            return self.renderer.update_spell(particle, image, w, h)
        elif particle_type == 'energy':
            return self.renderer.update_energy(particle, image, w, h)
        
        # Vũ trụ bất tận
        elif particle_type == 'planet':
            return self.renderer.update_planet(particle, image, w, h)
        elif particle_type == 'nebula':
            return self.renderer.update_nebula(particle, image, w, h)
        elif particle_type == 'blackhole':
            return self.renderer.update_blackhole(particle, image, w, h)
        elif particle_type == 'constellation':
            return self.renderer.update_constellation(particle, image, w, h)
        
        return False
    
    def draw_screen_border(self, image):
        """Vẽ viền màn hình với hiệu ứng"""
        h, w, _ = image.shape
        
        border_intensity = int(128 + 127 * math.sin(self.animation_offset * 0.1))
        border_color = (border_intensity, 100, 255 - border_intensity)
        
        # Viền trên dưới
        cv2.rectangle(image, (0, 0), (w, 5), border_color, -1)
        cv2.rectangle(image, (0, h-5), (w, h), border_color, -1)
        
        # Viền trái phải
        cv2.rectangle(image, (0, 0), (5, h), border_color, -1)
        cv2.rectangle(image, (w-5, 0), (w, h), border_color, -1)
        
        # Góc với hiệu ứng đặc biệt
        corner_size = 20
        for corner in [(0, 0), (w-corner_size, 0), (0, h-corner_size), (w-corner_size, h-corner_size)]:
            cv2.rectangle(image, corner, (corner[0]+corner_size, corner[1]+corner_size), 
                         (255, border_intensity, 0), -1)