import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from song_list import CUSTOM_TRACKS

# Christmas Power Hour Configuration
CHRISTMAS_PLAYLIST_URI = "spotify:playlist:3KmQlFPFNb1mpsF9mVkyZ8"
CHRISTMAS_PLAYLIST_NAME = "Christmas Power Hour"
SONG_DURATION = 60  # seconds - Change to 60 for real power hour


# Note: Total track count is retrieved dynamically from the playlist


def save_progress(track_index, track_name, total_tracks):
    """Save current progress to file."""
    try:
        with open('powerhour_progress.txt', 'w') as f:
            f.write(f"Last played: Track #{track_index + 1}/{total_tracks}\n")
            f.write(f"Track name: {track_name}\n")
    except Exception as e:
        # Don't crash the program if file write fails
        print(f"   Note: Couldn't save progress - {e}")


def read_last_progress():
    """Read last saved progress if it exists."""
    try:
        with open('powerhour_progress.txt', 'r') as f:
            content = f.read()
            print("\n📄 Last session progress found:")
            print(content)
            return True
    except FileNotFoundError:
        return False


def get_starting_track(total_tracks):
    """Ask user if they want to start from a specific track."""
    while True:
        choice = input(
            f"\nStart from beginning or specific track? (Enter track # 1-{total_tracks}, or press Enter for beginning): ").strip()

        if choice == "":
            return 0  # Start from beginning (index 0)

        try:
            track_num = int(choice)
            if 1 <= track_num <= total_tracks:
                print(f"✅ Starting from track #{track_num}")
                return track_num - 1  # Convert to 0-based index
            else:
                print(f"❌ Please enter a number between 1 and {total_tracks}")
        except ValueError:
            print("❌ Please enter a valid number or press Enter")


def find_custom_settings(track_search_string):
    """
    Check if a track has custom settings by matching track name (and optionally artist).
    Returns (start_ms, duration_seconds) or None if no match.
    """
    if not track_search_string:
        return None

    search_string_lower = track_search_string.lower()

    # Check for partial matches (case-insensitive)
    for custom_name, settings in CUSTOM_TRACKS.items():
        if custom_name.lower() in search_string_lower:
            # print(f"   ✓ Matched '{custom_name}' in '{track_search_string}'")  # Uncomment for debugging
            return settings

    return None


def christmas_powerhour(device_id, start_index=0):
    """Run the Christmas Power Hour with custom track timings."""

    print(f"\n🎄 Starting Christmas Power Hour! 🎄")
    print(f"Playing from '{CHRISTMAS_PLAYLIST_NAME}'")

    # Get playlist info and track count
    playlist = sp.playlist(playlist_id=CHRISTMAS_PLAYLIST_URI, additional_types=('track',))
    total_tracks = len(playlist['tracks']['items'])

    print(f"Total tracks: {total_tracks}\n")

    if start_index > 0:
        print(f"⏩ Skipping to track #{start_index + 1}\n")

    # Play all tracks in the playlist (starting from start_index)
    for track_index in range(start_index, total_tracks):
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

        # Save progress before playing track
        save_progress(track_index, track_name, total_tracks)

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

                # Sleep for the duration minus 5 seconds
                track_duration_sec = (track_duration_ms / 1000) - 5
                time.sleep(track_duration_sec)

                # Pause music after last song but before break
                sp.pause_playback(device_id=device_id)

            except Exception as e:
                print(f"   Note: Couldn't get track duration, waiting 5 minutes max - {e}")
                time.sleep(300)

            break

        # Check if this track has custom settings
        custom_settings = find_custom_settings(track_search_string)

        if custom_settings:
            start_ms, duration_seconds = custom_settings

            # Calculate start time in minutes and seconds
            start_min = start_ms // 60000
            start_sec = (start_ms % 60000) // 1000

            # Calculate stop time in milliseconds
            stop_ms = start_ms + (duration_seconds * 1000)

            # Convert stop time to minutes and seconds
            stop_min = stop_ms // 60000
            stop_sec = (stop_ms % 60000) // 1000

            # Print the log with stop time included
            print(
                f"🎵 Track #{song_number}/{total_tracks} - '{track_name}' - Starting at {start_min}:{start_sec:02d}, "
                f"playing {duration_seconds}s, stopping at {stop_min}:{stop_sec:02d} ⭐")

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

    # Show last progress if available
    read_last_progress()

    # Get playlist info to show track count
    temp_playlist = sp.playlist(playlist_id=CHRISTMAS_PLAYLIST_URI, additional_types=('track',))
    total_tracks = len(temp_playlist['tracks']['items'])

    # Get starting track
    start_index = get_starting_track(total_tracks)

    # Confirm before starting
    confirm = input("\nReady to start on ? (y/n): ").strip().lower()
    if confirm in ('y', 'yes'):
        christmas_powerhour(device_id, start_index)
    else:
        print("Christmas Power Hour cancelled. Happy Holidays! 🎁")