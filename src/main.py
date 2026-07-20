"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import textwrap

from src.recommender import load_songs, recommend_songs

MAX_SCORE = 7.0

# (heading, width) for each column of the recommendations table.
COLUMNS = [
    ("#", 3),
    ("Song", 28),
    ("Artist", 14),
    ("Score", 7),
    ("Match", 6),
    ("Reasons", 46),
]

# A few distinct taste profiles to try out the recommender with.
PROFILES = {
    "My Taste": {
        "favorite_genre": "pop",
        "favorite_mood": "bittersweet",
        "target_energy": 0.65,
        "likes_acoustic": False,
    },
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.9,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.9,
        "likes_acoustic": False,
    },
}


def _fit(text: str, width: int) -> str:
    """Pad text to width, or truncate with an ellipsis if it is too long."""
    text = str(text)
    if len(text) > width:
        return text[: width - 1] + "…"
    return text.ljust(width)


def _border(left: str, mid: str, right: str) -> str:
    """Build a horizontal table border line, e.g. ├────┼────┤."""
    return left + mid.join("─" * (w + 2) for _, w in COLUMNS) + right


def _row(values) -> str:
    """Build one table row: │ padded │ padded │ ... │."""
    cells = (_fit(v, w) for v, (_, w) in zip(values, COLUMNS))
    return "│ " + " │ ".join(cells) + " │"


def print_recommendations(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print a formatted table of the top-k songs for one named taste profile."""
    # Heading describing the profile we are recommending for.
    print(f"\nTOP RECOMMENDATIONS - {name}")
    print(
        f"Taste: {user_prefs['favorite_genre']} / "
        f"{user_prefs['favorite_mood']} / "
        f"energy {user_prefs['target_energy']} / "
        f"acoustic={user_prefs['likes_acoustic']}"
    )

    reason_width = COLUMNS[-1][1]

    print(_border("┌", "┬", "┐"))
    print(_row(heading for heading, _ in COLUMNS))
    print(_border("├", "┼", "┤"))

    recommendations = recommend_songs(user_prefs, songs, k=k)
    last = len(recommendations) - 1
    for rank, (song, score, explanation) in enumerate(recommendations):
        match = f"{score / MAX_SCORE * 100:.0f}%"
        score_text = f"{score:.2f}/{MAX_SCORE:.0f}"

        # Wrap each reason so long ones span multiple lines instead of truncating.
        reason_lines = []
        for reason in explanation.split("; "):
            reason_lines.extend(textwrap.wrap(reason, reason_width) or [""])

        # First line carries the song info; extra reason lines continue below it.
        print(_row([rank + 1, song["title"], song["artist"], score_text, match, reason_lines[0]]))
        for extra in reason_lines[1:]:
            print(_row(["", "", "", "", "", extra]))

        # Separator between songs, but close the table on the last one.
        if rank == last:
            print(_border("└", "┴", "┘"))
        else:
            print(_border("├", "┼", "┤"))


def main() -> None:
    songs = load_songs("data/songs.csv")

    for name, user_prefs in PROFILES.items():
        print_recommendations(name, user_prefs, songs)


if __name__ == "__main__":
    main()
