#!/usr/bin/env python3
'''
The main executable
'''
# pylint: disable = C0103
import os
from flask import Flask
import belmont_adventure.world as world
from belmont_adventure.player import Player

app = Flask(__name__)


@app.route('/')
def play():
    '''
    Game wrapper
    '''
    world.load_tiles()
    player = Player()
    #These lines load the starting room and display the text
    room = world.tile_exists(player.location_x, player.location_y)
    print(room.intro_text())
    while player.is_alive() and not player.victory:
        room = world.tile_exists(player.location_x, player.location_y)
        room.modify_player(player)
        # Check again since the room could have changed the player's state
        if player.is_alive() and not player.victory:
            print("Choose an action:\n")
            available_actions = room.available_actions()
            for action in available_actions:
                print(action)
            action_input = input('Action: ')
            for action in available_actions:
                if action_input == action.hotkey:
                    player.do_action(action, **action.kwargs)
                    break


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 6787))
    app.run(host='0.0.0.0', port=PORT)
