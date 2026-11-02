"""Reproduces every number and chart in the article and deck from data/*.csv.
Run from the repo root:  python analysis/analyze.py"""
import csv, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YEL, GRE, BLU, PUR = "#F9DF6D", "#A0C35A", "#B0C4EF", "#BA81C5"
plt.rcParams.update({"font.family": "DejaVu Sans", "figure.facecolor": "white",
                     "axes.facecolor": "white", "text.color": "black",
                     "axes.labelcolor": "black", "xtick.color": "black", "ytick.color": "black"})

def read(name):
    with open(os.path.join(ROOT, "data", name), newline="") as f:
        return list(csv.DictReader(f))

rounds, guesses, puzzles = read("rounds.csv"), read("guesses.csv"), read("puzzles.csv")
models = [r["model"] for r in read("models.csv")]
I = lambda x: int(x)

def agg(m):
    rs = [r for r in rounds if r["model"] == m]
    s = lambda k, t=None: sum(I(r[k]) for r in rs if t is None or r["puzzle_type"] == t)
    gs = [g for g in guesses if g["model"] == m]
    pf = sum(1 for g in gs if g["guess_number"] == "1" and g["color_if_correct"] == "Purple")
    return dict(model=m, found=s("connections_found"), nyt=s("connections_found", "NYT"),
                cus=s("connections_found", "Custom"), mist=s("mistakes"), one=s("one_away"),
                wins=s("solved"), nyt_wins=s("solved", "NYT"), cus_wins=s("solved", "Custom"),
                perfect=s("perfect"), guesses=s("guesses"), purple_first=pf,
                partial=s("connections_found") + 0.5 * s("one_away"),
                last3=sum(I(r["connections_found"]) for r in rs if I(r["round"]) >= 8))
A = {m: agg(m) for m in models}

# ---- reproducibility checks against published numbers
checks = [("Gemini connections", A["Gemini"]["found"], 30), ("Claude connections", A["Claude"]["found"], 30),
          ("NYT connections (all models)", sum(a["nyt"] for a in A.values()), 145),
          ("Custom connections (all models)", sum(a["cus"] for a in A.values()), 61),
          ("Last three custom puzzles", sum(a["last3"] for a in A.values()), 14),
          ("NYT mistakes", sum(I(r["mistakes"]) for r in rounds if r["puzzle_type"] == "NYT"), 38),
          ("Custom mistakes", sum(I(r["mistakes"]) for r in rounds if r["puzzle_type"] == "Custom"), 137),
          ("Claude partial credit", A["Claude"]["partial"], 34), ("Copilot connections", A["Copilot"]["found"], 26)]
ok = True
for n, got, want in checks:
    flag = "OK " if got == want else "MISMATCH"
    ok &= got == want
    print(f"{flag} {n}: {got} (published {want})")
print("All checks passed." if ok else "Some checks failed.")

# ---- tables
def order(key, rev=True, tie=("found",)):
    return sorted(models, key=lambda m: tuple(-A[m][k] if rev else A[m][k] for k in (key,) + tie))
def save_table(name, header, rows):
    with open(os.path.join(ROOT, "charts", name), "w", newline="") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)
def finish(fig, name):
    fig.savefig(os.path.join(ROOT, "charts", name), dpi=200, bbox_inches="tight"); plt.close(fig)

# 1 connections found (stacked)
o = order("found", tie=("cus",))
fig, ax = plt.subplots(figsize=(10, 6))
y = range(len(o))
ax.barh(y, [A[m]["nyt"] for m in o], color=BLU, label="NYT puzzles")
ax.barh(y, [A[m]["cus"] for m in o], left=[A[m]["nyt"] for m in o], color=PUR, label="Custom puzzles")
for i, m in enumerate(o):
    ax.text(A[m]["nyt"] / 2, i, A[m]["nyt"], ha="center", va="center", fontweight="bold")
    ax.text(A[m]["nyt"] + A[m]["cus"] / 2, i, A[m]["cus"], ha="center", va="center", fontweight="bold")
    ax.text(A[m]["found"] + 0.4, i, A[m]["found"], va="center", fontweight="bold")
ax.set_yticks(list(y)); ax.set_yticklabels(o); ax.invert_yaxis(); ax.set_xlim(0, 34)
ax.set_title("Gemini and Claude tied at the top with 30 of 40 connections", loc="left", fontweight="bold")
ax.legend(frameon=False, loc="lower right"); ax.spines[["top", "right"]].set_visible(False); ax.set_xticks([])
finish(fig, "connections_found.png")
save_table("connections_found.csv", ["model", "nyt_connections", "custom_connections", "total"], [[m, A[m]["nyt"], A[m]["cus"], A[m]["found"]] for m in o])

# 2 share found
tn, tc = sum(a["nyt"] for a in A.values()), sum(a["cus"] for a in A.values())
fig, ax = plt.subplots(figsize=(8, 6))
for i, (lab, v, c) in enumerate([("NYT puzzles", tn, BLU), ("Custom puzzles", tc, PUR)]):
    ax.bar(i, 100, color="white", edgecolor="black", linewidth=2, width=0.6)
    ax.bar(i, v / 160 * 100, color=c, width=0.6)
    ax.text(i, 104, f"{round(v/160*100)}%", ha="center", fontsize=24, fontweight="bold")
    ax.text(i, -9, f"{v} of 160 connections", ha="center")
