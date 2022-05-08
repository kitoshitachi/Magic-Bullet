
from cmath import isclose
from collections import namedtuple
from math import inf, trunc
from re import T
from typing import List

from pygame import Vector2
from settings import COLLISION_DETECTION_RADIUS
from utils import Utils

from game_object import GameObject


Box = namedtuple("Box", "x, y, w, h, vel")
CollisionData = namedtuple("CollisionData", "time, normal, who, other")

# https://www.gamedev.net/tutorials/programming/general-and-gameplay-programming/swept-aabb-collision-detection-and-response-r3084/
class CollisionEngine:

    # Kiểm tra va chạm nhiều object cùng lúc, sắp xếp dựa trên dộ gần với moving_object
    @staticmethod
    def detect_multiple(moving_object: GameObject, others, response = None) -> List[CollisionData]:
        closest_to_moving_object = lambda obj: Vector2(obj.hitbox.center).distance_to(Vector2(moving_object.hitbox.center))
        not_too_far_away = lambda obj: Vector2(obj.hitbox.center).distance_to(Vector2(moving_object.hitbox.center)) < COLLISION_DETECTION_RADIUS
        targets = sorted(filter(not_too_far_away, others), key=closest_to_moving_object)
        return [CollisionEngine.detect(moving_object, target, response) for target in targets]

    @staticmethod
    def detect(moving_object: GameObject, static_object: GameObject, response = None) -> CollisionData:
        mb = CollisionEngine._create_box_from_object(moving_object)
        sb = CollisionEngine._create_box_from_object(static_object)
        bbox = CollisionEngine._get_swept_broadphase_box(mb)

        if CollisionEngine._AABB_check(bbox, sb):
            data = CollisionEngine._swept_AABB(mb, sb, moving_object, static_object)
        else:
            data = CollisionData(1, Vector2(0, 0), moving_object, static_object)

        if response and data.time < 1:
            response(data)

        return data

    @staticmethod
    def _create_box_from_object(object: GameObject):
        return Box(object.hitbox.x, object.hitbox.y, object.hitbox.width, object.hitbox.height, object.vel.copy())

    @staticmethod
    def _get_swept_broadphase_box(b: Box) -> Box:
        r = Utils.round_away_from_zero
        x = b.x if b.vel.x > 0 else b.x + b.vel.x
        y = b.y if b.vel.y > 0 else b.y + b.vel.y
        w = b.w + abs(b.vel.x) 
        h = b.h + abs(b.vel.y) 
        return Box(r(x), r(y), r(w), r(h), Vector2())

    @staticmethod
    def _AABB_check(mb: Box, sb: Box) -> bool:
        return not (mb.x + mb.w <= sb.x or mb.x >= sb.x + sb.w or mb.y + mb.h <= sb.y or mb.y >= sb.y + sb.h)

    @staticmethod
    def _swept_AABB(mb: Box, sb: Box, moving_object, static_object) -> CollisionData:
        
        # find the distance between the objects on the near and far sides
        inv_entry = Vector2()
        inv_exit = Vector2()

        if mb.vel.x > 0:
            inv_entry.x = sb.x - (mb.x + mb.w)
            inv_exit.x = (sb.x + sb.w) - mb.x
        else:
            inv_exit.x = sb.x - (mb.x + mb.w)
            inv_entry.x = (sb.x + sb.w) - mb.x

        if mb.vel.y > 0:
            inv_entry.y = sb.y - (mb.y + mb.h)
            inv_exit.y = (sb.y + sb.h) - mb.y
        else:
            inv_exit.y = sb.y - (mb.y + mb.h)
            inv_entry.y = (sb.y + sb.h) - mb.y

        entry = Vector2()
        exit = Vector2()

        if isclose(mb.vel.x, 0):
            entry.x = -inf
            exit.x = inf
        else:
            entry.x = inv_entry.x / mb.vel.x
            exit.x = inv_exit.x / mb.vel.x

        if isclose(mb.vel.y, 0):
            entry.y = -inf
            exit.y = inf
        else:
            entry.y = inv_entry.y / mb.vel.y
            exit.y = inv_exit.y / mb.vel.y

        # find the earliest/latest times of collisionfloat
        entry_time = max(entry.x, entry.y)
        exit_time = max(exit.x, exit.y)
        
        no_collision = entry_time > exit_time or (entry.x < 0 and entry.y < 0) or entry.x > 1 or entry.y > 1
        if no_collision:
            return CollisionData(1, Vector2(0, 0), moving_object, static_object)

        if entry.x > entry.y:
            if mb.vel.x < 0:
                return CollisionData(entry_time, Vector2(1, 0), moving_object, static_object)
            else:
                return CollisionData(entry_time, Vector2(-1, 0), moving_object, static_object)
        else:
            if mb.vel.y < 0:
                return CollisionData(entry_time, Vector2(0, 1), moving_object, static_object)
            else:
                return CollisionData(entry_time, Vector2(0, -1), moving_object, static_object)

    
class CollisionResponse:
    @staticmethod
    def stop(collision_data: CollisionData):
        time, normal, who, _ = collision_data
        who.vel.x = Utils.round_away_from_zero(who.vel.x * time)
        who.vel.y = Utils.round_away_from_zero(who.vel.y * time)

    @staticmethod
    def slide(collision_data: CollisionData):
        time, normal, who, _ = collision_data
        prev_vel = who.vel.copy()

        CollisionResponse.stop(collision_data)

        remaining_time = 1 - time
        dot_prod = prev_vel.x * normal.y + prev_vel.y * normal.x
        who.vel.x += dot_prod * normal.y * remaining_time
        who.vel.y += dot_prod * normal.x * remaining_time

    @staticmethod
    def deflect(collision_data: CollisionData):
        time, normal, who, _ = collision_data

        remaining_time = 1 - time
        reflected_vel = (who.vel * remaining_time).reflect(normal)
        
        # CollisionResponse.stop(who, collision_data)
        who.vel = reflected_vel

