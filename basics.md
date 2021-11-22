---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.1
  kernelspec:
    display_name: pollsposition
    language: python
    name: pollsposition
---

# Basic statistics

```python
import collections
import sqlite3
import matplotlib.pyplot as plt
import numpy as np

conn = sqlite3.connect('/archive/chess/lichess.db')
```

## Player ELO ratings


Let us first look at the distribution of ELO rating for black and for white.

```python
cur = conn.cursor()
cur.row_factory = lambda cursor, row: row[0]

cur.execute("SELECT white_elo FROM lichess where white_elo is not null")
white_elos = cur.fetchall()

cur.execute("SELECT black_elo FROM lichess where black_elo is not null")
black_elos = cur.fetchall()

cur.execute("SELECT white_elo-black_elo FROM lichess where white_elo is not null and black_elo is not null")
elo_diff = cur.fetchall()
```

```python
plt.hist(white_elos, alpha=.3)
plt.hist(black_elos, alpha=.3)
```

```python
plt.hist(elo_diff)
```

```python
np.mean(elo_diff)
```

```python
np.std(elo_diff)
```

## Game outcome

See a [Chess stackexchange](https://chess.stackexchange.com/questions/2017/does-white-have-an-advantage) question on the topic. And [another one](https://chess.stackexchange.com/questions/2508/white-have-an-advantage-with-the-first-move?noredirect=1&lq=1)

In [this answer](https://chess.stackexchange.com/questions/1494/does-the-first-move-advantage-for-white-have-real-meaning-apart-from-the-highest?rq=1) the author went as far as doing the computations (look at method for keeping games/ELO).

"You will win with either color if you are the better player, but it takes longer with Black." — Isaac Kashdan (Chess Life, Sept 1969)
"The first-move advantage is founded more in psychology than in reality." - Andras Adorjan
--> Black is OK!


PLaying Black is equivalent to a 25-40 ELO rating point disadvantage:
"An easier handicap between two roughly equal opponents would be to give the weaker player white. This is roughly equal to 25-40 rating points"

Ok so this is really interesting. We can take all of A and B's games and [fit a
model](http://www.chessmetrics.com/KaggleComp/1-TimSalimans.pdf) that includes
the black-white advantage:

$$
d = s_A - s_B + \gamma + \epsilon, \epsilon \sim
\operatorname{Normal}(0,\sigma^2)
$$

if $d>1$, A wins, $d<-1$ B wins otherwise we have a draw. $S_i \sim
\operatorname{Normal}(\mu_i, 1)$ and the $\mu_i$ share the same hyperprior. We
can use a a random walk to compute a rating that evolves with time.

A lot of interesting stuff in Glickman's paper on rating systems. Apparently
this difference had been known for a while.


Look at number of #ply before white, black win or draw.

Relate this to tournamenent rules.

Look at AlphaZero against Stockfish!

Can we look at AlphaZero playing against itself?

That there is a higher chance of winning with white /does not/ mean that there
is first mover advantage, i.e. that the win can solely be explained by being the
first to move.

Maybe we can look at this differently and look at exactly mirrored board
positions. If we take every possible board there are more that would be
mate-in-one for the first move.

An explanation is that White is likeluy pushing the game down a line of play for
which it has spent more time preparing. If that's the case the ratio should
decrease as the ELO increases.

There is a clear and measurable first-mover advantage for white. But one can
wonder if it is structured into the game or merely psychological. To (partially)
answer this question we consider games from more and more experienced players,
by increasing ELO score.

Further, does this ratio apply to every player or are there players that are
insanely better with blacks that with whites?

When I am White I win because I am White. When I am Black I win because I am Bogoljubov. — Efim Bogoljubov

- Checkers has been shown to be a draw
- Greater than the house advantage in casinos




We can look at the game outcome and condition on the ELO rating, difference of ELO etc.

There is a lot of discussion around whether black has an advantage and we shall answer this with statistics. Look at this [wikipedia article](https://en.wikipedia.org/wiki/First-move_advantage_in_chess) for pointers.

```python
cur.execute("SELECT result FROM lichess where white_elo > 500 and black_elo > 500")
results = cur.fetchall()
```

```python
counter = collections.Counter(results)
ratios = [counter['1-0'] /  sum(counter.values()), counter['0-1'] /  sum(counter.values()), counter['1/2-1/2'] /  sum(counter.values())]
```

```python
ratios
```

We now plot the results as a function of ELO ceiling for both players.


And now plot what happens for black when difference of ELO increases.

```python
conn.close()
```

```python

```

## Game duration


