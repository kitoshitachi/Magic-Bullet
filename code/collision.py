
from cmath import isclose
from math import inf

from pygame import Rect, Vector2
from settings import COLLISION_DETECTION_RADIUS
from utils import Utils

from game_object import GameObject


# https://www.gamedev.net/tutorials/programming/general-and-gameplay-programming/swept-aabb-collision-detection-and-response-r3084/
class CollisionEngine:

    # Kiểm tra va chạm nhiều object cùng lúc, sắp xếp dựa trên dộ gần với moving_object
    @staticmethod
    def detect_multiple(moving_object: GameObject, others, response = None):
        closest_to_moving_object = lambda obj: Vector2(obj.hitbox.center).distance_to(Vector2(moving_object.hitbox.center))
        
        def not_too_far_away(obj): 
            close = Vector2(obj.hitbox.center).distance_to(Vector2(moving_object.hitbox.center)) <= COLLISION_DETECTION_RADIUS
            obj_very_large = obj.hitbox.width > COLLISION_DETECTION_RADIUS or obj.hitbox.height > COLLISION_DETECTION_RADIUS
            return close or obj_very_large 

        targets = sorted(filter(not_too_far_away, others), key=closest_to_moving_object)
        return [CollisionEngine.detect(moving_object, target, response) for target in targets]

    @staticmethod
    def detect(moving_object: GameObject, static_object: GameObject, response = None):
        '''return time, normal, who, other'''
        bbox = CollisionEngine._get_swept_broadphase_box(moving_object)
        if CollisionEngine._AABB_check(bbox, static_object.hitbox.copy()):
            data = CollisionEngine._swept_AABB(moving_object, static_object)
        else:
            data = (1, Vector2(0, 0), moving_object, static_object)

        if response and data[0] < 1:
            response(data)

        return data

    @staticmethod
    def _get_swept_broadphase_box(object:GameObject):
        r = Utils.round_away_from_zero
        new_Box = Rect(0,0,0,0)
        new_Box.left = r(object.hitbox.left if object.vel.x > 0 else object.hitbox.left + object.vel.x)
        new_Box.top = r(object.hitbox.top if object.vel.y > 0 else object.hitbox.top + object.vel.y)
        new_Box.width = r(object.hitbox.width + abs(object.vel.x))
        new_Box.height = r(object.hitbox.height + abs(object.vel.y)) 
        return new_Box.copy()

    @staticmethod
    def _AABB_check(mb: Rect, sb: Rect) -> bool:
        return not (mb.left + mb.width <= sb.left 
                    or mb.left >= sb.left + sb.width 
                    or mb.top + mb.height <= sb.top 
                    or mb.top >= sb.top + sb.height)

    @staticmethod
    def _swept_AABB(moving_object:GameObject, static_object:GameObject):
        '''return time, normal, who, other'''
        cur_mb_vel = moving_object.vel.copy()
        sb = static_object.hitbox.copy()
        mb = moving_object.hitbox.copy()
        # find the distance between the objects on the near and far sides
        inv_entry = Vector2()
        inv_exit = Vector2()

        if cur_mb_vel.x > 0.0:
            inv_entry.x = sb.x - (mb.x + mb.width)
            inv_exit.x = (sb.x + sb.width) - mb.x
        else:
            inv_exit.x = sb.x - (mb.x + mb.width)
            inv_entry.x = (sb.x + sb.width) - mb.x

        if cur_mb_vel.y > 0.0:
            inv_entry.y = sb.y - (mb.y + mb.height)
            inv_exit.y = (sb.y + sb.height) - mb.y
        else:
            inv_exit.y = sb.y - (mb.y + mb.height)
            inv_entry.y = (sb.y + sb.height) - mb.y

        entry = Vector2()
        exit = Vector2()

        if isclose(cur_mb_vel.x, 0):
            entry.x = -inf
            exit.x = inf
        else:
            entry.x = inv_entry.x / cur_mb_vel.x
            exit.x = inv_exit.x / cur_mb_vel.x

        if isclose(cur_mb_vel.y, 0):
            entry.y = -inf
            exit.y = inf
        else:
            entry.y = inv_entry.y / cur_mb_vel.y
            exit.y = inv_exit.y / cur_mb_vel.y

        # find the earliest/latest times of collisionfloat
        entry_time = max(entry.x, entry.y)
        exit_time = max(exit.x, exit.y)
        
        no_collision = entry_time > exit_time or (entry.x < 0 and entry.y < 0) or entry.x > 1 or entry.y > 1
        if no_collision:
            return (1, Vector2(0, 0), moving_object, static_object)

        if entry.x > entry.y:
            if cur_mb_vel.x < 0:
                return (entry_time, Vector2(1, 0), moving_object, static_object)
            else:
                return (entry_time, Vector2(-1, 0), moving_object, static_object)
        else:
            if cur_mb_vel.y < 0:
                return (entry_time, Vector2(0, 1), moving_object, static_object)
            else:
                return (entry_time, Vector2(0, -1), moving_object, static_object)

    
class CollisionResponse:
    @staticmethod
    def stop(collision_data):
        time, normal, who, _ = collision_data
        who.vel.x = Utils.round_away_from_zero(who.vel.x * time)
        who.vel.y = Utils.round_away_from_zero(who.vel.y * time)

    @staticmethod
    def slide(collision_data):
        time, normal, who, _ = collision_data
        prev_vel = who.vel.copy()

        CollisionResponse.stop(collision_data)

        remaining_time = 1 - time
        dot_prod = prev_vel.x * normal.y + prev_vel.y * normal.x
        who.vel.x += dot_prod * normal.y * remaining_time
        who.vel.y += dot_prod * normal.x * remaining_time

    @staticmethod
    def deflect(collision_data):
        time, normal, who, _ = collision_data

        remaining_time = 1 - time
        reflected_vel = (who.vel * remaining_time).reflect(normal)
        
        CollisionResponse.stop(collision_data)
        who.vel = reflected_vel

