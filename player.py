import pygame
from settings import *
from support import import_folder
from entity import Entity

class Player(Entity):
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack,create_magic):
        super().__init__(groups)

        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-26)

        # Movement
        self.attack = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites

        # weapon
        self.create_attack = create_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.destroy_attack = destroy_attack
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.duration_cooldown = 200

        # magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None


        # Graphic setup
        self.import_player_assets()
        self.status = 'down'

        # Stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 5}
        self.health = self.stats['health'] * 0.5
        self.energy = self.stats['energy'] * 0.8
        self.speed = self.stats['speed']
        self.exp = 100

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

    def import_player_assets(self):
        character_path = 'graphics/player/'
        self.animation = {'up': [],'down': [],'left': [],'right': [],
			'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
			'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}

        for animation in self.animation.keys():
            full_path = character_path + animation
            self.animation[animation] = import_folder(full_path)

    def intput(self):
        # Move input
        keys = pygame.key.get_pressed()

        if not self.attack:
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # Attack input
            if keys[pygame.K_SPACE]:
                self.attack = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            # Magic input
            if keys[pygame.K_LSHIFT]:
                self.magic = True
                self.magic_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength']
                cost = list(magic_data.values())[self.magic_index]['cost']

                self.create_magic(style,strength,cost)

            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                if self.weapon_index >= len(list(weapon_data.keys())) - 1:
                    self.weapon_index = 0
                else:
                    self.weapon_index += 1
                self.weapon = list(weapon_data.keys())[self.weapon_index]

            if keys[pygame.K_r] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                if self.magic_index >= len(list(magic_data.keys())) - 1:
                    self.magic_index = 0
                else:
                    self.magic_index += 1
                self.magic = list(magic_data.keys())[self.magic_index]

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attack:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack','')

    def cooldown(self):
            current_time = pygame.time.get_ticks()
            if self.attack:
                if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                    self.attack = False
                    self.destroy_attack()

            if not self.can_switch_weapon:
                if current_time - self.weapon_switch_time >= self.duration_cooldown:
                    self.can_switch_weapon = True

            if not self.can_switch_magic:
                if current_time - self.magic_switch_time >= self.duration_cooldown:
                    self.can_switch_magic = True

            if not self.vulnerable:
                if current_time - self.hurt_time >= self.invulnerability_duration:
                    self.vulnerable = True

    def animate(self):
        animation = self.animation[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(225)

    def get_full_weapon_damage(self):
        base_damege = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damege + weapon_damage

    def update(self):
        self.intput()
        self.cooldown()
        self.get_status()
        self.animate()
        self.move(self.speed)
