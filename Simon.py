from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.clock import Clock

import random


class MyLayout(Widget):
    color_sequence = []
    player_sequence = []

    player_turn = False
    run_counter = 0
    run_var = None

    play_sequence_counter = 0
    play_sequence_var = None

    red_tile = ObjectProperty(None)
    green_tile = ObjectProperty(None)
    blue_tile = ObjectProperty(None)
    yellow_tile = ObjectProperty(None)
    tile_grid = ObjectProperty(None)



    def player_clicks(self, tile):
        if self.player_turn:
            clicked_tile = self.get_clicked_tile(tile)
            self.player_sequence.append(clicked_tile)                       
        else:
            return None


    def get_clicked_tile(self, tile):
        if tile == 'red_tile':
            clicked_tile = self.red_tile
        elif tile == 'green_tile':
            clicked_tile = self.green_tile
        elif tile == 'blue_tile':
            clicked_tile = self.blue_tile
        elif tile == 'yellow_tile':
            clicked_tile = self.yellow_tile
        
        return clicked_tile


    def start(self):
        self.run_game()



    def check_most_recent_guess(self):
        index = len(self.player_sequence) - 1
        if index >= 0:
            if self.color_sequence[index] == self.player_sequence[index]:
                return True
            else:
                return False
        else:
            return True



    def run_game(self):
        self.run_var = Clock.schedule_interval(lambda _: self._run_game(), 0)
    
    
    def _run_game(self):
        if self.player_turn:
            self._players_turn()
        else:
            self._computers_turn()
            
    
    def end_game(self):
        print('Incorrect! Good Game!')
        Clock.unschedule(self.run_var)


    def _players_turn(self):
        if len(self.player_sequence) >= len(self.color_sequence):
            if self._compare_sequences():
                self.player_turn = False
            else:
                self.end_game()
        else:
            if self.check_most_recent_guess():
                pass
            else:
                self.end_game()



    def _compare_sequences(self):
        if self.color_sequence == self.player_sequence:
            return True
        else:
            return False


    def _computers_turn(self):
        self.add_tile_to_sequence()
        self.play_sequence()
        self.run_counter += 1
        self.player_sequence = []
        self.player_turn = True


    def play_sequence(self):
        self.play_sequence_var = Clock.schedule_interval(lambda _: 
                                                    self._play_sequence(), 1)


    def _play_sequence(self):
        if self.play_sequence_counter >= len(self.color_sequence):
            self.play_sequence_counter = 0
            Clock.unschedule(self.play_sequence_var)
        else: 
            MyLayout.highlight_tile(
                            self.color_sequence[self.play_sequence_counter])
            self.play_sequence_counter += 1
        

    def highlight_tile(tile):
        MyLayout.adjust_brightness_tile(tile)
        Clock.schedule_once(lambda _: 
                            MyLayout.adjust_brightness_tile(tile, 0.5), 0.8)


    def adjust_brightness_tile(tile, brightness_coefficient =2):
        tile.background_color = [val * brightness_coefficient 
        for val in tile.background_color]



    def random_tile(self):
        return random.choice(self.tile_grid.children)


    def add_tile_to_sequence(self):
        self.color_sequence.append(self.random_tile())


class Simon(App):
    def build(self):
        return MyLayout()

if __name__ == '__main__':
    Simon().run()