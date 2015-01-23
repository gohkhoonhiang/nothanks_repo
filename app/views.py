from models import *
from flask import render_template, jsonify, request, session

nothanksapp = NoThanksApp()

def index():
    return render_template('index.html')

#####
# must get json from client
# {'player_name':''}
#
# status codes:
# 'fail',0,'not a json',400
# 'fail',1,'unable to create player',400
# 'success',2,'player created',201
#####
def create_player():
    if not request.json:
        print "[DEBUG] /nothanks/api/v1.0/app/players/create/ - request is not json"
        return return_object('fail',0,'not a json',{},400)
    player_name = request.json['player_name']
    print "[DEBUG] /nothanks/api/v1.0/app/players/create/ - request.json['player_name'] = %s" % player_name
    player = nothanksapp.create_player(player_name)
    print "[DEBUG] /nothanks/api/v1.0/app/players/create/ - nothanksapp created player %s" % player
    if player is None:
        print "[DEBUG] /nothanks/api/v1.0/app/players/create/ - unable to create player %s" % player_name
        return return_object('fail',1,'unable to create player',{},400)
    session['player_id'] = player['id']
    print "[DEBUG] /nothanks/api/v1.0/app/players/create/ - session id for player %s is %s" % (player['name'] , session.get('player_id'))
    return return_object('success',2,'player created',player,201)

#####
# get player id from session
#
# status codes:
# 'fail',0,'player does not exist in session',404
# 'fail',1,'unable to remove player',400
# 'success',2,'player removed',200
#####
def remove_player():
    player_id = session.get('player_id')
    if not player_id:
        print "[DEBUG] /nothanks/api/v1.0/app/players/remove/ - player %s does not exist in session" % player_id
        return return_object('fail',0,'player does not exist in session',{},404)
    if not nothanksapp.remove_player(player_id):
        print "[DEBUG] /nothanks/api/v1.0/app/players/remove/ - unable to remove player %s" % player_id
        return return_object('fail',1,'unable to remove player',{},400)
    print "[DEBUG] /nothanks/api/v1.0/app/players/remove/ - player %s removed" % player_id
    return return_object('success',2,'player removed',{},200)
    
#####
# get all players in app
#
# status codes:
# 'success',2,'players retrieved',200
#####
def get_players():
    players = nothanksapp.get_players()
    print "[DEBUG] /nothanks/api/v1.0/app/players/ - all players: %s" % players
    return return_object('success',2,'players retrieved',players,200)

#####
# get all players in current room (by session)
#
# status codes:
# 'fail',0,'room does not exist in session,404
# 'fail',1,'room not exists',404
# 'success',2,'players objects',200
#####
def get_players_in_room():
    room_id = session.get('room_id')
    if not room_id:
        print "[DEBUG] /nothanks/api/v1.0/app/p/players/ - room %s does not exist in session" % room_id
        return return_object('fail',0,'room does not exist in session',{},404)
    room = nothanksapp.get_room_by_id(room_id)
    if not room:
        print "[DEBUG] /nothanks/api/v1.0/app/p/players/ - room %s does not exist" % room_id
        return return_object('fail',1,'room not exists',{},404)
    players = room['players']
    print "[DEBUG] /nothanks/api/v1.0/app/p/players/ - players %s found in room %s" % (players, room_id)
    return return_object('success',2,'players objects',players,200)

#####
# get all players in any room (by request arguments)
# ?room_id=
#
# status codes:
# 'fail',0,'room id not in request',400
# 'fail',1,'room not exists',404
# 'success',2,'players objects',200
#####
def get_players_in_room_by_room_id():
    room_id = request.args.get('room_id')
    if not room_id:
        print "[DEBUG] /nothanks/api/v1.0/app/rooms/players/ - request does not have room_id"
        return return_object('fail',0,'room id not in request',{},400)
    room = nothanksapp.get_room_by_id(room_id)
    if not room:
        print "[DEBUG] /nothanks/api/v1.0/app/rooms/players/ - room %s does not exist" % room_id
        return return_object('fail',1,'room not exists',{},404)
    players = room['players']
    print "[DEBUG] /nothanks/api/v1.0/app/rooms/players/ - players object %s in room %s" % (players, room_id)
    return return_object('success',2,'players object',players,200)

