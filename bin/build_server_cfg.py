# This builds a Q3A LAN server config with features such as :
#  - Randomized map rotation with pinned warmup maps.
#  - Randomized RCON password
# Author: Zathu

import zipfile
import os
import re
import random

base_dir = 'baseq3'
map_list_warmup = ['q3dm17', 'q3dm1']  # These maps will always be first. Also add to blacklist to avoid duplicates.
randomizer_blacklist = r'q3tourney|q3dm0.bsp|pro-|test_bigbox|q3dm17.bsp|q3dm1.bsp'
constants_ffa = 'set g_gametype 1; fraglimit 20; set bot_enable 0;'
constants_ctf = 'set g_gametype 4; capturelimit 5; set bot_enable 1; set bot_minplayers 8; g_spskill 4; seta g_teamAutoJoin 1;'
map_list = []
shuffled_maps = []

# Build a list of all map names
for file in os.listdir(base_dir):
    # Only PK3 files
    if file.endswith(".pk3"):
        zip = zipfile.ZipFile(os.path.join(base_dir, file))
        # Check for .bsp map files inside
        for inner_file in zip.namelist():
            if inner_file.endswith(".bsp"):
                # Filter out blacklisted maps and build a list
                if not any(re.findall(randomizer_blacklist, inner_file, re.IGNORECASE)):
                    map_name = inner_file.split('/')[1].split('.')[0]
                    shuffled_maps.append(map_name)

# Shuffle the maps
random.shuffle(shuffled_maps)
map_list = map_list_warmup + shuffled_maps
total_maps = len(map_list)

# Generate RCON password (set in client with /rconPassword XXXX)
rcon_password = str(random.randrange(1000, 9999))
print("RCON password: " + rcon_password)

# Loop to build the Q3 map rotation server cvars
count = 0
server_script = "seta sv_hostname \"^1LAN ^3Server\"\nseta rconpassword \"" + rcon_password + "\"\n"
while count < total_maps:
    next_cvar = count + 1
    # End by going back to d0
    if next_cvar == total_maps:
        next_cvar = 0
    # Build d#'s
    if 'ctf' in map_list[count]:
        constants = constants_ctf
    else:
        constants = constants_ffa
    server_script_line = "set d" + str(count) + " \"" + constants + " map " + map_list[count] + '; set nextmap vstr d' + str(next_cvar) + "\"" + "\n"
    server_script += server_script_line
    count += 1

server_script += "vstr d0\n"

with open(os.path.join(base_dir, "server.cfg"), "w") as text_file:
    text_file.write(server_script)