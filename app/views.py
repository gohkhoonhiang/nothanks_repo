#####
# global return json codes
#
# 0: request is not json, 400
# 0: request has no argument, 400
# 1: not in session, 404
# 2: does not exist in memory, 404
# 3: unsuccessful, 400
# 4: successful, 200/201
# 5: action not allowed, 403
#####

from models import *
from flask import render_template, jsonify, request, session
from functools import wraps
from datetime import datetime

nothanksapp = NoThanksApp()

SUPPRESS_LOG = True

API_NAME = {
    'create_player' : '/nothanks/api/v1.0/app/players/create/',
    'remove_player' : '/nothanks/api/v1.0/app/players/remove/',
    'get_players' : '/nothanks/api/v1.0/app/players/',
    'current_player' : '/nothanks/api/v1.0/app/players/current/',
    'create_room' : '/nothanks/api/v1.0/app/rooms/create/',
    'remove_room' : '/nothanks/api/v1.0/app/rooms/remove/',
    'get_rooms' : '/nothanks/api/v1.0/app/rooms/',
    'current_room' : '/nothanks/api/v1.0/app/rooms/current/',
    'get_players_in_room' : '/nothanks/api/v1.0/app/p/players/',
    'get_players_in_room_by_room_id' : '/nothanks/api/v1.0/app/rooms/players/',
    'player_join_room' : '/nothanks/api/v1.0/app/players/current/',
    'player_leave_room' : '/nothanks/api/v1.0/app/p/leave/',
    'start_game' : '/nothanks/api/v1.0/app/p/start/',
    'draw_card' : '/nothanks/api/v1.0/app/p/draw/',
    'place_chip' : '/nothanks/api/v1.0/app/p/placechip/',
    'take_card' : '/nothanks/api/v1.0/app/p/takecard/',
    'get_game_result' : '/nothanks/api/v1.0/app/p/gameresult/',
    'get_next_player_in_room' : '/nothanks/api/v1.0/app/p/nextplayer/'
}

#####
# logging wrapper
#####
def server_log(type='DEBUG', api_name='', message='', *args):
    if SUPPRESS_LOG:
        return
    log_message = "[{0}] -- [{1}] {2} - {3}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),type, api_name, message)
    if len(args):
        log_message = log_message.format(*args)
    print log_message
    print ''    


