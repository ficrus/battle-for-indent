from math import *
from abc import ABC, abstractmethod
from decorator import *
import arcade


class Part:
    def __init__(self, sprite, scale, mirrored=False):
        if mirrored:
            self.sprite = arcade.Sprite(sprite, scale)
            self.sprite._texture = arcade.load_texture(sprite, mirrored=True)
        else:
            self.sprite = arcade.Sprite(sprite, scale)
        self.points_of_joint = dict()
        self.clockwise_rotation = False


class TurningPart(Part):
    def __init__(self, sprite, scale, mirrored=False, turning_speed=0.0,
                 turning_speed_during_attack=0.0,
                 left_border_angle=0.0, right_border_angle=0.0):
        super().__init__(sprite, scale, mirrored)
        self.turning_speed = turning_speed
        self.turning_speed_during_attack = turning_speed_during_attack
        self.lb = left_border_angle
        self.rb = right_border_angle


class Point:
    def __init__(self):
        self.x = 0
        self.y = 0


def rotate_point(cx, cy, angle, p):
    s = sin(angle)
    c = cos(angle)
    p.x -= cx
    p.y -= cy
    x_new = p.x * c - p.y * s
    y_new = p.x * s + p.y * c
    p.x = x_new + cx
    p.y = y_new + cy
    return p


class ObjectSprite(ABC):

    @abstractmethod
    def __init__(self, scale=1):
        self.object = arcade.SpriteList()
        self.scale = scale
        self.object_parts = []
        self.center_x = 0
        self.center_y = 0

    def setup(self, x, y):
        for part in self.object_parts:
            self.object.append(part.sprite)

        self.change_x(x)
        self.change_y(y)
        self.change_scale(self.scale)

    def change_x(self, x):
        self.center_x += x
        for part in self.object_parts:
            part.sprite.center_x += x
            for point in part.points_of_joint:
                part.points_of_joint[point][0] += x

    def change_y(self, y):
        self.center_y += y
        for part in self.object_parts:
            part.sprite.center_y += y
            for point in part.points_of_joint:
                part.points_of_joint[point][1] += y

    def change_scale(self, scale):
        for part in self.object_parts:
            part.sprite.center_x = (part.sprite.center_x - self.center_x) * scale + self.center_x
            part.sprite.center_y = (part.sprite.center_y - self.center_y) * scale + self.center_y
            for point in part.points_of_joint:
                part.points_of_joint[point][0] = (part.points_of_joint[point][0] - self.center_x) * scale + \
                                                 self.center_x
                part.points_of_joint[point][1] = (part.points_of_joint[point][1] - self.center_y) * scale + \
                                                 self.center_y

    def on_draw(self):
        self.object.draw()

    @abstractmethod
    def update(self, delta_time):
        pass


def change_angle(angle: int, obj: Part, relobj=None):
    point = [obj.sprite.center_x, obj.sprite.center_y]
    if relobj is not None:
        point = relobj.points_of_joint[obj]
    obj.sprite.angle += angle
    phi = radians(angle)
    p = Point()
    p.x = obj.sprite.center_x
    p.y = obj.sprite.center_y
    new_center = rotate_point(point[0], point[1], phi, p)
    obj.sprite.center_x = new_center.x
    obj.sprite.center_y = new_center.y
    for pt in obj.points_of_joint:
        x = obj.points_of_joint[pt][0]
        y = obj.points_of_joint[pt][1]
        p.x = x
        p.y = y
        new_center = rotate_point(point[0], point[1], phi, p)
        obj.points_of_joint[pt][0] = new_center.x
        obj.points_of_joint[pt][1] = new_center.y
        pt.sprite.center_x += (new_center.x - x)
        pt.sprite.center_y += (new_center.y - y)


class UnitSprite(ObjectSprite):
    @abstractmethod
    def __init__(self, scale=1, move_speed=0):
        super().__init__(scale=scale)
        self.move_speed = move_speed
        self.player_body = None
        self.player_left_leg = None
        self.player_right_leg = None
        self.player_left_arm = None
        self.player_right_arm = None
        self.player_head = None

        self.attack = False
        self.start_attack = False
        self.move_right = False
        self.move_left = False
        self.movement_class = MovementSprite()
        self.attack_class = AttackSprite()

    def set_speed_decorator(self, decorator, alpha):
        self.movement_class = decorator(self.movement_class, alpha)
        self.attack_class = decorator(self.attack_class, alpha)

    @abstractmethod
    def setup(self, x, y):
        super().setup(x, y)

        self.center_x = self.player_body.sprite.center_x
        self.center_y = self.player_body.sprite.center_y
        self.player_right_arm.clockwise_rotation = True
        self.player_right_leg.clockwise_rotation = True

    def update(self, delta_time):
        if not self.start_attack:
            self.movement_class.act(unit=self, delta_time=delta_time)
        if not self.move_right or self.move_left:
            self.attack_class.act(unit=self, delta_time=delta_time)


