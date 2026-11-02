# AI vs NYT Connections

Eight free AI models played ten rounds of Connections, one guess at a time, with strikes. Five rounds were published NYT puzzles (2026) and five were custom puzzles I built.

- **Article:** [Making Connections: Artificial Intelligence meets Abstract Ingenuity using NYT Connections](ADD-SUBSTACK-LINK)
- **Deck:** see `docs/` (PDF)
- **Chat transcripts:** available on request; contact me via [LinkedIn](https://www.linkedin.com/in/uyiuwadiae).

## Headline results

| Result | Value |
|---|---|
| Top models | Gemini and Claude, 30 of 40 possible connections |
| NYT puzzles | 145 of 160 connections found (91%) across all models |
| Custom puzzles | 61 of 160 connections found (38%) across all models |
| Last three custom puzzles | 14 of 96 (15%) |
| Mistakes | 38 on NYT puzzles, 137 on custom puzzles |

## Repo layout

- `data/guesses.csv`: one row per guess (model, round, puzzle type, guess number, result, color if correct)
- `data/rounds.csv`: one row per model and round (guesses, connections found, one-aways, wrong guesses, mistakes, solved, perfect)
- `data/puzzles.csv`: puzzle names or NYT dates, type, and human solve rates where available
- `data/models.csv`: model versions, tier and thinking mode
- `analysis/analyze.py`: recomputes every metric and redraws all charts
- `charts/`: chart images with the data behind each one
- `docs/methodology.md`, `docs/limitations.md`

## Reproduce

```
pip install -r analysis/requirements.txt
python analysis/analyze.py
```

The script prints a check of the published numbers against the CSVs, then writes the charts.

## Definitions

- **Result:** `Y` correct connection, `1` one away (three of four right), `N` wrong. A `1` or an `N` is a mistake. Four mistakes ends the round.
- **Solved:** all four connections found. **Perfect:** solved with no mistakes.
- **Partial credit:** 1 point per connection found plus 0.5 per one-away.
- **Purple first:** the first guess of the round was a correct Purple connection.

## What is not in this repo

Custom puzzle answers and NYT puzzle grids and solutions are left out so the puzzles stay playable. NYT puzzles are referenced by date only. Human solve rates for NYT puzzles come from u/conchis-ness.

## License and citation

Code: MIT (LICENSE). Data and charts: CC BY 4.0. See CITATION.cff.
