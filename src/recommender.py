import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Score every song against the user, sort highest-first, return the top k."""
        ranked = sorted(
            self.songs,
            key=lambda song: score_song(asdict(user), asdict(song))[0],
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a readable string of the song's score and the reasons behind it."""
        score, reasons = score_song(asdict(user), asdict(song))
        detail = "; ".join(reasons) if reasons else "no strong matches"
        return f"Score {score:.2f}/7 - {detail}"

def load_songs(csv_path: str) -> List[Dict]:
    """Read the CSV into a list of song dicts, converting numeric columns to numbers."""
    int_fields = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness"}

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip blank lines that DictReader may return as empty rows.
            if not row or not row.get("id"):
                continue
            song: Dict = {}
            for key, value in row.items():
                if key in int_fields:
                    song[key] = int(value)
                elif key in float_fields:
                    song[key] = float(value)
                else:
                    song[key] = value
            songs.append(song)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the user's prefs (max 7.0), returning (score, reasons)."""
    score = 0.0
    reasons: List[str] = []

    # --- Genre (categorical, weight 3.0) ---
    if user_prefs["favorite_genre"] == song["genre"]:
        score += 3.0
        reasons.append(f"genre match: {song['genre']} (+3.0)")

    # --- Mood (categorical, weight 2.0) ---
    if user_prefs["favorite_mood"] == song["mood"]:
        score += 2.0
        reasons.append(f"mood match: {song['mood']} (+2.0)")

    # --- Energy (numeric, weight 1.0, rewards closeness) ---
    energy_points = 1.0 - abs(user_prefs["target_energy"] - song["energy"])
    score += energy_points
    reasons.append(
        f"energy close to {user_prefs['target_energy']} "
        f"(song {song['energy']}) (+{energy_points:.2f})"
    )

    # --- Acoustic-ness (boolean preference vs numeric feature, weight 1.0) ---
    song_is_acoustic = song["acousticness"] > 0.5
    if user_prefs["likes_acoustic"] == song_is_acoustic:
        score += 1.0
        if song_is_acoustic:
            reasons.append("you like acoustic and this song is acoustic (+1.0)")
        else:
            reasons.append("you prefer non-acoustic and this song is non-acoustic (+1.0)")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs, sort highest-first, and return the top k as (song, score, explanation)."""
    # Score every song. Each item is (song, score, explanation).
    scored = [
        (song, *score_and_explain(user_prefs, song))
        for song in songs
    ]

    # Sort by score (index 1), highest first.
    scored.sort(key=lambda item: item[1], reverse=True)

    # Cut to the top k.
    return scored[:k]


def score_and_explain(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """Helper: run score_song and turn its reasons list into one string."""
    score, reasons = score_song(user_prefs, song)
    explanation = "; ".join(reasons) if reasons else "no strong matches"
    return score, explanation
