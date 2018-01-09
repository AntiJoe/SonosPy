import soco
import time
import sqlite3
# from soco.discovery import by_name

test_uri = 'x-sonosapi-hls:live%3a9418?sid=49&flags=8480&sn=2'

my_sonos = \
    [
        {"name": "Kitchen", "ip": "192.168.2.130"},
        {"name": "Patio", "ip": "192.168.2.135"},
        {"name": "Shop", "ip": "192.168.2.132"},
        {"name": "Bedroom", "ip": "192.168.2.133"},
        {"name": "LivingRoom", "ip": "192.168.2.137"}
    ]

zone_list = list(soco.discover())
# Patio = soco.SoCo('192.168.2.135')
#
# print(zone_list)
# print("My Play 5 is called: " + Patio.player_name)
# # print("Track info: ")
#
# print("The Sonos:{} is currently: ".format(Patio.player_name) + Patio.get_current_transport_info()['current_transport_state'])
#
# # Patio.group.coordinator.pause()
#
# if (Patio.get_current_transport_info()['current_transport_state'] == "PLAYING"):
#     Patio.group.coordinator.pause()
#     print("Issue Pause command\n")
#     print("The Sonos:{} is currently: ".format(Patio.player_name) + Patio.get_current_transport_info()[
#         'current_transport_state'])
# else:
#     Patio.group.coordinator.play()
#     print("Issue Play command\n")
#     print("The Sonos:{} is currently: ".format(Patio.player_name) + Patio.get_current_transport_info()[
#         'current_transport_state'])
#
# wait_time = 2
# print("Waiting {} seconds...\n".format(wait_time))
# time.sleep(wait_time)
# print("The Sonos:{} is currently: ".format(Patio.player_name) + Patio.get_current_transport_info()[
#         'current_transport_state'])



# print("Playing: {}".format(playing['title']))
# print("Playing: {} at {} volume".format(playing['title'], vol))

print("\n\nList of my Sonos players:\n")
zones = soco.discover()
for zone in zones:
    state = zone.get_current_transport_info()['current_transport_state']
    vol = zone.volume
    track = zone.get_current_track_info()
    print ("  {:<13s}".format(zone.player_name))
    print ("      IP: {}".format(zone.ip_address))
    print ("      {} at {:3d}% level ".format(  state,vol))
    print ("      Track:  {} ".format(track['title']))
    print ("      URI:    {} ".format(track['uri']))
    print ("          position:  {} ".format(track['position']))
    print ("          duration:  {} ".format(track['duration']))
    print ("      Artist: {} ".format(track['artist']))
    print ("      Album:  {} ".format(track['album']))
    print ("      Coordinator is {}".format(zone.group.coordinator))
    print ("      Members are {}".format(zone.group.members))
    print()
    print(zone.get_current_track_info())
    print(type(zone.get_current_track_info()))
    print()



# print(zone.get_queue())
# # print(zone.get_current_transport_info())
# print(zone.get_current_track_info())


# for sonos in my_sonos:
#     print(sonos['name'])
#     print(sonos['ip'])
#     sonos['player'] = soco.SoCo(sonos['ip'])
#
# print(sonos.items())
# print(sonos.get())
