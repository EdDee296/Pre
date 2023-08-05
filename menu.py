from ursina import *
import json, os
from player import Player

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