#####
# must get json from client
# {'room_name':''}
#
# status codes:
# 'fail',0,'not a json',400
# 'fail',1,'unable to create room,400
# 'success',2,'room created',201
#####
def create_room():
    if not request.json:
        print "[DEBUG] /nothanks/api/v1.0/app/rooms/create/ - request is not json"
        return return_object('fail',0,'not a json',{},400)
    room_name = request.json['room_name']
    print "[DEBUG] /nothanks/api/v1.0/app/rooms/create/ - request.json['room_name'] = %s" % room_name
    room = nothanksapp.create_room(room_name)
    if room is None:
        print "[DEBUG] /nothanks/api/v1.0/app/rooms/create/ - unable to create room %s" % room_name
        return return_object('fail',1,'unable to create room',{},400)
    print "[DEBUG] /nothanks/api/v1.0/app/rooms/create/ - room %s with id %s created" % (room['name'] , room['id'])
    return return_object('success',2,'room created',room,201)

#####
# must get json from client
# {'room_id':''}
#
# status codes:
# 'fail',0,'not a json',400
# 'fail',1,'unable to remove room',400
# 'success',2,'room removed',200
#####
def remove_room():
    if not request.json:
        print "[DEBUG] /nothanks/api/v1.0/app/rooms/remove/ - request is not json"
        return return_object('fail',0,'not a json',{},400)
    room_id = request.json['room_id']
    if not nothanksapp.remove_room(room_id):
        print "[DEBUG] /nothanks/api/v1.0/app/rooms/remove/ - unable to remove room %s" % room_id
        return return_object('fail',1,'unable to remove room',{},400)
    print "[DEBUG] /nothanks/api/v1.0/app/rooms/remove/ - room %s removed" % room_id
    return return_object('success',2,'room removed',{},200)
    
#####
# get all rooms in app
#
# status codes:
# 'success',2,'rooms retrieved',200
#####
def get_rooms():
    rooms = nothanksapp.get_rooms()
    print "[DEBUG] /nothanks/api/v1.0/app/rooms/ - all rooms: %s" % rooms
    return return_object('success',2,'rooms retrieved',rooms,200)

#####
# get current room (by session)
#
# status codes:
# 'fail',0,'room not in session',404
# 'fail',1,'room does not exist',404
# 'success',2,'room exists',200
#####
def current_room():
    room_id = session.get('room_id')
    if not room_id:
        print "[DEBUG] /nothanks/api/v1.0/app/rooms/current/ - room %s does not exist in session" % room_id
        return return_object('fail',0,'room not in session',{},404)
    room = nothanksapp.get_room_by_id(room_id)
    if not room:
        print "[DEBUG] /nothanks/api/v1.0/app/rooms/current/ - room %s does not exist" % room_id
        return return_object('fail',1,'room does not exist',{},404)
    print "[DEBUG] /nothanks/api/v1.0/app/rooms/current/ - room %s exists" % room_id
    return return_object('success',2,'room exists',room,200)

#####
# get current_player (by session)
#
# status codes:
# 'fail',0,'player not in session',404
# 'fail',1,'player does not exist',404
# 'success',2,'player exists',200
#####
def current_player():
    player_id = session.get('player_id')
    if not player_id:
        print "[DEBUG] /nothanks/api/v1.0/app/players/current/ - player %s does not exist in session" % player_id
        return return_object('fail',0,'player not in session',{},404)
    player = nothanksapp.get_player_by_id(player_id)
    if not player:
        print "[DEBUG] /nothanks/api/v1.0/app/players/current/ - player %s does not exist" % player_id
        return return_object('fail',1,'player does not exist',{},404)
    print "[DEBUG] /nothanks/api/v1.0/app/players/current/ - player %s exists" % player_id
    return return_object('success',2,'player exists',player,200)

