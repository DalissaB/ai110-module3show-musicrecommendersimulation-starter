"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

MAX_SCORE = 7.0

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


def print_recommendations(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print a formatted top-k list for one named taste profile."""
    print("\n" + "=" * 52)
    print(f"  TOP RECOMMENDATIONS - {name}")
    print(
        f"  Taste: {user_prefs['favorite_genre']} / "
        f"{user_prefs['favorite_mood']} / "
        f"energy {user_prefs['target_energy']} / "
        f"acoustic={user_prefs['likes_acoustic']}"
    )
    print("=" * 52)

    for rank, (song, score, explanation) in enumerate(
        recommend_songs(user_prefs, songs, k=k), start=1
    ):
        confidence = score / MAX_SCORE * 100
        print(f"\n{rank}. {song['title']} - {song['artist']}")
        print(f"   Score: {score:.2f} / {MAX_SCORE:.0f}  ({confidence:.0f}% match)")
        print("   Reasons:")
        for reason in explanation.split("; "):
            print(f"     - {reason}")

    print("\n" + "=" * 52)


def main() -> None:
    songs = load_songs("data/songs.csv")

    for name, user_prefs in PROFILES.items():
        print_recommendations(name, user_prefs, songs)


if __name__ == "__main__":
    main()
