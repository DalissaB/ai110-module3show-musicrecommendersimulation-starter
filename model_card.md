# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

**VibeMatch 1.0**

It matches songs to your vibe. That is the whole idea in the name.

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

VibeMatch suggests songs that fit your taste. You tell it what you like. It gives you a ranked list of songs back.

It assumes you can name one favorite genre, one favorite mood, an energy level, and if you like acoustic music. It assumes your taste fits into those four things.

This is for classroom exploration, not real users. It is a small simulation to learn how recommenders work. It is not meant to be a real app.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

Each song has a few tags. It has a genre, a mood, an energy number, and how acoustic it is.

You have a profile too. You pick a favorite genre, a favorite mood, a target energy, and if you like acoustic songs.

The model gives each song points. A matching genre is worth 3 points. A matching mood is worth 2 points. Energy is worth up to 1 point, based on how close the song is to what you want. Acoustic is worth 1 point if it matches. The most a song can get is 7 points.

Then it sorts all the songs from highest points to lowest. It hands back the top few. That is your recommendation list.

I changed the starter code a lot. The starter just returned the first songs and had empty functions. I wrote the real scoring, the sorting, the CSV loader, and a reason for every song so you can see why it was picked.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog has 18 songs. It is small on purpose.

The genres include pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip hop, classical, reggaeton, country, metal, and folk. The moods include happy, chill, intense, moody, relaxed, focused, bittersweet, playful, party, confident, melancholy, nostalgic, angry, and hopeful.

I added songs to the starter file. I added 3 real songs by Taylor Swift, Bad Bunny, and Role Model. I also added a few made-up songs to cover more genres. I removed 3 of my made-up songs so the list stayed diverse.

A lot of taste is missing. There are only a few songs per genre. There are no lyrics, no language info, and no year or culture data. So the model does not really know a song, it only knows a few tags.

Also, the audio numbers for the real songs are my estimates. I guessed them from how the songs sound, so they are not exact.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

It works well for clear, single-genre tastes. When I asked for chill lofi, I got calm lofi songs. When I asked for intense rock, I got Storm Runner at the top. That felt right.

It captures energy well. It groups loud songs together and calm songs together. It does not just pick the highest energy song, it picks the song closest to what you want.

The reasons matched my intuition. Every pick shows why it was chosen. When Cruel Summer scored 99% for my taste, the reasons made total sense (pop, bittersweet, right energy). It is easy to trust because you can see the math.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

One weakness I found during my experiments is that my genre matching is brittle because it only checks for an exact text match. When I tested a profile that asked for "Pop" with a capital P instead of "pop," none of the pop songs earned their genre points, and my top match dropped from about 6.98 out of 7 all the way down to 3.98 just because of one capital letter. This matters because genre is worth 3 out of my 7 total points, so the single most important feature quietly stopped working without any error or warning. The same thing happens with near-genres, like a "pop" fan never matching "indie pop," so the system unfairly buries songs that a real person would obviously count as pop. To fix it I would lowercase both sides before comparing and maybe group similar genres together so small labeling differences don't throw off the whole recommendation.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

**Profiles I tested.** I built four "normal" profiles to compare against each other: My Taste (pop / bittersweet / energy 0.65 / not acoustic), High-Energy Pop (pop / happy / energy 0.9 / not acoustic), Chill Lofi (lofi / chill / energy 0.35 / acoustic), and Deep Intense Rock (rock / intense / energy 0.9 / not acoustic). For each one I looked at the top 5 songs and checked whether they actually matched the vibe I asked for, and whether the reasons the program printed made sense.

**What surprised me.** The biggest surprise was that High-Energy Pop and Deep Intense Rock, which sound like totally different tastes, actually shared a lot of the same songs in their top 5 (Gym Hero and Sunrise City showed up in both). That happens because they both ask for high energy (0.9), so the energy points pull the same loud songs into both lists even though the genres are different. It made me realize energy is doing more work than I thought, and genre is really just the tiebreaker that decides which one lands at #1.

**Comparing each pair of profiles:**

- **My Taste vs High-Energy Pop:** Both are pop, so they surface the same three pop songs, but the order flips — My Taste puts Cruel Summer #1 (its bittersweet mood matches) while High-Energy Pop puts Sunrise City #1 (happy mood + higher energy). This makes sense: same genre pool, but mood and energy re-rank it.
- **My Taste vs Chill Lofi:** Almost no overlap. My Taste returns upbeat pop, Chill Lofi returns calm lofi like Library Rain and Midnight Coding. This makes sense because the genre, the low energy, and the acoustic preference all point the opposite direction.
- **My Taste vs Deep Intense Rock:** My Taste tops out with Cruel Summer (pop), while Deep Intense Rock tops with Storm Runner (rock/intense). They only share a song lower down (Sunrise City) because of energy, not because they like the same music. Makes sense — different genre and much higher target energy.
- **High-Energy Pop vs Chill Lofi:** These are near opposites. High-Energy Pop wants loud, non-acoustic songs and Chill Lofi wants quiet, acoustic ones, so their lists don't overlap at all. This is exactly what I'd expect from flipping energy from 0.9 to 0.35 and acoustic from False to True.
- **High-Energy Pop vs Deep Intense Rock:** Both want energy 0.9 and non-acoustic, so they share the loud songs (Gym Hero, Sunrise City), but the genre match decides the winner — pop for one, rock for the other. This shows energy groups the "loud" songs together and genre breaks the tie.
- **Chill Lofi vs Deep Intense Rock:** The most extreme opposites. One is low energy, chill, and acoustic; the other is high energy, intense, and not acoustic. They share zero songs, which confirms the scoring really does separate calm music from loud music.

Overall the outputs looked valid — each profile got music that matched its vibe, and the differences between profiles lined up with which preferences I changed.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

I would let users pick more than one genre. My taste is pop and reggaeton, but right now I can only pick one.

I would fix the bugs I found. I would lowercase the text so "Pop" and "pop" match. I would also stop energy from going out of the 0 to 1 range.

I would add more features, like tempo, valence, and danceability. That would make the matches richer.

I would make the top list more diverse. Right now it can give me five very similar songs. I could add a rule so it mixes in some variety.

I would also grow the catalog. More songs would mean better and more surprising picks.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

I learned that a recommender is really just math on data. It gives points and sorts. There is no magic. It only knows what you feed it.

The interesting part was the weights. Changing how much genre is worth totally changed my results. Small choices by the person who builds it have a big effect.

I also learned that bias sneaks in easily. My model buries reggaeton just because I picked pop as my one genre. I did not mean to, but the design did it.

This changed how I see apps like Spotify. When it feels like it "gets me," it is really just matching tags and guessing. And when it keeps showing me the same kind of song, that is the filter bubble I built in my own tiny version too.
