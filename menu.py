from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import json
import os

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

class Menu(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)
        
        self.mainmenu = Entity(parent=self,
                               enabled=True,
                               model='quad',
                               scale=(2, 2),
                               position=(0, 0), texture='shore')
        self.set = Entity(parent=self,
                          enabled=False,
                          model='quad',
                          scale=(2, 2),
                          position=(0, 0), color = color.gray)
        self.start_button = Button(
            parent=self.mainmenu,
            model='quad',
            text='Start',
            scale=(0.2, 0.1),
            position=(0, 0.1),
            on_click=self.start_game  
        )

        self.setting_button = Button(
            parent=self.mainmenu,
            model='quad',
            text='Crosshair',
            scale=(0.2, 0.1),
            position=(0, 0),
            on_click=self.settings  
        )

        self.quit_button = Button(
            parent=self.mainmenu,
            model='quad',
            text='Quit',
            scale=(0.2, 0.1),
            position=(0, -0.1),
            on_click=self.quit_game  
        )

    def start_game(self):  
        self.mainmenu.disable()
        #Game initialization 
        ground = Entity(model='plane', scale=(100, 1, 100), color=color.yellow.tint(-.2), texture='white_cube', texture_scale=(100, 100), collider='box')
        player = Player( position=Vec3(-4.37877,0.00100005, 3.96363), rotation=Vec3(0, 90, 0))
        player.controller.on_enable()
        player.controller.speed = 0
        player.controller.cursor.disable()
        #Apply crosshair settings for game
        try:
            with open('data/crosshair.json', 'r') as file:
                slider_values = json.load(file)
                player.thickness_slider.value = slider_values['thickness']
                player.length_slider.value = slider_values['length']
                player.gap_slider.value = slider_values['gap']
                player.thick_slider()
                player.length_sli()
                player.gap()
        except FileNotFoundError:
            pass
                        
    def settings(self):
        global thickness_slider, length_slider, gap_slider
        self.mainmenu.disable()
        self.set.enable()
        player = Player(position=Vec3(-4.37877, 0.00100005, 3.96363), rotation=Vec3(0, 90, 0))
        for sliders in player.sli:
            sliders.enable()
        player.thickness_slider.position = (-0.7, -0.3)
        thickness_text = Text('Thickness', position = (-0.83, -0.29))
        player.length_slider.position = (-0.7, -0.4)
        length_text = Text('Length', position = (-0.83, -0.39))
        player.gap_slider.position = (0, -0.4)
        gap_text = Text('Gap', position = (-0.09, -0.39))
        save_button = Button(text='Save', scale=(0.2, 0.1), position=(0, -0.3))
        back_button = Button(text='Back', scale=(0.2, 0.1), position=(0.2,-0.3))
        entity = [player.gap_slider, player.thickness_slider, player.length_slider, thickness_text, length_text, gap_text, save_button, back_button]
        #Apply crosshair settings for preview
        try:
            with open('data/crosshair.json', 'r') as file:
                slider_values = json.load(file)
                player.thickness_slider.value = slider_values['thickness']
                player.length_slider.value = slider_values['length']
                player.gap_slider.value = slider_values['gap']
                player.thick_slider()
                player.length_sli()
                player.gap()
        except FileNotFoundError:
            pass

        def save_slider_values():
            file_path = 'data/crosshair.json'
            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            slider_values = {
                'thickness': player.thickness_slider.value,
                'length': player.length_slider.value,
                'gap': player.gap_slider.value
            }
            with open(file_path, 'w') as file:
                json.dump(slider_values, file)

        def go_back():
            self.set.disable()
            for item in entity:
                item.disable()
            for lines in player.line:
                lines.disable()
            self.mainmenu.enable()

        save_button.on_click = save_slider_values
        back_button.on_click = go_back
        
    def quit_game(self):  
        quit()




