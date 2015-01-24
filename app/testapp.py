from models import *

nothanksapp = NoThanksApp()
room = nothanksapp.create_room('room 1')
print "create room %s" % room
eric = nothanksapp.create_player('eric')
print "create eric %s" % eric
khoon = nothanksapp.create_player('khoon')
print "create khoon %s" % khoon
ace = nothanksapp.create_player('ace')
print "create ace %s" % ace
room = nothanksapp.add_player_to_room(room['id'],eric['id'])
room = nothanksapp.add_player_to_room(room['id'],khoon['id'])
room = nothanksapp.add_player_to_room(room['id'],ace['id'])
print "added player to room %s" % room
eric['chips'] = 11
eric['cards'] = [3,4,7,16,22,23,34,35]
khoon['chips'] = 19
khoon['cards'] = [6,11,15,19,20,30,31,32]
ace['chips'] = 3
ace['cards'] = [8,9,10,17,21,27,28,33]
room = nothanksapp.get_game_result(room['id'])
print "eric points %s" % eric
print "khoon points %s" % khoon
print "ace points %s" % ace
print "current winner %s" % room['current_winner']
