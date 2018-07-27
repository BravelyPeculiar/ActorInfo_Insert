import sys
import ctypes
import binascii
import copy
import json

actorinfo_filename = sys.argv[1]
insert_name = sys.argv[2]
try: copy_name = sys.argv[3]
except: copy_name = ""

with open (actorinfo_filename, encoding='latin-1') as json_file:  
	data = json.load(json_file)

actor_container_list = []
new_actor = {}
for actor in data["root"]["Actors"]:
	actor_container_list.append({"Actor": actor})
	if actor["name"]["value"] == copy_name:
		new_actor = copy.deepcopy(actor)
for index, hash_obj in enumerate(data["root"]["Hashes"]):
	actor_container_list[index]["Hash"] = hash_obj
	
new_actor["name"]["value"] = insert_name
new_hash = ctypes.c_uint32(binascii.crc32(insert_name.encode())).value
actor_container_list.append({"Actor": new_actor, "Hash": {"value" : new_hash, "size" : 0, "nodeType" : 209}})
actor_container_list.sort(key=lambda actor_container: actor_container["Hash"]["value"])

new_actor_list = []
new_hash_list = []
for actor_container in actor_container_list:
	new_actor_list.append(actor_container["Actor"])
	new_hash_list.append(actor_container["Hash"])
data["root"]["Actors"] = new_actor_list
data["root"]["Hashes"] = new_hash_list

outstring = json.dumps(data, indent=2)
with open(actorinfo_filename, 'w+') as outfile:
	outfile.write(outstring)
