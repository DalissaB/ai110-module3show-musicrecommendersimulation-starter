# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

From what I looked into, real platforms like Spotify and YouTube basically guess what you'll like next by watching two things: what other people with similar taste enjoy (collaborative filtering) and what a song is actually made of, like its genre or energy (content-based filtering). They mix a ton of signals for this too, like likes, skips, how long you listen, playlists, tempo, and mood. My version is way simpler than that. I'm going content-based only, since I don't have a bunch of users to compare against. So instead of asking "what did people like you listen to," my recommender asks "how close is this song to what this one user already says they like?" It scores every song against the user's taste profile, and then it prioritizes the songs that match the user's genre and vibe first, and after that how close the song's feel (energy, acoustic-ness) is to what they want.

Here's the exact data my objects use:

**`Song` uses (loaded from `data/songs.csv`):**

- `genre` — e.g. pop, lofi, rock
- `mood` — e.g. happy, chill, intense
- `energy` — a 0 to 1 number for how intense it feels
- `acousticness` — a 0 to 1 number for acoustic vs electronic

**`UserProfile` stores (the person's taste):**

- `favorite_genre` — the genre they want
- `favorite_mood` — the mood they want
- `target_energy` — the energy level they're going for (0 to 1)
- `likes_acoustic` — True or False for whether they like acoustic songs

**How the score works:** for each song I add up points, and each feature is weighted so the important stuff counts for more:

- **Genre match → 3 points.** This is worth the most because genre is the biggest deal in what a song actually *is*.
- **Mood match → 2 points.** Same idea as genre (do they match or not), just worth a little less.
- **Energy → up to 1 point.** Instead of "higher is better," I reward how *close* the song's energy is to what the user wants, using `1 - abs(user_energy - song_energy)`. So a perfect match gives 1 point and it drops off the further away it gets, in either direction (too intense is penalized the same as too calm).
- **Acoustic-ness → 1 point.** The user's `likes_acoustic` is True/False, so I turn the song into "is it acoustic?" (acousticness > 0.5) and give 1 point if that matches what they like.

Add those up and the highest a song can score is **7 points** (a perfect match on everything), so I can also show `score / 7` as a confidence percentage. Then I sort all the songs by their score, highest first, and hand back the top few. That sorting-and-cutting step is what actually turns a pile of scores into the short list of recommendations.

**Biases I expect from this scoring:**

- **Genre bias.** Genre is worth 3 out of 7 points, so it dominates. A song in my favorite genre almost always beats a great match from another genre, which reinforces the single-genre bubble and buries reggaeton when I set my genre to "pop."
- **Popularity/majority bias.** Since pop is common in my catalog, pop songs have more chances to score high, so rarer genres get pushed down just for being rare.
- **Mainstream-mood bias.** Common moods like "happy" match more songs than niche ones, so unusual moods get fewer matches even if I'd love those songs.
- **My own labeling bias.** I picked the moods and estimated the audio values myself, so my personal opinion of how a song "feels" is baked into the scores before any math even happens.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

```
====================================================
  TOP RECOMMENDATIONS FOR YOU
  Taste: pop / bittersweet / energy 0.65 / acoustic=False
====================================================

1. Cruel Summer - Taylor Swift
   Score: 6.95 / 7  (99% match)
   Reasons:
     - genre match: pop (+3.0)
     - mood match: bittersweet (+2.0)
     - energy close to 0.65 (song 0.7) (+0.95)
     - you prefer non-acoustic and this song is non-acoustic (+1.0)

2. Sunrise City - Neon Echo
   Score: 4.83 / 7  (69% match)
   Reasons:
     - genre match: pop (+3.0)
     - energy close to 0.65 (song 0.82) (+0.83)
     - you prefer non-acoustic and this song is non-acoustic (+1.0)

3. Gym Hero - Max Pulse
   Score: 4.72 / 7  (67% match)
   Reasons:
     - genre match: pop (+3.0)
     - energy close to 0.65 (song 0.93) (+0.72)
     - you prefer non-acoustic and this song is non-acoustic (+1.0)

4. Sally When the Wine Runs Out - Role Model
   Score: 1.99 / 7  (28% match)
   Reasons:
     - energy close to 0.65 (song 0.64) (+0.99)
     - you prefer non-acoustic and this song is non-acoustic (+1.0)

5. Titi Me Pregunto - Bad Bunny
   Score: 1.93 / 7  (28% match)
   Reasons:
     - energy close to 0.65 (song 0.72) (+0.93)
     - you prefer non-acoustic and this song is non-acoustic (+1.0)

====================================================
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

- It only picks one favorite genre, so it can't capture my multi-genre taste (I like pop AND reggaeton at the same time, but reggaeton scores lower when I set my genre to pop)
- It only works on a tiny catalog of 18 songs
- It does not understand lyrics or language, just numbers and tags
- It is content-based only, so it can't do "people like you also liked..." and might trap me in a bubble
- My audio values for the real songs are estimates, not exact Spotify data

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



