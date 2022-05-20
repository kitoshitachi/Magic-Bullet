class SpriteAnimation():
	def __init__(self, target, images, animation_speed=60, loop=True):
		'''
		make the sprite has Animation

		parameter target: the object have animation
		parameter images: images of animation
		parameter animation_speed: animated motion speed
		parameter loop: given True or False to loop the animation
		'''
		self._images = images
		self._target = target
		self._animation_speed = animation_speed
		self.loop = loop

		self._current_frame = 0
		self._ended = False

	def update(self, delta_time):
		'''
		update the animation at this delta_time
		'''
		self._current_frame += self.animation_speed * delta_time

		length = len(self._images)
		if self.current_frame >= length:
			if self.loop:
				self._current_frame -= (self.current_frame // length) * length
			else:
				self._current_frame = length - 1
				self._ended = True

		self._target.image = self._images[self.current_frame]

	@property
	def current_frame(self):
		'''return current frame'''
		return int(self._current_frame)

	@property
	def is_ended(self):
		'''return True if animation is ended else False'''
		return self._ended 

	def set_images(self, images, reset=True):
		'''
		paramater images: images of animation
		paramater reset: default = True , this will be reset animation to new animation
		'''
		self._images = images
		if reset:
			self._current_frame = 0

	@property
	def animation_speed(self):
		'''animated motion speed'''
		return self._animation_speed

	@animation_speed.setter
	def animation_speed(self, speed):
		self._animation_speed = speed
	
