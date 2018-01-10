import soco
import socket
import logging
import json
import time
from datetime import datetime

UDP_PORT = 7778
vnum = 3.0
vmsg = "many fixes... "

# update Sonos dictionary
def update_Local_Sonos(delay):
    time.sleep(delay)
    track = sonos.get_current_track_info()
    Sonos['name'] = sonos.player_name
    Sonos['volume'] = sonos.volume
    Sonos['state'] = sonos.get_current_transport_info()['current_transport_state']
    Sonos['uri'] = track['uri']
    Sonos['title'] = track['title']
    Sonos['artist'] = track['artist']
    Sonos['album'] = track['album']

server_list = [("156.57.253.45", UDP_PORT)]

hostname = socket.gethostname()

# depending on where run...  sets server list and Local Sonos ip
if hostname == 'Maple-AAI':
    ip = '192.168.2.133'
    print("In Jody's office")
    server_list = [("192.168.2.205", UDP_PORT)]
else:
    ip = '192.168.5.13'
    print("Bone's Sonos")

print("Sonos track transfer...  sending on port: ", UDP_PORT)
print("version: ", vnum)
print("version message: ", vmsg)
print(server_list)

# create empty dictionaries
meta = dict()
out = dict()
Sonos = dict()

sonos = soco.SoCo(ip) # change this ip to your sonos...  to copy track from.

update_Local_Sonos(2)  # initial update

# set initial meta data dictionary
meta['records'] = 1
meta['command'] = 3
meta['show_meta'] = 1
meta['show_raw'] = 0
meta['log'] = "empty"
meta['host'] = hostname
meta['extra_lines'] = 3
meta['show_meta'] = 1
meta['records'] = 0

out['log'] = "Version {} calling home... ".format(vnum)
out['Sonos'] = Sonos


while True:

    track = sonos.get_current_track_info()

    while (track['title'] == sonos.get_current_track_info()['title'] and track['uri'] == sonos.get_current_track_info()['uri']):
        # print("checking track...  {}".format(track.get('uri', "")))
        time.sleep(2)

    update_Local_Sonos(5)

# compile sub dictionaries into main out
    out['meta'] = meta
    out['samples'] = 0
    out['Sonos'] = Sonos


    if meta['command'] == 3 and (Sonos['uri'].startswith("x-sonos") or Sonos['uri'].startswith("hls-radio") or Sonos['uri'].startswith("x-rincon")):
        print("Playing a Sonos link")
    else:
        print("un-playable link")

    new_json = json.dumps(out).encode(encoding='utf-8')

    state = sonos.get_current_transport_info()['current_transport_state']
    vol = sonos.volume

    queue = sonos.get_queue()
    print ("  {:<13s} ".format(sonos.player_name))
    print ("      {} at {:3d}% level ".format(  state,vol))
    print ("      Title:  {} ".format(track['title']))
    print ("      URI:    {} ".format(track['uri']))
    print ("          position:  {} ".format(track['position']))
    print ("          duration:  {} ".format(track['duration']))
    print ("      Artist: {} ".format(track['artist']))
    print ("      Album:  {} ".format(track['album']))
    print ("      Coordinator is {}".format(sonos.group.coordinator))
    print ("      Members are {}".format(sonos.group.members))
    print ("      Items in Queue are {}".format(len(queue)))
    # for item in queue:
    #     print("                 {}".format(item.title))
    print()
    print(sonos.get_current_track_info())


    for server in server_list:
        try:
            # Send data
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sent = sock.sendto(new_json, server)
        finally:
            print('Called home')
            print(new_json)
            # print (Sonos['track']['uri'])
            sock.close()