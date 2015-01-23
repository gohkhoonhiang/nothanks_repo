import datetime
from random import shuffle

class NoThanksApp(object):

    '''
    game_state = [
        waiting_player,
        ready_to_start,
        draw_card,
        take_or_pay,
        calculate_points
    ]
    nothanksapp = {
		'roomid' : {
			'id' : '',
			'name' : '',
			'players' : {
				'playerid' : {
					'id' : '',
					'name' : '',
					'chips' : 11,
					'cards' : [],
					'points' : 0
				},
				'playerid' : {
					'id' : '',
					'name' : '',
					'chips' : 11,
					'cards' : [],
					'points' : 0
				}
			},
			'cards' : [],
			'next_player' : 0,
			'top_card' : 0,
			'current_chips' : 0,
			'state' : '',
			'current_winner' : {
		        'point' : 0,
		        'player' : ''
			}
		},
		'roomid' : {
			'id' : '',
			'name' : '',
			'players' : {
				'playerid' : {
					'id' : '',
					'name' : '',
					'chips' : 11,
					'cards' : [],
					'points' : 0
				},
				'playerid' : {
					'id' : '',
					'name' : '',
					'chips' : 11,
					'cards' : [],
					'points' : 0
				}
			},
			'cards' : [],
			'next_player' : 0,
			'top_card' : 0,
			'current_chips' : 0,
			'state' : '',
			'current_winner' : {
		        'point' : 0,
		        'player' : ''
			}
		}
	}
    '''

    def __init__(self):
        self.rooms = {}
        self.players = {}
        
    # operations concerning rooms

    def create_room(self, room_name):
        if self.check_room_exists_by_name(room_name):
            return None
        room_id = self.generate_id(room_name)
        room = self.reset_room_state(room_id, room_name=room_name)
        self.rooms[room_id] = room
        return room

    def remove_room(self, room_id):
        if self.check_room_exists_by_id(room_id):
            self.rooms.pop(room_id)
            return True
        return False

    def get_rooms(self):
        return self.rooms

    def check_room_exists_by_id(self, room_id):
        return room_id in self.rooms.keys()

    def check_room_exists_by_name(self, room_name):
        return room_name in [room['name'] for room in self.rooms.values()]  

    def get_room_by_id(self, room_id):
        return self.rooms.get(room_id)
        
    def reset_room_state(self, room_id, *args, **kwargs):
        room = {}
        if self.check_room_exists_by_id(room_id):
            room = self.get_room_by_id(room_id)
        else:
            room['id'] = room_id
            room['name'] = kwargs.get('room_name', '')
        room['cards'] = []
        room['players'] = {}
        room['next_player'] = 0
        room['top_card'] = 0
        room['current_chips'] = 0
        room['state'] = 'waiting_player'
        room['current_winner'] = {'point' : 0, 'player' : ''}
        return room
    
    # operations concerning players

    def create_player(self, player_name):
        if self.check_player_exists_by_name(player_name):
            return None
        player_id = self.generate_id(player_name)
        player = self.reset_player_state(player_id, player_name=player_name)
        self.players[player_id] = player 
        return player

    def remove_player(self, player_id):
        if self.check_player_exists_by_id(player_id):
            self.players.pop(player_id)
            return True
        return False

    def get_players(self):
        return self.players

    def check_player_exists_by_id(self, player_id):
        return player_id in self.players.keys()

    def check_player_exists_by_name(self, player_name):
        return player_name in [player['name'] for player in self.players.values()]

    def get_player_by_id(self, player_id):
        return self.players.get(player_id)
        
    def reset_player_state(self, player_id, *args, **kwargs):
        player = {}
        if self.check_player_exists_by_id(player_id):
            player = self.get_player_by_id(player_id)
        else:
            player['id'] = player_id
            player['name'] = kwargs.get('player_name', '')
        player['chips'] = 0
        player['cards'] = []
        player['points'] = 0
        return player
        
    # operations concerning player management in room

    def add_player_to_room(self, room_id, player_id):
        if not self.check_player_exists_by_id(player_id):
            return None 
        if not self.check_room_exists_by_id(room_id):
            return None
        if self.check_player_exists_in_room_by_id(room_id, player_id):
            return None
        if not self.check_can_add_player_to_room(room_id):
            return None
        room = self.get_room_by_id(room_id)
        player = self.get_player_by_id(player_id)
        room['players'][player_id] = player
        if self.check_enough_players_to_start_game(room_id):
            room['state'] = 'ready_to_start'
        return room

    def remove_player_from_room(self, room_id, player_id):
        if not self.check_player_exists_by_id(player_id):
            return None
        if not self.check_room_exists_by_id(room_id):
            return None
        if not self.check_player_exists_in_room_by_id(room_id, player_id):
            return None
        room = self.get_room_by_id(room_id)
        player = self.get_player_by_id(player_id)
        room['players'].pop(player_id)
        if not self.check_enough_players_to_start_game(room_id):
            room['state'] = 'waiting_player'
        return room

    def get_players_in_room(self, room_id):
        if not self.check_room_exists_by_id(room_id):
            return None
        room = self.get_room_by_id(room_id)
        return room['players']

    def get_player_in_room_by_id(self, room_id, player_id):
        if not self.check_player_exists_in_room_by_id(room_id, player_id):
            return None
        room = self.get_room_by_id(room_id)
        return room['players'].get(player_id)

    def get_next_player_in_room(self, room_id):
        if not self.check_room_exists_by_id(room_id):
            return None
        room = self.get_room_by_id(room_id)
        room_players = room['players']
        if not room_players:
            return None
        players = [p for p in room_players.keys()]
        players.sort()
        player_index = room['next_player']
        return room['players'].get(players[player_index])

    def set_next_player_in_room(self, room_id):
        if not self.check_room_exists_by_id(room_id):
            return False
        room = self.get_room_by_id(room_id)
        next_player_index = room['next_player'] + 1
        print "next_player_index %s" % next_player_index
        if next_player_index == len(room['players']):
            next_player_index = 0
        room['next_player'] = next_player_index
        print "room['next_player'] %s" % room['next_player']

    def check_player_exists_in_room_by_id(self, room_id, player_id):
        if not self.check_room_exists_by_id(room_id):
            return False
        if not self.check_player_exists_by_id(player_id):
            return False
        room = self.get_room_by_id(room_id)
        return player_id in room['players'].keys()
        
    def check_enough_players_to_start_game(self, room_id):
        if not self.check_room_exists_by_id(room_id):
            return False
        room = self.get_room_by_id(room_id)
        num_of_players = len(room['players'])
        if num_of_players > 2 and num_of_players < 6:
            return True
        return False
    
    def check_can_add_player_to_room(self, room_id):
        if not self.check_room_exists_by_id(room_id):
            return False
        room = self.get_room_by_id(room_id)
        if room['state'] != 'waiting_player':
            return False
        if self.check_enough_players_to_start_game(room_id):
            return False
        return True
        
    # operations concerning actual game play

    def start_game(self, room_id):
        if not self.check_room_exists_by_id(room_id):
            return None 
        room = self.get_room_by_id(room_id)
        if not self.check_enough_players_to_start_game(room_id):
            return None
        for player in room['players'].values():
			player['chips'] = 11
        cards = [x for x in range(3,36)]
        shuffle(cards)
        room['cards'] = cards
        room['state'] = 'draw_card'
        return room

    def end_game(self, room_id):
        if not self.check_room_exists_by_id(room_id):
            return False
        if self.reset_room_state(room_id):
            return True
        return False
        
    def check_has_next_card(self, room_id):
        if not self.check_room_exists_by_id(room_id):
            return False
        room = self.get_room_by_id(room_id)
        if len(room['cards']) == 0:
            return False
        return True

    def draw_card(self, room_id):
        if not self.check_room_exists_by_id(room_id):
            return None
        room = self.get_room_by_id(room_id)
        if self.check_has_next_card(room_id):
            top_card = room['cards'].pop()
            room['top_card'] = top_card
            room['state'] = 'take_or_pay';
            return room
        room['state'] = 'calculate_points'
        return None
    
    def take_card(self, room_id, player_id):
        if not self.check_room_exists_by_id(room_id):
            return None
        if not self.check_player_exists_by_id(player_id):
            return None
        if not self.check_player_exists_in_room_by_id(room_id, player_id):
            return None
        room = self.get_room_by_id(room_id)
        player = self.get_player_in_room_by_id(room_id, player_id)
        top_card = room['top_card']
        current_chips = room['current_chips']
        player['cards'].append(top_card)
        player['cards'].sort()
        player['chips'] += current_chips
        room['current_chips'] = 0
        room['state'] = 'draw_card'
        self.set_next_player_in_room(room_id)
        return room

    def place_chip(self, room_id, player_id):
        if not self.check_room_exists_by_id(room_id):
            return None
        if not self.check_player_exists_by_id(player_id):
            return None
        if not self.check_player_exists_in_room_by_id(room_id, player_id):
            return None
        room = self.get_room_by_id(room_id)
        player = self.get_player_in_room_by_id(room_id, player_id)
        player['chips'] -= 1
        room['current_chips'] += 1
        self.set_next_player_in_room(room_id)
        return room
        
    def get_game_result(self, room_id):
        if not self.check_room_exists_by_id(room_id):
            return None
        if not self.check_player_exists_by_id(player_id):
            return None
        if not self.check_player_exists_in_room_by_id(room_id, player_id):
            return None
        room = self.get_room_by_id(room_id)
        for p in room['players'].values():
            chips = p['chips']
            cards = p['cards']
            points = chips + self.calculate_card_points(cards)
            p['points'] = points
            if points > current_winner['point']:
                room['current_winner']['point'] = points
                room['current_winner']['player'] = p['id']
        return room
    
    # helper functions

    def generate_id(self, name):
        return str(hash(name + str(datetime.datetime.now())))