#####
# must get room id json from client, player id by session
# {'room_id':''}
#
# status codes:
# 'fail',0,'not a json',400
# 'fail',1,'player not in sesion',404
# 'fail',2,'room not found',404
# 'fail',3,'unable to join room',400
# 'success',4,'player successfully joined room',200
#####
def player_join_room():
    if not request.json:
        print "[DEBUG] /nothanks/api/v1.0/app/p/join/ - request is not json"
        return return_object('fail',0,'not a json',{},400)
    room_id = request.json['room_id']
    player_id = session.get('player_id')
    if not player_id:
        print "[DEBUG] /nothanks/api/v1.0/app/p/join/ - player %s not in session" % player_id
        return return_object('fail',1,'player not in session',{},404)
    print "[DEBUG] /nothanks/api/v1.0/app/p/join/ - player id in session %s" % player_id
    if not nothanksapp.get_room_by_id(room_id):
        print "[DEBUG] /nothanks/api/v1.0/app/p/join/ - room %s not found" % room_id
        return return_object('fail',2,'room not found',{},404)
    room = nothanksapp.add_player_to_room(room_id, player_id)
    if not room:
        print "[DEBUG] /nothanks/api/v1.0/app/p/join/ - player %s unable to join room %s" % (player_id, room_id)
        return return_object('fail',3,'unable to join room',{},400)
    print "[DEBUG] /nothanks/api/v1.0/app/p/join/ - player %s successfully joined room %s" % (player_id, room_id)
    session['room_id'] = room['id']
    print "[DEBUG] /nothanks/api/v1.0/app/p/join/ - session id for room %s is %s" % (room['id'] , session.get('room_id'))
    return return_object('success',4,'player successfully joined room',room,200)

#####
# remove player from room (by session)
#
# status codes:
# 'fail',0,'room not in session',404
# 'fail',1,'player not in session',404
# 'fail',2,'unable to remove player',400
# 'success',3,'player left room',200
#####
def player_leave_room():
    room_id = session.get('room_id')
    if not room_id:
        print "[DEBUG] /nothanks/api/v1.0/app/p/leave/ - room %s not in session" % room_id
        return return_object('fail',0,'room not in session',{},404)
    print "[DEBUG] /nothanks/api/v1.0/app/p/leave/ - session id for room %s" % session.get('room_id')
    player_id = session.get('player_id')
    if not player_id:
        print "[DEBUG] /nothanks/api/v1.0/app/p/leave/ - player %s not in session" % player_id
        return return_object('fail',1,'player not in session',{},404)
    room = nothanksapp.remove_player_from_room(room_id, player_id)
    if not room:
        print "[DEBUG] /nothanks/api/v1.0/app/p/leave/ - unable to remove player %s from room %s" % (player_id, room_id)
        return return_object('fail',1,'unable to leave room',{},400)
    print "[DEBUG] /nothanks/api/v1.0/app/p/leave/ - player %s removed from room %s" % (player_id, room_id)
    return return_object('success',2,'player left room',room,200)

#####
# start game (by session)
#
# status code:
# 'fail',0,'room not in session',404
# 'fail',1,'unable to start game',400
# 'success',2,'game started',200
#####
def start_game():
    room_id = session.get('room_id')
    if not room_id:
        print "[DEBUG] /nothanks/api/v1.0/app/p/start/ - room %s not in session" % room_id
        return return_object('fail',0,'room not in session',{},404)
    print "[DEBUG] /nothanks/api/v1.0/app/p/start/ - session id for room %s" % session.get('room_id')
    room = nothanksapp.start_game(room_id)
    if not room:
        print "[DEBUG] /nothanks/api/v1.0/app/p/start/ - unable to start game for room %s" % room_id
        return return_object('fail',1,'unable to start game',{},400)
    print "[DEBUG] /nothanks/api/v1.0/app/p/start/ - game started in room %s" % room_id
    return return_object('success',2,'game started',room,200)