ax.set_xticks([0, 1]); ax.set_xticklabels(["NYT puzzles", "Custom puzzles"], fontweight="bold")
ax.set_ylim(-12, 115); ax.set_yticks([]); ax.spines[["top", "right", "left"]].set_visible(False)
ax.set_title("AI found 91% of the NYT connections but only 38% of the custom ones", loc="left", fontweight="bold")
finish(fig, "share_found.png")
save_table("share_found.csv", ["puzzle_type", "connections_found", "possible", "percent"], [["NYT", tn, 160, round(tn/160*100)], ["Custom", tc, 160, round(tc/160*100)]])

# 3 games won
o = sorted(models, key=lambda m: (-A[m]["wins"], -A[m]["cus_wins"]))
fig, ax = plt.subplots(figsize=(10, 6)); y = range(len(o))
ax.barh(y, [A[m]["nyt_wins"] for m in o], color=BLU, label="NYT puzzles won (of 5)")
ax.barh(y, [A[m]["cus_wins"] for m in o], left=[A[m]["nyt_wins"] for m in o], color=PUR, label="Custom puzzles won (of 5)")
for i, m in enumerate(o):
    ax.text(A[m]["wins"] + 0.1, i, f'{A[m]["wins"]} of 10', va="center", fontweight="bold")
ax.set_yticks(list(y)); ax.set_yticklabels(o); ax.invert_yaxis(); ax.set_xlim(0, 9); ax.set_xticks([])
ax.set_title("Games won: Gemini and Claude won 7 of 10", loc="left", fontweight="bold")
ax.legend(frameon=False, loc="lower right"); ax.spines[["top", "right"]].set_visible(False)
finish(fig, "games_won.png")
save_table("games_won.csv", ["model", "nyt_wins_of_5", "custom_wins_of_5", "total_of_10"], [[m, A[m]["nyt_wins"], A[m]["cus_wins"], A[m]["wins"]] for m in o])

# 4 partial credit comparison (three panels, sorted by partial credit)
o = sorted(models, key=lambda m: (-A[m]["partial"], -A[m]["found"]))
fig, axs = plt.subplots(1, 3, figsize=(13, 6), sharey=True)
for ax, (k, t, c) in zip(axs, [("partial", "Partial credit points", YEL), ("mist", "Mistakes (fewer is better)", PUR), ("perfect", "Rounds with no mistakes", GRE)]):
    ax.barh(range(len(o)), [A[m][k] for m in o], color=c)
    for i, m in enumerate(o): ax.text(A[m][k] + 0.3, i, A[m][k], va="center", fontweight="bold")
    ax.set_title(t, fontweight="bold"); ax.spines[["top", "right", "bottom"]].set_visible(False); ax.set_xticks([])
    ax.set_xlim(0, max(A[m][k] for m in o) * 1.18)
axs[0].set_yticks(range(len(o))); axs[0].set_yticklabels(o); axs[0].invert_yaxis()
fig.suptitle("Partial credit (1 point per connection + 0.5 per one-away) reshuffles the middle of the pack", x=0.01, ha="left", fontweight="bold")
finish(fig, "partial_credit.png")
save_table("partial_credit.csv", ["model", "partial_credit", "mistakes", "perfect_rounds"], [[m, A[m]["partial"], A[m]["mist"], A[m]["perfect"]] for m in o])

# 5 purple first
o = sorted(models, key=lambda m: (-A[m]["purple_first"], -A[m]["found"]))
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(range(len(o)), [A[m]["purple_first"] for m in o], color=PUR)
for i, m in enumerate(o): ax.text(A[m]["purple_first"] + 0.1, i, A[m]["purple_first"], va="center", fontweight="bold")
ax.set_yticks(range(len(o))); ax.set_yticklabels(o); ax.invert_yaxis(); ax.set_xticks([]); ax.spines[["top", "right"]].set_visible(False)
ax.set_title("Gemini led with a correct Purple six times; ChatGPT and Grok never did", loc="left", fontweight="bold")
finish(fig, "purple_first.png")
save_table("purple_first.csv", ["model", "rounds_first_guess_correct_purple"], [[m, A[m]["purple_first"]] for m in o])

# 6 human solve rate vs models solved (NYT)
nyt = [p for p in puzzles if p["puzzle_type"] == "NYT"]
rows = []
for p in nyt:
    s = sum(I(r["solved"]) for r in rounds if r["round"] == p["round"])
    rows.append((p["puzzle"], float(p["human_solve_rate_pct"]), s))
rows.sort(key=lambda r: r[1])
fig, ax = plt.subplots(figsize=(10, 5))
for i, (d, h, s) in enumerate(rows):
    ax.barh(i, s, color=YEL if s < 8 else BLU)
    ax.text(s + 0.1, i, f"{s} of 8 models | humans {h:.1f}%", va="center", fontweight="bold")
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows]); ax.invert_yaxis(); ax.set_xlim(0, 12); ax.set_xticks([])
ax.spines[["top", "right"]].set_visible(False)
ax.set_title("The puzzle hardest for humans was easy for AI, and the reverse", loc="left", fontweight="bold")
finish(fig, "human_vs_models.png")
save_table("human_vs_models.csv", ["puzzle_date", "human_solve_rate_pct", "models_solved_of_8"], [[d, h, s] for d, h, s in rows])
print("Charts written to charts/")
