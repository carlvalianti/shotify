import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

# Christmas Power Hour Configuration
CHRISTMAS_PLAYLIST_URI = "spotify:playlist:3KmQlFPFNb1mpsF9mVkyZ8"
CHRISTMAS_PLAYLIST_NAME = "Christmas Power Hour"
SONG_DURATION = 3 #seconds

# ONLY list tracks with custom timings
# Format: "track name (or partial)": (start_ms, duration_seconds, play_full)
# Track names are case-insensitive and can be partial matches
# Any track not listed here will default to: start at 0s, play 60s
CUSTOM_TRACKS = {
    "Christmas Canon": (165000, 60, False),  # Start at 2:45
    "Thistlehair": (20000, 60, False),  # Start at 0:20
    "Has Got the Aids": (55000, 60, False),  # Start at 0:55
    "Same Old Lang": (160000, 60, False),  # Start at 2:40
    "Do They Know": (100000, 60, False),  # Start at 1:40
    "Grown-Up": (130000, 60, False),  # Start at 2:10
    "Twelve Pains": (115000, 60, False),  # Start at 1:55
    "Cherry Cherry": (120000, 60, False),  # Start at 2:00
    "Believe Josh": (158000, 60, False),  # Start at 2:38
    "Happy Hanukkah": (0, None, True),  # Play entire song
}


# Note: Total track count is retrieved dynamically from the playlist

def find_custom_settings(track_search_string):
    """
    Check if a track has custom settings by matching track name (and optionally artist).
    Returns (start_ms, duration_seconds, play_full) or None if no match.
    """
    if not track_search_string:
        return None

    search_string_lower = track_search_string.lower()

    # Check for partial matches (case-insensitive)
    for custom_name, settings in CUSTOM_TRACKS.items():
        if custom_name.lower() in search_string_lower:
            #print(f"   ✓ Matched '{custom_name}' in '{track_search_string}'")
            return settings

    return None


def christmas_powerhour(device_id):
    """Run the Christmas Power Hour with custom track timings."""

    print(f"\n🎄 Starting Christmas Power Hour! 🎄")
    print(f"Playing from '{CHRISTMAS_PLAYLIST_NAME}'")

    # Get playlist info and track count
    playlist = sp.playlist(playlist_id=CHRISTMAS_PLAYLIST_URI, additional_types=('track',))
    total_tracks = len(playlist['tracks']['items'])

    print(f"Total tracks: {total_tracks}\n")

    # Play all tracks in the playlist
    for track_index in range(total_tracks):
        song_number = track_index + 1
        is_last_song = (track_index == total_tracks - 1)

        # Get track name and artist
        track_item = playlist['tracks']['items'][track_index]
        if track_item.get('track'):
            track_name = track_item['track']['name']
            artists = track_item['track']['artists']
            artist_names = ', '.join([artist['name'] for artist in artists]) if artists else ""
            # Create searchable string with both track name and artists
            track_search_string = f"{track_name} - {artist_names}" if artist_names else track_name
        else:
            track_name = "Unknown"
            track_search_string = "Unknown"

        # Handle last song - always play in full
        if is_last_song:
            print(f"🎵 Track #{song_number}/{total_tracks} - '{track_name}' - [FINAL SONG] You made it!! 🎄")
            sp.start_playback(
                device_id=device_id,
                context_uri=CHRISTMAS_PLAYLIST_URI,
                offset={"position": track_index},
                position_ms=0
            )
            print("   🎅 Last song playing... waiting...")

            # Wait for the song to finish
            try:
                # Get the song duration
                track_duration_ms = track_item['track']['duration_ms']
                track_duration_sec = track_duration_ms / 1000

                # Sleep for the duration (with a small buffer)
                time.sleep(track_duration_sec + 2)

            except Exception as e:
                print(f"   Note: Couldn't get track duration, waiting 5 minutes max - {e}")
                time.sleep(300)

            break

        # Check if this track has custom settings
        custom_settings = find_custom_settings(track_search_string)

        if custom_settings:
            start_ms, duration_seconds, play_full = custom_settings

            if play_full:
                print(f"🎵 Track #{song_number}/{total_tracks} - '{track_name}' - Playing FULL SONG ⭐")
                sp.start_playback(
                    device_id=device_id,
                    context_uri=CHRISTMAS_PLAYLIST_URI,
                    offset={"position": track_index},
                    position_ms=start_ms
                )
                # Wait for song to finish (you could also just let it play and move on manually)
                print("   ⏸️  Press Ctrl+C when ready for next track, or wait for song to end...")
                try:
                    # Sleep for a long time - user will Ctrl+C or let it finish
                    time.sleep(600)  # 10 minutes max
                except KeyboardInterrupt:
                    print("   ⏭️  Moving to next track...")
            else:
                # Convert start time to readable format
                start_min = start_ms // 60000
                start_sec = (start_ms % 60000) // 1000

                print(
                    f"🎵 Track #{song_number}/{total_tracks} - '{track_name}' - Starting at {start_min}:{start_sec:02d}, playing {duration_seconds}s ⭐")

                sp.start_playback(
                    device_id=device_id,
                    context_uri=CHRISTMAS_PLAYLIST_URI,
                    offset={"position": track_index},
                    position_ms=start_ms
                )

                # Wait for the specified duration
                time.sleep(duration_seconds)
        else:
            # Default behavior: start at 0s, play 60s
            print(f"🎵 Track #{song_number}/{total_tracks} - '{track_name}' - Starting at 0:00, playing 60s")

            sp.start_playback(
                device_id=device_id,
                context_uri=CHRISTMAS_PLAYLIST_URI,
                offset={"position": track_index},
                position_ms=0
            )

            time.sleep(SONG_DURATION)

    print(f"\n🎅 Christmas Power Hour Complete! Merry Christmas! 🎅\n")