#####
# draw card (by session)
#
# status codes:
# 'fail',0,'room not in session',404
# 'fail',1,'player not in session',404
# 'fail',2,'unable to draw card',400
# 'success',3,'card is drawn',200
#####
def draw_card():
    room_id = session.get('room_id')
    if not room_id:
        print "[DEBUG] /nothanks/api/v1.0/app/p/draw/ - room %s not in session" % room_id
        return return_object('fail',0,'room not in session',{},404)
    player_id = session.get('player_id')
    if not player_id:
        print "[DEBUG] /nothanks/api/v1.0/app/p/draw/ - player %s not in session" % player_id
        return return_object('fail',1,'player not in session',{},404)
    room = nothanksapp.draw_card(room_id)
    if not room:
        print "[DEBUG] /nothanks/api/v1.0/app/p/draw/ - unable to draw card"
        return return_object('fail',2,'unable to draw card',{},400)
    print "[DEBUG] /nothanks/api/v1.0/app/p/draw/ - top card is %s in room %s" % (room['top_card'], room_id)
    return return_object('success',3,'card is drawn',room,200)


def get_next_player_in_room():
    room_id = session.get('room_id')
    if not room_id:
        print "[DEBUG] /nothanks/api/v1.0/app/p/nextplayer/ - room %s not in session" % room_id
        return return_object('fail',0,'room not in session',{},404)
    room = nothanksapp.get_room_by_id(room_id)
    if not room:
        print "[DEBUG] /nothanks/api/v1.0/app/p/nextplayer/ - room %s does not exist" % room_id
        return return_object('fail',1,'room not exists',{},404)
    next_player = nothanksapp.get_next_player_in_room(room_id)
    if not next_player:
        print "[DEBUG] /nothanks/api/v1.0/app/p/nextplayer/ - unable to find next player in room %s" % room_id
        return return_object('fail',2,'unable to find next player',{},400)
    print "[DEBUG] /nothanks/api/v1.0/app/p/nextplayer/ - next player found %s in room %s" % (next_player, room_id)
    return return_object('success',3,'next player found',next_player,200)
    

def place_chip():
    room_id = session.get('room_id')
    if not room_id:
        print "[DEBUG] /nothanks/api/v1.0/app/p/placechip/ - room %s not in session" % room_id
        return return_object('fail',0,'room not in session',{},404)
    player_id = session.get('player_id')
    if not player_id:
        print "[DEBUG] /nothanks/api/v1.0/app/p/placechip/ - player %s not in session" % player_id
        return return_object('fail',1,'player not in session',{},404)
    room = nothanksapp.place_chip(room_id, player_id)
    if not room:
        print "[DEBUG] /nothanks/api/v1.0/app/p/placechip/ - unable to place chip"
        return return_object('fail',2,'unable to place chips',{},400)
    print "[DEBUG] /nothanks/api/v1.0/app/p/placechip/ - player %s places a chip" % player_id
    return return_object('success',3,'player places chip',room,200)


def take_card():
    room_id = session.get('room_id')
    if not room_id:
        print "[DEBUG] /nothanks/api/v1.0/app/p/takecard/ - room %s not in session" % room_id
        return return_object('fail',0,'room not in session',{},404)
    player_id = session.get('player_id')
    if not player_id:
        print "[DEBUG] /nothanks/api/v1.0/app/p/takecard/ - player %s not in session" % player_id
        return return_object('fail',1,'player not in session',{},404)
    room = nothanksapp.take_card(room_id, player_id)
    if not room:
        print "[DEBUG] /nothanks/api/v1.0/app/p/takecard/ - unable to take card"
        return return_object('fail',2,'unable to take card',{},400)
    print "[DEBUG] /nothanks/api/v1.0/app/p/takecard/ - player %s takes card %s" % (player_id, room['topcard']) 
    return return_object('success',3,'card is taken',room,200)
    

def end_game():
    pass
    
    
def has_next_card():
    pass


def get_game_result():
    pass
    
#####
# decorator functions
#####
def check_room_in_session(func):
    def func_wrapper(*args, **kwargs):
        room_id = session.get('room_id')
        if not room_id:
            return return_object('fail',0,'room not in session',{},404)
        return func(*args, **kwargs)
    return func_wrapper


#####
# format return json object
#####
def return_object(result, code, message, output, status_code):
    return jsonify({'result':result, 'code':code, 'message':message, 'output':output}), status_code
