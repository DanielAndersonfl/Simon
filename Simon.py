from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.clock import Clock

import random


class MyLayout(Widget):
    color_sequence = []
    player_sequence = []

    player_turn = False
    run_var = None

    score = 0

    play_sequence_counter = 0
    play_sequence_var = None

    score_label = ObjectProperty(None)
    red_tile = ObjectProperty(None)
    green_tile = ObjectProperty(None)
    blue_tile = ObjectProperty(None)
    yellow_tile = ObjectProperty(None)
    tile_grid = ObjectProperty(None)



    def player_clicks(self, tile):
        '''
        During the players turn player_clicks enables the functionality 
        of the buttons it is the on_press method on to append themselves 
        to the list of the players guesses.

        returns None
        '''
        if self.player_turn:
            clicked_tile = self.get_clicked_tile(tile)
            self.player_sequence.append(clicked_tile)                       
        else:
            return None


    def get_clicked_tile(self, tile):
        '''
        returns which game tile the player clicked.
        '''
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
        '''
        The on_press function for the 'start' button, begins the game.
        '''
        self.run_game()



    def check_most_recent_guess(self):
        '''
        Compares the most recent guess of the player to the correct 
        index in the games expected sequence.

        returns False if the guess is wrong and returns True if the 
        player was correct OR the player has not yet clicked a tile.
        '''
        index = len(self.player_sequence) - 1
        if index >= 0:
            if self.color_sequence[index] == self.player_sequence[index]:
                return True
            else:
                return False
        else:
            return True



    def run_game(self):
        '''
        Begins the scheduled interval for the game loop.
        
        returns None
        '''
        self.run_var = Clock.schedule_interval(lambda _: self._run_game(), 0)
    
    
    def _run_game(self):
        '''
        Controls whether it is the players turn or if the game needs to
        append another color to the sequence.
        
        returns None
        '''
        if self.player_turn:
            self._players_turn()
        else:
            self._computers_turn()
            
    
    def end_game(self):
        '''
        Is called when the player makes an error and the game ends.

        returns None
        '''
        print('Incorrect! Good Game!')
        Clock.unschedule(self.run_var)


    def _players_turn(self):
        '''
        Continuously checks the players guesses to the expected guesses
        calling the end_game function if the player messes up.

        If the player guesses the entire expected sequence for this turn
        ends the players turn.

        returns None
        '''
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
        '''
        Compares the final full guess of the players turn with the full
        expected guess.
        
        returns True if the player is correct and False if they made a 
        mistake.
        '''
        if self.color_sequence == self.player_sequence:
            return True
        else:
            return False


    def _computers_turn(self):
        '''
        Performs the games logic inbetween the players attempts.

        - adds a new tile to the sequence
        - plays the sequence to the player
        - increments the score
        - empties the players previous guess
        - makes it the players turn

        returns None
        '''
        self.add_tile_to_sequence()
        self.play_sequence()
        self.increment_score()
        self.player_sequence = []
        self.player_turn = True


    def play_sequence(self):
        '''
        Initializes the scheduled interval for the sequence of colors 
        to be displayed on the UI.

        returns None
        '''
        self.play_sequence_var = Clock.schedule_interval(lambda _: 
                                                    self._play_sequence(), 1)


    def _play_sequence(self):
        '''
        Plays the sequence of colors on the UI for the player to see.
        
        returns None
        '''
        if self.play_sequence_counter >= len(self.color_sequence):
            self.play_sequence_counter = 0
            Clock.unschedule(self.play_sequence_var)
        else: 
            MyLayout.highlight_tile(
                            self.color_sequence[self.play_sequence_counter])
            self.play_sequence_counter += 1
        

    def highlight_tile(tile):
        '''
        raises the brightness of the inputted tile then dims it back to 
        it's default color.
        
        returns None
        '''
        MyLayout.adjust_brightness_tile(tile)
        Clock.schedule_once(lambda _: 
                            MyLayout.adjust_brightness_tile(tile, 0.5), 0.8)


    def adjust_brightness_tile(tile, brightness_coefficient =2):
        '''
        Adjusts the brightness of the tile provided.

        returns None
        '''
        tile.background_color = [val * brightness_coefficient 
        for val in tile.background_color]



    def random_tile(self):
        '''
        returns a random tile from the game board.
        '''
        return random.choice(self.tile_grid.children)


    def add_tile_to_sequence(self):
        '''
        adds the provided tile to the current sequence for the game.
        
        returns None
        '''
        self.color_sequence.append(self.random_tile())


    def increment_score(self):
        '''
        Adds 1 to the score then calls update_score_label
        
        returns None
        '''
        self.score += 1
        Clock.schedule_once(lambda _: self.update_score_label(), 0)

        return None


    def update_score_label(self):
        '''
        updates the score_label
        
        returns None
        '''
        self.score_label.text = str(self.score)

        return None
    

class Simon(App):
    def build(self):
        return MyLayout()

if __name__ == '__main__':
    Simon().run()