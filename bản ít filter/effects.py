import cv2
import numpy as np
import random
import math
from particles import ParticleRenderer

class EffectsManager:
    def __init__(self):
        self.effects = {
            'snow': False,
            'cherry_blossom': False,
            'hearts': False,
            'stars': False,
            'butterflies': False,
            'fire': False,
            'rainbow': False
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
    
    def _update_particle(self, particle, image, w, h):
        """Cập nhật một particle"""
        particle_type = particle['type']
        
        if particle_type == 'snow':
            return self.renderer.update_snow(particle, image, w, h)
        elif particle_type == 'cherry':
            return self.renderer.update_cherry(particle, image, w, h)
        elif particle_type == 'heart':
            return self.renderer.update_heart(particle, image, w, h)
        elif particle_type == 'star':
            return self.renderer.update_star(particle, image, w, h)
        elif particle_type == 'butterfly':
            return self.renderer.update_butterfly(particle, image, w, h)
        elif particle_type == 'fire':
            return self.renderer.update_fire(particle, image, w, h)
        elif particle_type == 'rainbow':
            return self.renderer.update_rainbow(particle, image, w, h)
        
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