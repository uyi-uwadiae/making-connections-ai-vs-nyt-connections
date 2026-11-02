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
> PASTE THE EXACT PROMPT USED HERE.

## Metrics
See the definitions in the README. Accuracy is connections found divided by total guesses. The comeback metric counts solved rounds with three mistakes. Reverse rainbows are Purple, Blue, Green, Yellow with no mistakes.
