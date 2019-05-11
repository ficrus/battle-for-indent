from sprite import *
from abc import abstractmethod


class AbstractSpriteBehaviour:
    def __init__(self, unit: UnitSprite):
        self.unit = unit

    @abstractmethod
    def act(self, delta_time):
        pass


class MovementSprite(AbstractSpriteBehaviour):
    def act(self, delta_time):
        if self.unit.move_left:
            self.unit.change_x(-self.unit.move_speed * delta_time)
        if self.unit.move_right:
            self.unit.change_x(self.unit.move_speed * delta_time)

        turning_movement(self.unit.player_left_leg, self.unit.player_body, delta_time, self.unit.player_left_leg.turning_speed,
                         self.unit.player_left_leg.lb, self.unit.player_left_leg.rb)
        turning_movement(self.unit.player_right_leg, self.unit.player_body, delta_time, self.unit.player_right_leg.turning_speed,
                         self.unit.player_right_leg.lb, self.unit.player_right_leg.rb)
        turning_movement(self.unit.player_left_arm, self.unit.player_body, delta_time, self.unit.player_left_arm.turning_speed,
                         self.unit.player_left_arm.lb, self.unit.player_left_arm.rb)
        turning_movement(self.unit.player_right_arm, self.unit.player_body, delta_time, self.unit.player_right_arm.turning_speed,
                         self.unit.player_right_arm.lb, self.unit.player_right_arm.rb)
        turning_movement(self.unit.player_head, self.unit.player_body, delta_time, self.unit.player_head.turning_speed,
                         self.unit.player_head.lb, self.unit.player_head.rb)


class AttackSprite(AbstractSpriteBehaviour):
    def act(self, delta_time):
        if self.unit.attack:
            self.unit.player_left_arm.clockwise_rotation = False
            self.unit.attack = False
            self.unit.start_attack = True
        if self.unit.start_attack:
            turning_movement(self.unit.player_left_arm, self.unit.player_body, delta_time,
                             self.unit.player_left_arm.turning_speed_during_attack, self.unit.player_left_arm.lb - 1, 50)
            if self.unit.player_left_arm.sprite.angle <= self.unit.player_left_arm.lb - 1:
                self.unit.start_attack = False
                change_angle(1, self.unit.player_left_arm, self.unit.player_body)


class AbstractBehaviourDecorator(AbstractSpriteBehaviour):
    def __init__(self, decoratee):
        self._decoratee = decoratee

    def act(self, sprite: UnitSprite, delta_time):
        self._decoratee.act(sprite, delta_time)


class SpeedDecorator(AbstractBehaviourDecorator):
    def __init__(self, decoratee, alpha):
        super().__init__(decoratee)
        self.alpha = alpha

    def act(self, unit: UnitSprite, delta_time):
        unit.player_left_leg.turning_speed *= self.alpha
        unit.player_right_leg.turning_speed *= self.alpha
        unit.player_left_arm.turning_speed *= self.alpha
        unit.player_right_arm.turning_speed *= self.alpha
        unit.player_head.turning_speed *= self.alpha
        unit.player_left_arm.turning_speed_during_attack *= self.alpha

        AbstractBehaviourDecorator.act(self, unit, delta_time)

        unit.player_left_leg.turning_speed /= self.alpha
        unit.player_right_leg.turning_speed /= self.alpha
        unit.player_left_arm.turning_speed /= self.alpha
        unit.player_right_arm.turning_speed /= self.alpha
        unit.player_head.turning_speed /= self.alpha
        unit.player_left_arm.turning_speed_during_attack /= self.alpha







