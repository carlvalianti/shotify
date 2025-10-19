import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import random

def powerhour(chosen_uri, chosen_playlist, chosen_random, chosen_offset, chosen_device_id):
    """Main logic for running the powerhour program."""
    # playlist URI and info - make this user selectable
    powerhour_uri = chosen_uri
    playlist = sp.playlist(playlist_id=powerhour_uri, additional_types=('track',))
    local_device_id = chosen_device_id
    local_playlist = chosen_playlist

    num_tracks = len(playlist['tracks']['items'])
    # create track # list
    track_list = list(range(num_tracks))
    # randomize track_list and get last track number
    if chosen_random:
        random.shuffle(track_list)

    # create song start offset if user wants
    if chosen_offset:
        offset = 30000 #30 seconds
    else:
        offset = 0

    # get last track number
    last_song = track_list[-1]

    for i in track_list:
        # play every song but the last starting at 30s
        if i != last_song:
            print(f"Playing track #{i + 1} out of {num_tracks} tracks from '{local_playlist}'")
            sp.start_playback(device_id = local_device_id,context_uri=powerhour_uri, offset={"position": i}, position_ms=offset)
            # wait 60 seconds to change song / 60 1 second waits for any user pauses
            for _ in range(10):
                time.sleep(1)
                # if user pauses, sleep program until they resume
                while not sp.current_playback()['is_playing']:
                    time.sleep(0.1)
        # play last song in its entirety
        else:
            print(f"Playing [LAST TRACK] #{i + 1} out of {num_tracks} tracks from '{local_playlist}'")
            sp.start_playback(context_uri=powerhour_uri, offset={"position": i})

def devices(user_devices):
    """Handles device selection (ID) with refresh support"""
    while True:
        device_info = []
        count = 0

        # grab and store all of user's devices (name, id) tuples in a list
        for item in user_devices["devices"]:
            new_device_tuple = (item["name"], item["id"])
            device_info.append(new_device_tuple)

        # display list of available device options to the user (I think enumerate is easier, but I don't really know it yet)
        print("Available Devices:\n")
        for item in device_info:
            count += 1
            print(f"{count}. {item[0]}")

        choice = input(
            "\nWhich device # would you like to play? "
            "(Enter 'refresh' to update list, or # to select): ").strip().lower()

        if choice == "refresh":
            return None
        # get device ID for user selected device
        try:
            device_choice = int(choice) -1

            if 0 <= device_choice < len(device_info):
                selected_name = device_info[device_choice][0]  # get name
                local_device_id = device_info[device_choice][1] #get ID
                print(f"Playing on '{selected_name}' (ID: {local_device_id})")
                break
            else:
                print("Invalid number. Please try again.")

        except ValueError:
            print("Please enter a valid number...")
    return local_device_id

def user_information(user_playlists):
    """Playlist and program options selection"""

    name_and_uri = []
    count = 0

    # grab and store 50 playlists from user's account
    for item in user_playlists['items']:
        new_tuple = (item['name'], item['uri'])
        name_and_uri.append(new_tuple)

    while True:
    # print 25 user playlists and store IDs of each
        print("\nHere are your (25) most recently played playlists:")
        for item in name_and_uri[:25]:
            count += 1
            print(f"{count}. {item[0]}") #maybe only show first X amount of characters?

        choice = input("\nEnter playlist # (or 'refresh' to reload): ").strip().lower()

        if choice == "refresh":
            return None, None, None

        try:
            choice_number = int(choice) -1
            if 0 <= choice_number < len(name_and_uri):
                local_playlist_name = name_and_uri[choice_number][0]
                local_uri = name_and_uri[choice_number][1]
                break
            else:
                count = 0
                print("Invalid number. Please try again.")
        except ValueError:
            count = 0
            print("Please enter a valid number or 'refresh'...")

    # user choices for random and time offset
    local_is_random = yes_or_no("Do you want the track order to be randomized? (y/n): ")
    local_is_offset = yes_or_no("Do you want a 30 second offset for each song? (y/n): ")

    return local_uri, local_playlist_name, local_is_random, local_is_offset

def yes_or_no(prompt):
    """Keeps asking user for yes or no"""
    while True:
        try:
            answer = input(prompt).lower().strip()
            if answer in ('y', 'yes', "n", "no"):
                return answer == "y"
            print("Please respond with 'y' or 'n'...")
        except ValueError:
            return False

#setup and permissions--------------------------------------------------

scope = ("user-library-read user-read-playback-state user-read-currently-playing "
         "playlist-read-private user-modify-playback-state")

#user credentials
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="49ec0ed6ee984a9ba779dde3afe5dbb5",
                                               client_secret="d558d0eabcbb4d3eb9aec4b3622a3ec9",
                                               redirect_uri="http://127.0.0.1:8888/callback",
                                               scope=scope))

#user input--------------------------------------------------------
print("Welcome to the Shotify app!\n")

while True:
    #grab all user device info, send to device function, receive device ID back
    devices_grab = sp.devices()
    device_id = devices(devices_grab)

    if device_id is not None:
        break

while True:
    playlists_grab = sp.current_user_playlists(limit=25)
    uri, playlist_name, is_random, is_offset = user_information(playlists_grab)
    if uri:
        break
powerhour(uri, playlist_name, is_random, is_offset, device_id)

#todo 1 - pause execution somehow.  the user can pause from the device playing but the program should be able to also
#todo 2 - should we send a pause command if the program is forcefully stopped
#todo 3 - pause option upon restart?  you might not have access to the playing device to actually pause it
#todo 4 - add a christmas mode, maybe its own class?
