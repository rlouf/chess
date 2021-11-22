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

We can look at the game outcome and condition on the ELO rating, difference of ELO etc.

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