#####
# request is json decorator
#####
def request_is_json(api_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.json:
                server_log('ERROR',api_name,'request is not json')
                return return_object('fail',0,'request is not json',{},400)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


#####
# request has arguments decorator
#####
def request_has_args(api_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.args:
                server_log('ERROR',api_name,'request has no argument')
                return return_object('fail',0,'request has no argument',{},400)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


#####
# room in session decorator
#####
def room_in_session(api_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            room_id = session.get('room_id')
            if not room_id:
                server_log('ERROR',api_name,'room not in session')
                return return_object('fail',1,'room does not exist in session',{},404)
            room = nothanksapp.get_room_by_id(room_id)
            if not room:
                server_log('ERROR',api_name,'room {0} not exists',room_id)
                return return_object('fail',2,'room does not exist',{},404)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
    

#####
# player in session decorator
#####
def player_in_session(api_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            player_id = session.get('player_id')
            if not player_id:
                server_log('ERROR',api_name,'player not in session')
                return return_object('fail',1,'player does not exist in session',{},404)
            player = nothanksapp.get_player_by_id(player_id)
            if not player:
                server_log('ERROR',api_name,'player {0} not exists',player_id)
                return return_object('fail',2,'player does not exist',{},404)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


#####
# player in request is next player to take action decorator
#####
def is_next_player(api_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            room_id = session.get('room_id')
            player_id = session.get('player_id')
            if nothanksapp.check_is_next_player_in_room(room_id, player_id):
                return f(*args, **kwargs)
            server_log('ERROR',api_name,'action not allowed for player {0} in room {1}',player_id,room_id)
            return return_object('fail',5,'action not allowed',{},403)
        return decorated_function
    return decorator

def index():
    return render_template('index.html')


#####
# must get json from client
# {'player_name':''}
#
# status codes:
# 'fail',3,'fail to create player',400
# 'success',4,'player created',201
#####
@request_is_json(API_NAME['create_player'])
def create_player():
    player_name = request.json['player_name']
    server_log('DEBUG',API_NAME['create_player'],"request.json['player_name'] = {0}",player_name)
    player = nothanksapp.create_player(player_name)
    if player is None:
        server_log('ERROR',API_NAME['create_player'],'fail to create player {0}',player_name)
        return return_object('fail',3,'fail to create player',{},400)
    server_log('DEBUG',API_NAME['create_player'],'player {0} created',player)
    session['player_id'] = player['id']
    server_log('DEBUG',API_NAME['create_player'],'id in session for player {0} is {1}',player_name,session.get('player_id'))
    return return_object('success',4,'player created',player,201)


#####
# get player id from session
#
# status codes:
# 'fail',3,'fail to remove player',400
# 'success',4,'player removed',200
#####
@player_in_session(API_NAME['remove_player'])
def remove_player():
    player_id = session.get('player_id')
    if not nothanksapp.remove_player(player_id):
        server_log('ERROR',API_NAME['remove_player'],'fail to remove player {0}',player_id)
        return return_object('fail',3,'unable to remove player',{},400)
    server_log('DEBUG',API_NAME['remove_player'],'player {0} removed',player_id)
    return return_object('success',4,'player removed',{},200)
    
    
#####
# get all players in app
#
# status codes:
# 'success',4,'players retrieved',200
#####
def get_players():
    players = nothanksapp.get_players()
    server_log('DEBUG',API_NAME['get_players'],'all players: {0}',players)
    return return_object('success',4,'players retrieved',players,200)


#####
# get all players in current room (by session)
#
# status codes:
# 'success',4,'players retrieved',200
#####
@room_in_session(API_NAME['get_players_in_room'])
def get_players_in_room():
    room_id = session.get('room_id')
    room = nothanksapp.get_room_by_id(room_id)
    players = room['players']
    server_log('DEBUG',API_NAME['get_players_in_room'],'players {0} in room {1}',players,room_id)
    return return_object('success',4,'players retrieved',players,200)


#####
# get all players in any room (by request arguments)
# ?room_id=
#
# status codes:
# 'success',4,'players objects',200
#####
@request_has_args(API_NAME['get_players_in_room_by_room_id'])
def get_players_in_room_by_room_id():
    room_id = request.args.get('room_id')
    if not room_id:
        server_log('ERROR',API_NAME['get_players_in_room_by_room_id'],'request does not have room_id')
        return return_object('fail',0,'room id not in request',{},400)
    room = nothanksapp.get_room_by_id(room_id)
    if not room:
        server_log('ERROR',API_NAME['get_players_in_room_by_room_id'],'room {0} does not exist',room_id)
        return return_object('fail',2,'room not exists',{},404)
    players = room['players']
    server_log('DEBUG',API_NAME['get_players_in_room_by_room_id'],'players {0} in room {1}',players,room_id)
    return return_object('success',4,'players object',players,200)


#####
# must get json from client
# {'room_name':''}
#
# status codes:
# 'fail',3,'fail to create room,400
# 'success',4,'room created',201
#####
@request_is_json(API_NAME['create_room'])
def create_room():
    room_name = request.json['room_name']
    server_log('DEBUG',API_NAME['create_room'],"request.json['room_name'] = {0}",room_name)
    room = nothanksapp.create_room(room_name)
    if room is None:
        server_log('ERROR',API_NAME['create_room'],'fail to create room {0}',room_name)
        return return_object('fail',3,'fail to create room',{},400)
    server_log('DEBUG',API_NAME['create_room'],'room {0} created',room)
    return return_object('success',4,'room created',room,201)


#####
# must get json from client
# {'room_id':''}
#
# status codes:
# 'fail',3,'fail to remove room',400
# 'success',4,'room removed',200
#####
@request_is_json(API_NAME['remove_room'])
def remove_room():
    room_id = request.json['room_id']
    if not nothanksapp.remove_room(room_id):
        server_log('ERROR',API_NAME['remove_room'],'fail to remove room {0}',room_id)
        return return_object('fail',3,'fail to remove room',{},400)
    server_log('DEBUG',API_NAME['remove_room'],'room {0} removed',room_id)
    return return_object('success',4,'room removed',{},200)
    
    
#####
# get all rooms in app
#
# status codes:
# 'success',4,'rooms retrieved',200
#####
def get_rooms():
    rooms = nothanksapp.get_rooms()
    server_log('DEBUG',API_NAME['get_rooms'],'all rooms: {0}',rooms)
    return return_object('success',4,'rooms retrieved',rooms,200)


#####
# get current room (by session)
#
# status codes:
# 'success',4,'room exists',200
#####
@room_in_session(API_NAME['current_room'])
def current_room():
    room_id = session.get('room_id')
    room = nothanksapp.get_room_by_id(room_id)
    server_log('DEBUG',API_NAME['current_room'],'room {0} exists: {1}',room_id,room)
    return return_object('success',4,'room exists',room,200)


#####
# get current_player (by session)
#
# status codes:
# 'success',4,'player exists',200
#####
@player_in_session(API_NAME['current_player'])
def current_player():
    player_id = session.get('player_id')
    player = nothanksapp.get_player_by_id(player_id)
    server_log('DEBUG',API_NAME['current_player'],'player {0} exists: {1}',player_id,player)
    return return_object('success',4,'player exists',player,200)


#####
# must get room id json from client, player id by session
# {'room_id':''}
#
# status codes:
# 'fail',3,'fail to join room',400
# 'success',4,'player successfully joined room',200
#####
@request_is_json(API_NAME['player_join_room'])
@player_in_session(API_NAME['player_join_room'])
def player_join_room():
    room_id = request.json['room_id']
    player_id = session.get('player_id')
    room = nothanksapp.add_player_to_room(room_id, player_id)
    if not room:
        server_log('ERROR',API_NAME['player_join_room'],'player {0} fail to join room {1}',player_id,room_id)
        return return_object('fail',3,'fail to join room',{},400)
    server_log('DEBUG',API_NAME['player_join_room'],'player {0} successfully joined room {1}',player_id,room_id)
    session['room_id'] = room['id']
    server_log('DEBUG',API_NAME['player_join_room'],'id in session for room {0} is {1}',room_id,session.get('room_id'))
    return return_object('success',4,'player successfully joined room',room,200)


#####
# remove player from room (by session)
#
# status codes:
# 'fail',3,'fail to remove player from room',400
# 'success',4,'player left room',200
#####
@room_in_session(API_NAME['player_leave_room'])
@player_in_session(API_NAME['player_leave_room'])
def player_leave_room():
    room_id = session.get('room_id')
    player_id = session.get('player_id')
    room = nothanksapp.remove_player_from_room(room_id, player_id)
    if not room:
        server_log('ERROR',API_NAME['player_leave_room'],'fail to remove player {0} from room {1}',player_id,room_id)
        return return_object('fail',3,'fail to remove player from room',{},400)
    server_log('DEBUG',API_NAME['player_leave_room'],'player {0} removed from room {1}',player_id,room_id)
    return return_object('success',4,'player left room',room,200)


#####
# start game (by session)
#
# status code:
# 'fail',3,'fail to start game',400
# 'success',4,'game started',200
#####
@room_in_session(API_NAME['start_game'])
def start_game():
    room_id = session.get('room_id')
    room = nothanksapp.start_game(room_id)
    if not room:
        server_log('ERROR',API_NAME['start_game'],'fail to start game in room {0}',room_id)
        return return_object('fail',3,'fail to start game',{},400)
    server_log('DEBUG',API_NAME['start_game'],'game started in room {0}: {1}',room_id,room)
    session['last_draw_player'] = '-1'
    return return_object('success',4,'game started',room,200)


#####
# draw card (by session)
#
# status codes:
# 'fail',3,'fail to draw card',400
# 'success',4,'card is drawn',200
# 'fail',5,'draw action not allowed',403
#####
@room_in_session(API_NAME['draw_card'])
@player_in_session(API_NAME['draw_card'])
@is_next_player(API_NAME['draw_card'])
def draw_card():
    room_id = session.get('room_id')
    player_id = session.get('player_id')
    if player_id == session.get('last_draw_player'):
        server_log('ERROR',API_NAME['draw_Card'],'draw action not allowed for player {0}',player_id)
        return return_object('fail',5,'draw action not allowed',{},403)
    room = nothanksapp.draw_card(room_id)
    if not room:
        server_log('ERROR',API_NAME['draw_card'],'player {0} fail to draw card in room {1}',player_id,room_id)
        return return_object('fail',3,'fail to draw card',{},400)
    server_log('DEBUG',API_NAME['draw_card'],'top card in room {0} is {1}',room_id,room['top_card'])
    session['last_draw_player'] = player_id
    return return_object('success',4,'card is drawn',room,200)


#####
# place chip (by session)
#
# status code:
# 'fail',3,'fail to place chips',400
# 'success',4,'player placed chip',200
#####
@room_in_session(API_NAME['place_chip'])
@player_in_session(API_NAME['place_chip'])
@is_next_player(API_NAME['place_chip'])
def place_chip():
    room_id = session.get('room_id')
    player_id = session.get('player_id')
    room = nothanksapp.place_chip(room_id, player_id)
    if not room:
        server_log('ERROR',API_NAME['place_chip'],'player {0} fail to place chip in room {1}',player_id,room_id)
        return return_object('fail',2,'unable to place chips',{},400)
    server_log('DEBUG',API_NAME['place_chip'],'player {0} placed a chip in room {1}',player_id,room_id)
    return return_object('success',4,'player placed chip',room,200)


#####
# take card (by session)
#
# status codes:
# 'fail',3,'fail to take card',400
# 'success',4,'card is taken',200
#####
@room_in_session(API_NAME['take_card'])
@player_in_session(API_NAME['take_card'])
@is_next_player(API_NAME['take_card'])
def take_card():
    room_id = session.get('room_id')
    player_id = session.get('player_id')
    room = nothanksapp.take_card(room_id, player_id)
    if not room:
        server_log('ERROR',API_NAME['take_card'],'player {0} fail to take the card in room {1}',player_id,room_id)
        return return_object('fail',3,'fail to take card',{},400)
    server_log('DEBUG',API_NAME['take_card'],'player {0} took card {1}',player_id,room['top_card'])
    return return_object('success',4,'card is taken',room,200)


#####
# get game result (by session)
#
# status codes:
# 'fail',3,'fail to calculate results',400
# 'success',4,'results out',200
#####
@room_in_session(API_NAME['get_game_result'])
def get_game_result():
    room_id = session.get('room_id')
    room = nothanksapp.get_game_result(room_id)
    if not room:
        server_log('ERROR',API_NAME['get_game_result'],'fail to calculate results for room {0}',room_id)
        return return_object('fail',3,'fail to calculate result',{},400)
    server_log('DEBUG',API_NAME['get_game_result'],'result for room {0}: winner is {1}',room_id,room['current_winner'])
    return return_object('success',4,'results out',room,200)
    

#####
# get next player (by session)
#
# status codes:
# 'fail',3,'fail to get next player',400
# 'success',4,'next player found',200
#####
@room_in_session(API_NAME['get_next_player_in_room'])
def get_next_player_in_room():
    room_id = session.get('room_id')
    room = nothanksapp.get_room_by_id(room_id)
    next_player = nothanksapp.get_next_player_in_room(room_id)
    if not next_player:
        server_log('ERROR',API_NAME['get_next_player_in_room'],'fail to get next player in room {0}',room_id)
        return return_object('fail',3,'fail to get next player',{},400)
    server_log('DEBUG',API_NAME['get_next_player_in_room'],'next player in room {0} is {1}',room_id,next_player)
    return return_object('success',4,'next player found',next_player,200)
    

def end_game():
    pass
    
    
def has_next_card():
    pass
    

#####
# format return json object
#####
def return_object(result, code, message, output, status_code):
    return jsonify({'result':result, 'code':code, 'message':message, 'output':output}), status_code