class ZombieSprite(UnitSprite):
    def __init__(self, scale=1):
        super().__init__(scale=scale)
        self.player_body = Part("images/zombie/zbody.png", self.scale)
        self.player_left_leg = TurningPart("images/zombie/zleftleg.png", self.scale, turning_speed=2,
                                           left_border_angle=-5, right_border_angle=35)
        self.player_right_leg = TurningPart("images/zombie/zrightleg.png", self.scale, turning_speed=2,
                                            left_border_angle=-35, right_border_angle=5)
        self.player_left_arm = TurningPart("images/zombie/zleftarm.png", self.scale, turning_speed_during_attack=10,
                                           turning_speed=1, left_border_angle=-10,
                                           right_border_angle=10)
        self.player_right_arm = TurningPart("images/zombie/zrightarm.png", self.scale, turning_speed=1,
                                            left_border_angle=-10, right_border_angle=10)
        self.player_head = TurningPart("images/zombie/zhead.png", self.scale, turning_speed=0.5,
                                       left_border_angle=-5, right_border_angle=5)

        # setting the initial coordinates of the points of joint
        self.player_body.points_of_joint[self.player_left_leg] = [-33, -80]
        self.player_body.points_of_joint[self.player_right_leg] = [63, -83]
        self.player_body.points_of_joint[self.player_left_arm] = [-83, 65]
        self.player_body.points_of_joint[self.player_right_arm] = [115, 68]
        self.player_body.points_of_joint[self.player_head] = [18, 122]

        # setting the initial coordinates of the parts of the player
        self.player_body.center_x = 0
        self.player_body.center_y = 0
        self.player_left_leg.sprite.center_x = -95
        self.player_left_leg.sprite.center_y = -200
        self.player_right_leg.sprite.center_x = 125
        self.player_right_leg.sprite.center_y = -200
        self.player_left_arm.sprite.center_x = -170
        self.player_left_arm.sprite.center_y = -25
        self.player_right_arm.sprite.center_x = 180
        self.player_right_arm.sprite.center_y = 0
        self.player_head.sprite.center_x = 2
        self.player_head.sprite.center_y = 223

    def setup(self, x, y):
        self.object_parts.append(self.player_left_arm)
        self.object_parts.append(self.player_right_arm)
        self.object_parts.append(self.player_left_leg)
        self.object_parts.append(self.player_right_leg)
        self.object_parts.append(self.player_body)
        self.object_parts.append(self.player_head)

        super().setup(x, y)
        change_angle(15, self.player_left_leg, self.player_body)
        change_angle(-15, self.player_right_leg, self.player_body)


class KnightSprite(UnitSprite):
    def __init__(self, scale=1):
        super().__init__(scale=scale)
        self.player_body = Part("images/knight/body.png", self.scale)
        self.player_left_leg = TurningPart("images/knight/right_leg_stand.png",
                                           self.scale, turning_speed=4, left_border_angle=-50,
                                           right_border_angle=-10)
        self.player_right_leg = TurningPart("images/knight/right_leg_stand.png",
                                            self.scale, turning_speed=4, left_border_angle=-20,
                                            right_border_angle=20)
        self.player_left_arm = TurningPart("images/knight/left_arm.png",
                                           self.scale, turning_speed_during_attack=8, turning_speed=2,
                                           left_border_angle=-10, right_border_angle=10)
        self.player_right_arm = TurningPart("images/knight/right_arm.png",
                                            self.scale, turning_speed=2, left_border_angle=-10,
                                            right_border_angle=10)
        self.player_head = TurningPart("images/knight/head.png",
                                       self.scale, turning_speed=1, left_border_angle=-5,
                                       right_border_angle=5)
        self.player_shield = Part("images/knight/shield.png", self.scale)
        self.player_spear = Part("images/knight/spear_with_arm.png", self.scale)

        # setting the initial coordinates of the points of joint
        self.player_body.points_of_joint[self.player_left_leg] = [-18, -70]
        self.player_body.points_of_joint[self.player_right_leg] = [46, -68]
        self.player_body.points_of_joint[self.player_left_arm] = [-65, 51]
        self.player_body.points_of_joint[self.player_right_arm] = [83, 47]
        self.player_body.points_of_joint[self.player_head] = [9, 89]
        self.player_left_arm.points_of_joint[self.player_spear] = [-115, -37]
        self.player_right_arm.points_of_joint[self.player_shield] = [175, -12]

        # setting the initial coordinates of the parts of the player
        self.player_body.center_x = 0
        self.player_body.center_y = 0
        self.player_left_leg.sprite.center_x = 21
        self.player_left_leg.sprite.center_y = -144
        self.player_right_leg.sprite.center_x = 85
        self.player_right_leg.sprite.center_y = -142
        self.player_left_arm.sprite.center_x = -98
        self.player_left_arm.sprite.center_y = 10
        self.player_right_arm.sprite.center_x = 135
        self.player_right_arm.sprite.center_y = 5
        self.player_head.sprite.center_x = 2
        self.player_head.sprite.center_y = 223
        self.player_shield.sprite.center_x = 186
        self.player_shield.sprite.center_y = -106
        self.player_spear.sprite.center_x = 32
        self.player_spear.sprite.center_y = -2

    def setup(self, x, y):
        self.object_parts.append(self.player_right_leg)
        self.object_parts.append(self.player_left_arm)
        self.object_parts.append(self.player_right_arm)
        self.object_parts.append(self.player_body)
        self.object_parts.append(self.player_left_leg)
        self.object_parts.append(self.player_head)
        self.object_parts.append(self.player_spear)
        self.object_parts.append(self.player_shield)

        super().setup(x, y)

        change_angle(-30, self.player_left_leg, self.player_body)


def turning_movement(obj: Part, relobj: Part, delta_time, turning_speed, lb, rb):
    if obj.clockwise_rotation:

        if obj.sprite.angle > lb:
            change_angle(-turning_speed * delta_time, obj, relobj)
        else:
            obj.clockwise_rotation = False

    else:

        if obj.sprite.angle < rb:
            change_angle(turning_speed * delta_time, obj, relobj)
        else:
            obj.clockwise_rotation = True
