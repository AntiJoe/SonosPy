import soco
import socket
import logging
import json
import time
from datetime import datetime

vnum = 0.13
vmsg = "Change Jody's Sonos...  \n  fixes for apple and tuneit...  hopefully spotify\n  and feedback on good uri"


server_list = [("156.57.20.108", 7777)]
# HOME = ("156.57.20.108", 7777)
# bones = "192.168.5.13"
hostname = socket.gethostname()

if hostname == 'Maple-AAI':
    ip = '192.168.2.133'
    print("In Jody's office")
    server_list = [("192.168.2.205", 7777), ("156.57.20.108", 7777)]
else:
    ip = '192.168.5.13'
    print("Bone's Sonos")

sonos = soco.SoCo(ip) # change this ip to your sonos...  to copy track from.
# sonos2 = soco.SoCo('192.168.2.135')

# .play_uri(title="anytext",uri='x-sonosapi-hls:r%3aestreetradio?sid=49&amp;flags=8480&amp;sn=8')

track = sonos.get_current_track_info()
# track2 = sonos2.get_current_track_info()
# print("playing: {}".format(track2['title']))
# sonos.play_uri(title="anytext",uri=track2['title'])
# sonos2.play_uri(title="anytext",uri=track['title'])
# sonos2.play_uri(title="anytext",uri='x-sonosapi-hls:live:estreetradio?sid=49&flags=8480&sn=8')
meta = dict()
out = dict()
meta['records'] = 1
meta['command'] = 3
meta['show_meta'] = 1
meta['show_raw'] = 0
meta['log'] = "empty"
meta['host'] = hostname
meta['track'] = track['uri']
out['log'] = "Version {} calling home... ".format(vnum)
meta['extra_lines'] = 3
meta['show_meta'] = 1
meta['uri'] = track['uri']
meta['records'] = 0
out['meta'] = meta
out['samples'] = 0


if meta['command'] == 3 and (meta['uri'].startswith("x-sonos") or meta['uri'].startswith("hls-radio")):
    print("Playing a Sonos link")
else:
    print("un-playable link")

new_json = json.dumps(out, indent=2).encode(encoding='utf-8')

state = sonos.get_current_transport_info()['current_transport_state']
vol = sonos.volume
track = sonos.get_current_track_info()
queue = sonos.get_queue()
print ("  {:<13s} ".format(sonos.player_name))
print ("      {} at {:3d}% level ".format(  state,vol))
print ("      Track:  {} ".format(track['title']))
print ("          position:  {} ".format(track['position']))
print ("          duration:  {} ".format(track['duration']))
print ("      Artist: {} ".format(track['artist']))
print ("      Album:  {} ".format(track['album']))
print ("      Coordinator is {}".format(sonos.group.coordinator))
print ("      Members are {}".format(sonos.group.members))
print ("      Items in Queue are {}".format(len(queue)))
for item in queue:
    print("                 {}".format(item.title))
print()
print(sonos.get_current_track_info())


for server in server_list:
    try:
        # Send data
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sent = sock.sendto(new_json, server)
    finally:
        print('Called home')
        sock.close()