# ONLY list tracks with custom timings
# Format: "track name (or partial)": (start_ms, duration_seconds)
# Track names are case-insensitive and can be partial matches
# Any track not listed here will default to: start at 0s, play 60s

CUSTOM_TRACKS = {
    "Mariah Carey": (0, 101),  # Play for 101 seconds, stop at 1:41
    "Mathis": (0, 62),  # Play for 62 seconds, stop at 1:02
    "Christmas Canon": (165000, 66),  # Start at 2:45, play for 66 seconds, stop at 3:51
    "Kitt": (0, 59),  # Play for 59 seconds, stop at 0:59
    "Paisley": (15000, 61),  # Start at 0:15, play for 61 seconds, stop at 1:16
    "Thurl": (0, 57),  # Play for 57 seconds, stop at 0:57
    "Back Door": (25000, 70),  # Start at 0:25, play for 70 seconds, stop at 1:35
    "Bruce": (30000, 66),  # Start at 0:30, play for 66 seconds, stop at 1:36
    "Has Got the Aids": (55000, 68),  # Start at 0:55, play for 68 seconds, stop at 2:03
    "Same Old Lang": (158000, 56),  # Start at 2:39, play for 56 seconds, stop at 3:35
    "Kalikimaka": (5000, 61),  # Start at 0:05, play for 61 seconds, stop at 1:06
    "Nuttin": (3000, 61),  # Start at 0:03, play for 61 seconds, stop at 1:04
    "Streisand": (0, 62),  # Play for 62 seconds, stop at 1:02
    "Boomers": (0, 76),  # Play for 76 seconds, stop at 1:16
    "Andy Williams": (0, 65),  # Play for 65 seconds, stop at 1:05
    "Ariana": (9000, 62),  # Start at 0:09, play for 62 seconds, stop at 1:11
    "Band Aid": (106000, 66),  # Start at 1:46, play for 66 seconds, stop at 2:52
    #"Brenda Lee": (0, 61),  # Play for 61 seconds, stop at 1:01
    "Daryl Hall": (0, 67),  # Play for 67 seconds, stop at 1:07
    "Thistlehair": (19000, 63),  # Start at 0:19, play for 63 seconds, stop at 1:22
    "Burl Ives": (0, 68),  # Play for 68 seconds, stop at 1:08
    "XXX": (3000, 60),  # Start at 0:03, play for 60 seconds, stop at 1:03
    "Step Into Christmas": (14000, 61),  # Start at 0:14, play for 61 seconds, stop at 1:15
    "John Denver": (0, 70),  # Play for 70 seconds, stop at 1:10
    "Feliz Navidad": (0, 64),  # Play for 64 seconds, stop at 1:04
    "Grown-Up": (130000, 61),  # Start at 2:10, play for 61 seconds, stop at 3:11
    "The Chimney Song": (0, 59),  # Play for 59 seconds, stop at 0:59
    "Wonderful Christmastime": (0, 62),  # Play for 62 seconds, stop at 1:02
    "Twelve Pains": (115000, 69),  # Start at 1:55, play for 69 seconds, stop at 3:04
    "Lady Gaga": (8000, 58),  # Start at 0:08, play for 58 seconds, stop at 1:06
    "Italian Jingle Bells": (0, 59),  # Play for 59 seconds, stop at 0:59
    "Patapan": (0, 71),  # Play for 71 seconds, stop at 1:11
    "Cherry Cherry": (121000, 83),  # Start at 2:01, play for 83 seconds, stop at 3:24
    "Puppies Are Forever": (0, 59),  # Play for 59 seconds, stop at 0:59
    "Santa Went Crazy": (15000, 66),  # Start at 0:15, play for 66 seconds, stop at 1:21
    "Merry Christmas, Happy Holidays": (20000, 71),  # Start at 0:20, play for 71 seconds, stop at 1:31
    "The Christmas Queen": (8000, 68),  # Start at 0:08, play for 68 seconds, stop at 1:16
    "William Hung": (0, 66),  # Play for 66 seconds, stop at 1:06 (revisit)
    "I Guess It's Christmas": (85000, 68),  # Start at 1:25, play for 68 seconds, stop at 2:33 (double check)
    "Carrie Underwood": (175000, 61),  # Start at 2:55, play for 61 seconds, stop at 3:56
    "Happy Hanukkah": (0, 167),  # Play almost full song, stop at 2:47
    "Justin Bieber": (50000, 60),  # Start at 0:50, play for 60 seconds, stop at 1:50
    "I Saw Mommy": (20000, 61),  # Start at 0:20, play for 61 seconds, stop at 1:21
    "Hippopoptamus": (3000, 61),  # Start at 0:03, play for 61 seconds, stop at 1:04
    "Mary, Did You Know": (67000, 69),  # Start at 1:07, play for 70 seconds, stop at 2:17
    "Happy Birthday Jesus": (10000, 63),  # Start at 0:10, play for 63 seconds, stop at 1:13
    "Jackson 5": (3000, 62),  # Start at 0:03, play for 62 seconds, stop at 1:05
    "Shake Them Bells": (10000, 66),  # Start at 0:10, play for 66 seconds, stop at 1:16
    "Sleigh Ride": (10000, 64),  # Start at 0:10, play for 64 seconds, stop at 1:14
    "Who Put the Stump": (13000, 69),  # Start at 0:13, play for 69 seconds, stop at 1:22
    "What Christmas Means To Me": (9000, 66),  # Start at 0:09, play for 66 seconds, stop at 1:15
    "Believe": (158000, 61),  # Start at 2:38, play for 61 seconds, stop at 3:39
    "Wizards in Winter": (120000, 61),  # Start at 2:00, play for 61 seconds, stop at 3:01
    "DMX": (0, 64),  # Play for 64 seconds, stop at 1:04
    "Augie Rios": (6000, 62),  # Start at 0:06, play for 62 seconds, stop at 1:08
    "Sarajevo": (124000, 67),  # Start at 2:04, play for 67 seconds, stop at 3:11
    "Philly Specials": (14000, 63),  # Start at 0:14, play for 63 seconds, stop at 1:17
    "The First": (106000, 66),  # Start at 1:46, play for 66 seconds, stop at 2:52
#Extra 175 seconds
}