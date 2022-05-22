from math import inf,isclose
from pygame import Rect, Vector2
from settings import COLLISION_DETECTION_RADIUS
from utils import Utils
from game_object import GameObject


# https://www.gamedev.net/tutorials/programming/general-and-gameplay-programming/swept-aabb-collision-detection-and-response-r3084/
class CollisionEngine:
    '''class to check collsion'''
    @staticmethod
    def detect_multiple(moving_object: GameObject, others, response = None):
        '''Kiểm tra va chạm nhiều object cùng lúc, sắp xếp dựa trên dộ gần với moving_object
        param moving object: the object is moving
        param other: the sprite of game, can be moving object or static object
        param respone: default is None, stop when collided
                       respone = slide, slide moving object when collide
                       respone = deflect, deflect the sprites when collide
                       
        return  list data when collided
        the data is [time, vector normalize, game object, other]
        '''
        closest_to_moving_object = lambda obj: Vector2(obj.hitbox.center).distance_to(Vector2(moving_object.hitbox.center))
        
        def not_too_far_away(obj): 
            close = Vector2(obj.hitbox.center).distance_to(Vector2(moving_object.hitbox.center)) <= COLLISION_DETECTION_RADIUS
            obj_very_large = obj.hitbox.width > COLLISION_DETECTION_RADIUS or obj.hitbox.height > COLLISION_DETECTION_RADIUS
            return close or obj_very_large 

        targets = sorted(filter(not_too_far_away, others), key=closest_to_moving_object)
        return [CollisionEngine.detect(moving_object, target, response) for target in targets]

    @staticmethod
    def detect(moving_object: GameObject, static_object: GameObject, response = None):
        '''
        kiểm tra va chạm của 1 moving object and static object, sau đó respone và trả về dữ liệu
        return time,vector normalize, who, other'''

        bbox = CollisionEngine._get_swept_broadphase_box(moving_object, static_object)
        if CollisionEngine._AABB_check(bbox, static_object.hitbox.copy()):
            data = CollisionEngine._swept_AABB(moving_object, static_object)
        else:
            data = (1, Vector2(0, 0), moving_object, static_object)

        if response and data[0] < 1:
            response(data)

        return data

    @staticmethod
    def _get_swept_broadphase_box(m_object:GameObject, s_object:GameObject):
        '''quick check but the accuracy isnt 100%
        param m_object: moving object
        param s_object: static object
        '''
        r = Utils.round_away_from_zero
        new_Box = Rect(0,0,0,0)
        new_Box.left = r(m_object.hitbox.left if m_object.vel.x >0 else m_object.hitbox.left + m_object.vel.x - s_object.vel.x)
        new_Box.top = r(m_object.hitbox.top if m_object.vel.y > 0 else m_object.hitbox.top + m_object.vel.y - s_object.vel.y)
        new_Box.width = r(m_object.hitbox.width + abs(m_object.vel.x))
        new_Box.height = r(m_object.hitbox.height + abs(m_object.vel.y)) 
        return new_Box.copy()

    @staticmethod
    def _AABB_check(mb: Rect, sb: Rect):
        '''
        check collide with AABB
        param mb: get rect of moving object
        param sb: get rect of static object
        return True if collided else False
        '''
        return not (mb.left + mb.width <= sb.left 
                    or mb.left >= sb.left + sb.width 
                    or mb.top + mb.height <= sb.top 
                    or mb.top >= sb.top + sb.height)

    @staticmethod
    def _swept_AABB(moving_object:GameObject, static_object:GameObject):
        '''
        param moving object: the object is moving
        param static_object: the object is not moving, but can be moving object

        return time, normal, who, other'''
        cur_mb_vel = moving_object.vel - static_object.vel
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
    '''class respone when collided'''
    @staticmethod
    def stop(collision_data):
        '''
        param collsion_data: data when collide from check sweet AABB
        stop the moving object'''
        time, _, who, _ = collision_data
        who._vel.x = Utils.round_away_from_zero(who.vel.x * time)
        who._vel.y = Utils.round_away_from_zero(who.vel.y * time)

    @staticmethod
    def slide(collision_data):
        '''
        param collsion_data: data when collide from check sweet AABB
        slide the moving object'''
        time, normal, who, _ = collision_data
        prev_vel = who._vel.copy()

        CollisionResponse.stop(collision_data)

        remaining_time = 1 - time
        dot_prod = prev_vel.x * normal.y + prev_vel.y * normal.x
        who._vel.x += dot_prod * normal.y * remaining_time
        who._vel.y += dot_prod * normal.x * remaining_time

    @staticmethod
    def deflect(collision_data):
        '''
        param collsion_data: data when collide from check sweet AABB
        reflect moving object'''
        time, normal, who, _ = collision_data

        remaining_time = 1 - time
        reflected_vel = (who._vel * remaining_time).reflect(normal)
        
        CollisionResponse.stop(collision_data)
        who._vel = reflected_vel

