from assets import Assets
from sprite_animation import SpriteAnimation
from game_object import GameObject

class SmokeEffect(GameObject):
	FIRE_SFX = Assets.audio
	FIRE_SFX.set_volume(0.4)

	def __init__(self, pos, level):
		'''
		make effect of bullet
		param pos: give pos of bullet
		param level: take group sprite
		'''
		super().__init__(level, [level.group_visible], Assets.smoke_effect[0], pos=pos)
		self._animation = SpriteAnimation(self, Assets.smoke_effect, loop=False)

		SmokeEffect.FIRE_SFX.play();

	def update(self, delta_time):
		'''
		update the animation after deltatime
		param delta_time: FPS
		'''
		super().update(delta_time)
		self._animation.update(delta_time)

		if self._animation.is_ended:
			self.kill()
