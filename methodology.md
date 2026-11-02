# Methodology

## Models
Free versions of Gemini, Claude, Vibe by Mistral, DeepSeek, Copilot, ChatGPT, Muse Spark and Grok, with thinking or reasoning mode turned on for every model that offers one. Grok has none. Versions are in `data/models.csv`. Copilot does not disclose a version number. One run per model.

## Puzzles
- Rounds 1 to 5: published NYT Connections puzzles from 2026 (July 1, July 2, August 24, August 28, September 2), chosen from the hardest of the past quarter by human solve rate (34.8% to 43.7%).
- Rounds 6 to 10: custom puzzles I built. What We Really Need (29% human solve rate) and Treasure Chest (39%) had already been played by others. Numbers Game, Calculated Guess and New Testament were unpublished at the time.

## Rules
1. The model sees 16 terms and guesses one group of four at a time, explaining its reasoning.
2. I reply `Y` (correct, plus the connection), `1` (one away) or `N`.
3. A `1` or `N` is a mistake. Four mistakes ends the round.
4. After every round the full solution is revealed, solved or not.
5. No looking up solutions online. Looking up unfamiliar terms was allowed.
6. Models were encouraged to try Purple first and to guess on "vibes" if they could not pinpoint a connection.

## Instruction prompt
> I'd like to see if you can solve NYT Connections puzzles.
> 
> I'll send a set of 16 terms and you are to group them into 4 groups of 4 based on a theme that connects each individual group. 
>
> Respond with one connection (Group of 4) at a time and I'll let you know if it's correct (Y), if you have 3/4 of the group which means that you're one away (1), or if it's incorrect (N). When you have a Group of 4 Connections correct, those 4 are removed from the remain pool of terms
> 
> When you get a connection correct, I'll respond with Y and what the connection is.
> 
> Give your thoughts on what you think the connection between the terms is when you guess each time, even if it's just that you're going off vibes.

Don't be afraid to just guess if you're struggling

Since you're probably going to try to "pre-solve" before making guesses, you can try getting "Purple first," that is guessing the most difficult/trickiest connection first.

At the end of each puzzle, I'll reveal the connections, whether you get them all right or not, so that you know the actual solution and can learn from it, perhaps it will help you with future games. Feel free to reply with your thoughts on the puzzle after I send the solution, before we begin the next round.

You can make 4 mistakes (my response or either 1 or N is a mistake) at which point the round is over. We will do 10 rounds, that is 10 Connections games. The first 5 are Connections games that the NYT has published, and the second 5 are Connections games I crafted myself.

Do not look up the solutions online but you can look up the terms you're unfamiliar with. 

Before we begin, do you understand this exercise and do you have any clarifying questions?


## Metrics
See the definitions in the README. Accuracy is connections found divided by total guesses. The comeback metric counts solved rounds with three mistakes. Reverse rainbows are Purple, Blue, Green, Yellow with no mistakes.
