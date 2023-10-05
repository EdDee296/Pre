from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

thickness = 0.0021000028848648074
length = 0.006454188346862793
horizontal_x = 0.006270825766026974
horizontal_y = 0
vertical_x = 0
vertical_y = 0.006270825766026974

class Player(Entity):
    def __init__(self, **kwargs):
        self.controller = FirstPersonController(**kwargs)
        self.controller.on_disable()
        super().__init__(parent=self.controller)
        self.right_horizontal_line = Entity(
            parent=camera.ui,
            model='quad',
            scale=(thickness, length),
            color=color.red,
            position=(horizontal_x, horizontal_y),
            rotation=(0, 0, 90)
        )
        self.left_horizontal_line = Entity(parent=camera.ui,
            model='quad',
            scale=(thickness, length),
            color=color.red,
            position=(-horizontal_x, horizontal_y),
            rotation=(0, 0, 90)
        )

        self.upper_vertical_line = Entity(parent=camera.ui,
            model='quad',
            scale=(thickness, length),
            color=color.red,
            position=(vertical_x, vertical_y)
        )

        self.lower_vertical_line = Entity(parent=camera.ui,
            model='quad',
            scale=(thickness, length),
            color=color.red,
            position=(vertical_x, -vertical_y)
        )
        self.line = [self.upper_vertical_line, self.lower_vertical_line,
                     self.left_horizontal_line, self.right_horizontal_line]
        
        self.thickness_slider = Slider(0.001, 0.1, default=0.0021000028848648074, on_value_changed=self.thick_slider,enabled = False)
        self.length_slider = Slider(0.001, 0.1, default=0.006454188346862793, on_value_changed=self.length_sli,enabled = False)
        self.gap_slider = Slider(0.001, 0.1, default=0.006270825766026974, on_value_changed=self.gap,enabled = False)
        self.sli = [self.thickness_slider,self.length_slider,self.gap_slider]

        self.gun = Entity(
            model='assets//gun',
            scale=2,
            position=(0.4, -0.4, 0.8),
            rotation_y=70,
            parent=camera,
            enabled=True
        )

        self.scope = Entity(
            model='assets//gun',
            scale=2,
            rotation = (0,90,0),
            position = (0,-0.2,0),
            parent=camera,
            enabled = False
        )

    def recoil(self):
        if self.gun.enabled:
            self.gun.rotation_z -= 20
        else:
            self.scope.rotation_z -= 10

    def input(self,key):
        if key == 'left mouse down':
            if self.gun.enabled:
                self.gun.rotation_z += 20
            else:
                self.scope.rotation_z += 10
            invoke(self.recoil, delay=0.2)
        if key == 'right mouse down':
            if self.gun.enabled:
                self.gun.disable()
                self.scope.enable()
                camera.position = (0,0,2)
            else:
                self.scope.disable()
                self.gun.enable()
                camera.position = (0,0,0)
        
    def thick_slider(self):
            for item in self.line:
                item.scale_x = self.thickness_slider.value

    def length_sli(self):
            for item in self.line:
                item.scale_y = self.length_slider.value

    def gap(self):
            self.right_horizontal_line.x = self.gap_slider.value
            self.left_horizontal_line.x = -self.gap_slider.value
            self.upper_vertical_line.y = self.gap_slider.value
            self.lower_vertical_line.y = -self.gap_slider.value