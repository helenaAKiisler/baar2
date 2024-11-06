self.x_vel = 0
self.y_vel = 0
self.mask = None
self.direction = "left"
self.animation_count = 0


def move(self, dx, dy):
    self.rect.x += dx
    self.rect.y += dy


def move_left(self, vel):
    self.x_vel = -vel
    if self.direction != "left":
        self.direction = "left"
        self.animation_count = 0


def move_right(self, vel):
    self.x_vel = vel
    if self.direction != "right":
        self.direction = "right"
        self.animation_count = 0


def move_down(self, vel):
    self.y_vel = -vel


def move_up(self, vel):
    self.y_vel = vel


def loop(self, fps):
    self.move(self.x_vel, self.y_vel)