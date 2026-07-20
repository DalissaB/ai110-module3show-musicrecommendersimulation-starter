"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # My taste profile
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "bittersweet",
        "target_energy": 0.65,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    MAX_SCORE = 7.0

    # Header showing the profile we recommended for.
    print("\n" + "=" * 52)
    print("  TOP RECOMMENDATIONS FOR YOU")
    print(
        f"  Taste: {user_prefs['favorite_genre']} / "
        f"{user_prefs['favorite_mood']} / "
        f"energy {user_prefs['target_energy']} / "
        f"acoustic={user_prefs['likes_acoustic']}"
    )
    print("=" * 52)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        confidence = score / MAX_SCORE * 100
        print(f"\n{rank}. {song['title']} - {song['artist']}")
        print(f"   Score: {score:.2f} / {MAX_SCORE:.0f}  ({confidence:.0f}% match)")
        print("   Reasons:")
        for reason in explanation.split("; "):
            print(f"     - {reason}")

    print("\n" + "=" * 52 + "\n")


if __name__ == "__main__":
    main()