def select_device(user_devices):
    """Handles device selection with refresh support."""
    while True:
        device_info = []
        count = 0

        # Grab and store all of user's devices (name, id) tuples in a list
        for item in user_devices["devices"]:
            new_device_tuple = (item["name"], item["id"])
            device_info.append(new_device_tuple)

        if not device_info:
            print("❌ No devices found. Please open Spotify on a device and try again.")
            input("Press Enter to refresh...")
            return None

        # Display list of available device options
        print("Available Devices:\n")
        for item in device_info:
            count += 1
            print(f"{count}. {item[0]}")

        choice = input(
            "\nWhich device # would you like to play? "
            "(Enter 'refresh' to update list, or # to select): ").strip().lower()

        if choice == "refresh":
            return None

        # Get device ID for user selected device
        try:
            device_choice = int(choice) - 1

            if 0 <= device_choice < len(device_info):
                selected_name = device_info[device_choice][0]
                local_device_id = device_info[device_choice][1]
                print(f"✅ Playing on '{selected_name}'\n")
                return local_device_id
            else:
                print("❌ Invalid number. Please try again.")

        except ValueError:
            print("❌ Please enter a valid number...")


# Setup and permissions
scope = ("user-library-read user-read-playback-state user-read-currently-playing "
         "playlist-read-private user-modify-playback-state")

# User credentials (same as main.py)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="49ec0ed6ee984a9ba779dde3afe5dbb5",
    client_secret="d558d0eabcbb4d3eb9aec4b3622a3ec9",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope=scope))

# Main execution
if __name__ == "__main__":
    print("🎄 Welcome to the Christmas Power Hour! 🎄\n")

    # Device selection
    while True:
        devices_grab = sp.devices()
        device_id = select_device(devices_grab)
        if device_id is not None:
            break

    # Confirm before starting
    confirm = input("Ready to start? (y/n): ").strip().lower()
    if confirm in ('y', 'yes'):
        christmas_powerhour(device_id)
    else:
        print("Christmas Power Hour cancelled. Happy Holidays! 🎁")