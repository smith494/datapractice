# Data Analytics Practice Assignments — 9 Projects (One per Category)

Source: [DataCamp — 30 Data Analytics Projects for All Levels (2026)](https://www.datacamp.com/blog/data-analytics-projects-all-levels)

This document defines **one practice project per category** from the DataCamp list. Your goal is not just to get code running, but to *understand* what you're doing at every step. Each project includes:

- **The business question** — why this analysis matters
- **Dataset + download links** (no-login mirrors included)
- **Requirements** — what you must produce
- **Starter code** — a scaffold, not the full solution
- **Gotchas** — common traps, so you don't get stuck
- **Resources** — where to look when you *are* stuck

---

## The 9 Projects

| # | Category | Project | Skills |
|---|----------|---------|--------|
| 1 | Data Importing & Cleaning | **Exploring the NYC Airbnb Market** | CSV/TSV/Excel import, string cleaning, dates, merging |
| 2 | Data Manipulation | **Visualizing the History of Nobel Prize Winners** | Grouping, decades, derived columns, seaborn trends |
| 3 | Data Visualization | **Exploring Stock Market Trends with Plotly** | Interactive lines, dropdowns, range sliders |
| 4 | Probability & Statistics | **Modeling Car Insurance Claim Outcomes** | Missing values, logistic regression, model evaluation |
| 5 | Exploratory Data Analysis | **Investigating Netflix Movies** | EDA, scatter plots, genre insights |
| 6 | Predictive Analytics | **Predicting Credit Card Approvals** | Imputation, encoding, scaling, GridSearchCV |
| 7 | Final-Year (Deep-Dive) | **World Population Analysis** | Distributions, correlations, storytelling |
| 8 | AI-Powered (NLP) | **Sentiment Analysis on Customer Reviews** | Text preprocessing, TF-IDF, classification |
| 9 | End-to-End | **Time Series Analysis & Forecasting** | Resampling, decomposition, ARIMA/SARIMAX |

---

## Environment Setup

This project runs in the repo's Python virtualenv (Python 3.14, venv at `.venv`).

```sh
source .venv/bin/activate

# Existing deps: faker, pandas, jupyter, matplotlib
# Install per project as you reach it:
pip install openpyxl scikit-learn matplotlib seaborn statsmodels nltk plotly
```

> Tip: install packages only when a project needs them, and pin exact versions in `requirements.txt` as you go.

---

# Project 1 — Exploring the NYC Airbnb Market (Data Importing & Cleaning)

**Category:** Data Importing and Cleaning · **Source project:** DataCamp #1 (1354)
**Difficulty:** Beginner · **Est. time:** 1–2 hours

## Business Question
The travel agency "Airbnb NYC" wants to understand the short-term rental market in New York. Combine three messy files into one clean dataset and answer: *What is the average rental price? Is it above the private 1-bedroom market rate ($3,100/month)? What are the busiest review periods and how many private rooms are available?*

## Learning Objectives
- Import data from **CSV, TSV, and Excel** files into pandas
- Clean messy string columns (currency suffix, inconsistent casing)
- Parse formatted date strings into `datetime`
- Merge DataFrames on a shared key and handle missing values
- Extract new columns with `.str` accessors and summarize with `groupby`

## Datasets
Three files, all keyed by `listing_id`. Download to `data/` (no-login mirrors of the exact DataCamp files):

```
https://raw.githubusercontent.com/katiehuangx/DataCamp-Projects/main/Exploring%20the%20NYC%20Airbnb%20Market/datasets/airbnb_price.csv
https://raw.githubusercontent.com/katiehuangx/DataCamp-Projects/main/Exploring%20the%20NYC%20Airbnb%20Market/datasets/airbnb_room_type.xlsx
https://raw.githubusercontent.com/katiehuangx/DataCamp-Projects/main/Exploring%20the%20NYC%20Airbnb%20Market/datasets/airbnb_last_review.tsv
```

| File | Format | Key columns |
|---|---|---|
| `airbnb_price.csv` | CSV | `listing_id`, `price` (e.g. `"225 dollars"`), `nbhood_full` (e.g. `"Manhattan, Midtown"`) |
| `airbnb_room_type.xlsx` | Excel | `listing_id`, `description`, `room_type` |
| `airbnb_last_review.tsv` | TSV | `listing_id`, `host_name`, `last_review` (e.g. `"May 21 2019"`) |

> Alternative full dataset (same underlying 2019 data): [Kaggle — NYC Airbnb Open Data](https://www.kaggle.com/datasets/dgomonov/new-york-city-airbnb-open-data).

## Requirements (Deliverables)
1. Load all three files into DataFrames (`prices`, `room_types`, `reviews`) and print their heads.
2. Clean `price` so it becomes numeric (strip the `" dollars"` suffix, cast to float).
3. Drop listings priced at `0` (free) and compute the **average price** (expected ≈ **$141.82**). Compare to the $3,100/month benchmark using `price * 365 / 12`.
4. Clean `room_type` (lowercase) and count **private rooms** (expected ≈ **11,356**).
5. Convert `last_review` to `datetime`; find first and last dates (expected **2019-01-01** and **2019-07-09**).
6. Merge all frames on `listing_id` (outer), `dropna()`, check for duplicate `listing_id`s.
7. Extract **borough** from `nbhood_full` (text before the comma) and compute average price per borough; explain the ranking.
8. (Bonus) Bucket prices with `pd.cut` (`Budget <70`, `Average 70–175`, `Expensive 176–350`, `Extravagant >350`) and count by borough.

## Starter Code
```python
import pandas as pd

prices = pd.read_csv("data/airbnb_price.csv")
room_types = pd.read_excel("data/airbnb_room_type.xlsx")
reviews = pd.read_csv("data/airbnb_last_review.tsv", sep="\t")

print(prices.head(), room_types.head(), reviews.head(), sep="\n")

# Clean price: "225 dollars" -> 225.0
prices["price"] = prices["price"].str.replace(" dollars", "").astype(float)

# Normalize room_type casing
room_types["room_type"] = room_types["room_type"].str.lower()

# Parse dates
reviews["last_review"] = pd.to_datetime(reviews["last_review"])

# Merge + clean
df = prices.merge(room_types, on="listing_id", how="outer") \
           .merge(reviews,  on="listing_id", how="outer")
df = df.dropna()
# ... continue: avg price, monthly price, room_type counts, date range,
#     borough via .str.partition(",", expand=True)[0], groupby, pd.cut
```

## Gotchas
- The **TSV** needs `sep="\t"`.
- Strip `" dollars"` **before** converting to numeric.
- Exclude `price == 0` before averaging, or you'll get 141.78 instead of 141.82.
- `host_name` (8 nulls) + `description` (10 nulls) → `dropna()` removes exactly 25 rows (25,209 → 25,184).
- Month-name dates parse fine with `pd.to_datetime` — no format string needed.

## Resources (check these if stuck)
- [DataCamp — Introduction to Importing Data in Python](https://www.datacamp.com/courses/introduction-to-importing-data-in-python)
- [DataCamp — Cleaning Data in Python](https://www.datacamp.com/courses/cleaning-data-in-python)
- pandas docs: [`pd.to_datetime`](https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html) · [Merge/Join](https://pandas.pydata.org/docs/user_guide/merging.html) · [Text methods `.str`](https://pandas.pydata.org/docs/user_guide/text.html)
- Reference solution: [github.com/katiehuangx/DataCamp-Projects — NYC Airbnb](https://github.com/katiehuangx/DataCamp-Projects/tree/main/Exploring%20the%20NYC%20Airbnb%20Market)

---

# Project 2 — Visualizing the History of Nobel Prize Winners (Data Manipulation)

**Category:** Data Manipulation · **Source project:** DataCamp #6 (1888)
**Difficulty:** Beginner–Intermediate · **Est. time:** 1–2 hours

## Business Question
The Nobel Foundation wants to understand a century of prizes: *Which country dominates? When did the USA's dominance begin? How has the gender balance shifted per category? Are laureates getting older?* You'll manipulate the data with pandas and tell the story with seaborn.

## Learning Objectives
- Group and aggregate with `groupby`; bin years into **decades**
- Create boolean flags and compute proportions with `.mean()` on booleans
- Derive new columns (e.g., laureate age) from dates
- Visualize trends with seaborn `lineplot`, `lmplot` (lowess), and `catplot`

## Dataset
One CSV, **911 rows × 18 columns** (laureates, 1901–2016). Download to `data/`:

```
https://raw.githubusercontent.com/ozlerhakan/datacamp-projects/master/A%20Visual%20History%20of%20Nobel%20Prize%20Winners/datasets/nobel.csv
```
Alternates: [nafisalawalidris mirror](https://raw.githubusercontent.com/nafisalawalidris/Analyzing-Nobel-Prize-Dataset-Demographics-and-Trends/main/nobel.csv) · [official Nobel API CSV](https://api.nobelprize.org/v1/laureate.csv)

Columns: `year, category, prize, motivation, prize_share, laureate_id, laureate_type, full_name, birth_date, birth_city, birth_country, sex, organization_name, organization_city, organization_country, death_date, death_city, death_country`

## Requirements (Deliverables)
1. Load, `head(6)`, count prizes, `sex.value_counts()`, and top-10 `birth_country`.
2. Create `usa_born_winner = birth_country == "United States of America"`; add a `decade = np.floor(year/10)*10` column.
3. Plot **proportion of USA-born winners per decade** with `sns.lineplot` (use a 0–1 percent format). Which decade does US dominance begin? (≈ the 1930s.)
4. Create `female_winner`; plot **female share by decade and category** (`groupby(["decade","category"]).mean()` + `hue="category"`). Which categories lag furthest behind?
5. Find the **first female winner** (`nsmallest(1, "year")`) → Marie Curie (1903, Physics).
6. Find **repeat laureates** (`groupby("full_name").filter(lambda g: len(g) >= 2)`).
7. Compute **age at award**: parse `birth_date` → `age = year - birth_date.dt.year`; plot with `sns.lmplot(x="year", y="age", lowess=True)`.
8. (Bonus) Same age trend faceted per category (`row="category"`) plus oldest (Leonid Hurwicz, 90) and youngest (Malala Yousafzai, 17) laureates.

## Starter Code
```python
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib.ticker import PercentFormatter

nobel = pd.read_csv("data/nobel.csv")
print(nobel.head(6), nobel.sex.value_counts(), nobel["birth_country"].value_counts().head(10), sep="\n")

nobel["usa_born_winner"] = nobel["birth_country"] == "United States of America"
nobel["decade"] = np.floor(nobel["year"] / 10) * 10
usa_per_decade = nobel.groupby("decade")["usa_born_winner"].mean()

# 3) line plot of usa_per_decade
ax = sns.lineplot(x=usa_per_decade.index, y=usa_per_decade.values)
ax.yaxis.set_major_formatter(PercentFormatter(1.0))

# 4) female share
nobel["female_winner"] = nobel["sex"] == "Female"
female_share = nobel.groupby(["decade", "category"])["female_winner"].mean()
sns.lineplot(data=female_share.reset_index(), x="decade", y="female_winner", hue="category")

# 7) age
nobel["birth_date"] = pd.to_datetime(nobel["birth_date"], errors="coerce")
nobel["age"] = nobel["year"] - nobel["birth_date"].dt.year
sns.lmplot(data=nobel, x="year", y="age", lowess=True)
```

## Gotchas
- Use **`birth_country`** for country — `organization_country` is NaN for shared prizes.
- Country names must be matched exactly (`"United States of America"`, quirks like `"Prussia (Germany)"`).
- Parse `birth_date` with `errors="coerce"`; derived `age` will contain NaNs (organizations / missing dates).
- `sex.value_counts()` only shows Male/Female — organizations are NaN.

## Resources (check these if stuck)
- [DataCamp — Intermediate Data Visualization with Seaborn](https://www.datacamp.com/courses/intermediate-data-visualization-with-seaborn)
- [DataCamp — Data Manipulation with pandas](https://www.datacamp.com/courses/data-manipulation-with-pandas)
- seaborn docs: [`lmplot`](https://seaborn.pydata.org/generated/seaborn.lmplot.html) · [`lineplot`](https://seaborn.pydata.org/generated/seaborn.lineplot.html) · [tutorial](https://seaborn.pydata.org/tutorial.html)

---

# Project 3 — Exploring Stock Market Trends with Plotly (Data Visualization)

**Category:** Data Visualization · **Source project:** DataCamp #7 (2905)
**Difficulty:** Intermediate · **Est. time:** 1–2 hours

## Business Question
A fund analyst wants an interactive dashboard to explore the relative momentum of ten fast-food restaurant stocks (McDonald's, Starbucks, Domino's, Yum, Wendy's, Papa John's, etc.). Build interactive charts with dropdown menus and a range slider so she can compare tickers and price columns without writing a query each time.

## Learning Objectives
- Build interactive line charts and candlesticks with Plotly
- Add hover, zoom, dropdowns, and range sliders
- Use `adj_close` vs `close` correctly; handle large price-range differences between tickers
- (Extension) subtract moving averages, annotate key events

## Dataset
One CSV, **11,857 rows × 8 columns**, daily OHLCV for **10 tickers**, 2019–2023. Download to `data/`:

```
https://raw.githubusercontent.com/daniel207pzd/Exploring-Stock-Market-Trends-with-Plotly/main/companies.csv
```
Alternate mirrors: [swarajbobade2414](https://raw.githubusercontent.com/swarajbobade2414/Exploring-Stock-Market-Trends-with-Plotly/main/companies.csv) · [XuanS3647](https://raw.githubusercontent.com/XuanS3647/Exploring-Stock-Market-Trends-with-Plotly-python/main/companies.csv)

Columns (lowercase): `date, open, high, low, close, adj_close, volume, company_ticker`
Tickers: `BRK-A` (Berkshire), `DNUT`, `DPZ`, `LKNCY`, `MCD`, `PZZA`, `QSR`, `SBUX`, `WEN`, `YUM`

## Requirements (Deliverables)
1. Load `companies.csv`, parse `date` as datetime; run `info()`/`describe()`.
2. Build one `go.Scatter` trace per company (using `close`).
3. Add a **company dropdown** that toggles trace visibility.
4. Add a **column dropdown** (`close`, `high`, `low`, `volume`, …) that updates all traces' y-data.
5. Add **range-selector buttons** (YTD, 1Y, 5Y) plus a `rangeslider`; assemble with `update_layout`.
6. (Extension) Add a candlestick chart for one ticker (`go.Candlestick`), a 50-day moving average, and annotate an event (e.g., an IPO or earnings spike).

## Starter Code
```python
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("data/companies.csv")
df["date"] = pd.to_datetime(df["date"])
tickers = sorted(df["company_ticker"].unique())

fig = go.Figure()
for t in tickers:
    sub = df[df["company_ticker"] == t].sort_values("date")
    fig.add_trace(go.Scatter(x=sub["date"], y=sub["close"],  # switch to adj_close to compare
                             name=t, visible=(t == "MCD")))

# Company dropdown (update 'visible'), column dropdown (update 'y'),
# range selector ('rangeselector' + 'rangeslider'):
fig.update_layout(
    updatemenus=[
        dict(buttons=[dict(label=t, method="update",
                           args=[{"visible": [n == t for n in tickers]}]) for t in tickers],
             direction="down"),
    ],
    xaxis=dict(rangeselector=dict(buttons=[], buttons=[dict(count=1, step="year", label="1Y"),
                                                      dict(step="all", label="All")]),
               rangeslider=dict(visible=True)),
    title="Fast-Food Stocks — Interactive Explorer",
)
fig.show()
```

## Gotchas
- Column names are **lowercase**, and `adj_close` differs from `close` (splits/dividends) — use `adj_close` for fair cross-ticker comparisons.
- `DNUT` (IPO 2021) and `LKNCY` have **fewer rows** than the other 8 tickers.
- Price scales differ massively (BRK-A ≈ $300k vs PZZA ≈ $40) — use a **log y-axis** for cross-ticker charts.
- `graph_objects` needs Plotly ≥ 5; it renders in Jupyter with `fig.show()`.

## Resources (check these if stuck)
- [DataCamp — Introduction to Data Visualization with Plotly in Python](https://www.datacamp.com/courses/introduction-to-data-visualization-with-plotly-in-python)
- Plotly docs: [line charts](https://plotly.com/python/line-charts/) · [candlestick](https://plotly.com/python/candlestick-charts/) · [dropdowns](https://plotly.com/python/dropdowns/) · [range slider](https://plotly.com/python/range-slider/)
- Fallback data: `pip install yfinance` → `yf.download("MCD SBUX DPZ YUM QSR WEN PZZA LKNCY DNUT BRK-A", start="2019-01-01", end="2023-12-31")`

---

# Project 4 — Modeling Car Insurance Claim Outcomes (Probability & Statistics)

**Category:** Probability & Statistics · **Source project:** DataCamp #10 (1645)
**Difficulty:** Intermediate · **Est. time:** 1–2 hours

## Business Question
"On the Road" car insurance has very limited ML infrastructure. They want a **single-feature** model that predicts whether a customer will file a claim. Which one feature (age, credit score, driving experience, …) predicts claim outcomes *best*? Answer with statistics (logistic regression) and rank each feature by accuracy.

## Learning Objectives
- Handle missing values and understand target class balance (~70/30)
- Fit a logistic regression to predict a binary outcome
- Compute accuracy per single-feature model and rank features
- (Bonus) Evaluate honestly with precision/recall/F1 and an 80/20 split

## Dataset
One CSV, **10,000 rows × 19 columns** (no-login mirror):

```
https://raw.githubusercontent.com/nicolasfoss/ml_insurance/Primary/car_insurance.csv
```

Columns: `id, age, gender, race, driving_experience, education, income, credit_score, vehicle_ownership, vehicle_year, married, children, postal_code, annual_mileage, vehicle_type, speeding_violations, duis, past_accidents, outcome`

- `outcome` = target: `0` no claim, `1` claim (~30%)
- `credit_score` (~9.8%) and `annual_mileage` (~9.6%) have **missing values**
- Categoricals are numeric-encoded (e.g., `driving_experience` 0–3)

> Human-readable label variant (same data): [github.com/AchrafSL/Modeling-Car-Insurance-Claim-Outcomes-DataCamp](https://github.com/AchrafSL/Modeling-Car-Insurance-Claim-Outcomes-DataCamp).

## Requirements (Deliverables)
1. Load; report shape, dtypes, and missing-value counts per column.
2. Drop `id`. Impute `credit_score` and `annual_mileage` (median), confirm no NaNs.
3. For **each** feature, fit `LogisticRegression` on the single column, predict, and compute **accuracy**.
4. Build `feature → accuracy` table, pick the best, and return `best_feature_df` (`best_feature`, `best_accuracy`). Expected: **`driving_experience` ≈ 0.777**.
5. (Bonus) Add precision/recall/F1 + ROC-AUC, and/or re-run with an 80/20 split for an honest score (a "always predict no-claim" baseline scores ~70%).

## Starter Code
```python
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

df = pd.read_csv("data/car_insurance.csv")
print(df.info())                                     # spot missing values
df = df.drop(columns=["id"])
df["credit_score"]   = pd.to_numeric(df["credit_score"], errors="coerce")
df["annual_mileage"] = pd.to_numeric(df["annual_mileage"], errors="coerce")
df = df.fillna(df.median(numeric_only=True))

y = df["outcome"]
results = []
for col in [c for c in df.columns if c != "outcome"]:
    model = LogisticRegression()
    model.fit(df[[col]], y)
    pred = model.predict(df[[col]])
    results.append({"feature": col, "accuracy": accuracy_score(y, pred)})

best = max(results, key=lambda r: r["accuracy"])
print(pd.DataFrame(results).sort_values("accuracy", ascending=False))
best_feature_df = pd.DataFrame({"best_feature": [best["feature"]],
                                "best_accuracy": [best["accuracy"]]})
```

## Gotchas
- Missing cells can load as empty strings → `pd.to_numeric(..., errors="coerce")` first.
- Median beats mean for imputation here (outliers exist).
- No scaling needed since each model uses one raw feature.
- At ~70/30 imbalance, accuracy is inflated — always compare against the 70% "always majority" baseline.

## Resources (check these if stuck)
- [DataCamp — Supervised Learning with scikit-learn](https://www.datacamp.com/courses/machine-learning-with-scikit-learn)
- [scikit-learn — LogisticRegression docs](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html) · [model evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html)
- [statsmodels — Logit](https://www.statsmodels.org/stable/generated/statsmodels.discrete.discrete_model.Logit.html) (p-values / confidence intervals)
- Reference solutions: [thisyourgokul](https://github.com/thisyourgokul/Modeling-Car-Insurance-Claim-Outcomes)

---

# Project 5 — Investigating Netflix Movies (Exploratory Data Analysis)

**Category:** Exploratory Data Analysis · **Source project:** DataCamp #14 (1237)
**Difficulty:** Beginner · **Est. time:** 1–2 hours

## Business Question
A friend claims Netflix **movies are getting shorter**. Verify this with the real catalog data, dig into the outliers, and explain what's really happening — then write a color-coded scatter that visualizes the trend by genre.

## Learning Objectives
- Read data, filter rows, subset columns (`loc`)
- Scatter plots for relationships (`release_year` vs `duration`)
- Explore short-movie outliers by examining genres
- Use `for` loops / conditionals to assign colors from a mapping
- Draw an evidence-based conclusion from plots

## Dataset
One CSV, **7,787 rows × 11 columns** (DataCamp version). Download to `data/`:

```
https://raw.githubusercontent.com/edwinrlambert/Investigating-Netflix-Movies/main/data/netflix_data.csv
```
Alternate mirror (verify `head()` first — 7,787 rows expected): [idanglomato](https://raw.githubusercontent.com/idanglomato/DC-Investigating-Netflix-Movies-and-Guest-Stars-in-The-Office/main/datasets/netflix_data.csv)

Columns: `show_id, type, title, director, cast, country, date_added, release_year, duration, description, genre`
> The Office guest-stars half of this project is optional — data at [Kaggle — The Office Dataset](https://www.kaggle.com/datasets/nehaprabhavalkar/the-office-dataset).

## Requirements (Deliverables)
1. Load `netflix_data.csv`; filter `type == "Movie"`.
2. Subset to `title, country, genre, release_year, duration`.
3. Scatter `release_year` vs `duration` (matplotlib). What does the bare plot suggest?
4. Look at movies shorter than 60 minutes — what genres dominate? (Children, Documentaries, Stand-Up.)
5. Assign each movie a color by genre bucket (`Children` / `Documentaries` / `Stand-Up` / `Other`) using a loop + `if/elif`; plot the colored scatter.
6. Write your conclusion: are movies actually getting shorter? (**Answer: no** — non-feature films skew the average; feature-length movies are roughly stable.)*Hint: the average of 2011–2020 durations `[103,101,99,100,100,95,95,96,93,90]` is the "red herring" the project tests.*
7. (Optional bonus) For The Office data, scatter `episode_number` vs `viewership_mil`, color by `scaled_ratings` buckets, highlight guest-star episodes with larger markers.

## Starter Code
```python
import pandas as pd
import matplotlib.pyplot as plt

movies = pd.read_csv("data/netflix_data.csv")
movies = movies.loc[movies["type"] == "Movie", ["title", "country", "genre", "release_year", "duration"]]

fig, ax = plt.subplots(figsize=(12, 6))
ax.scatter(movies["release_year"], movies["duration"])
ax.set_title("Netflix Movie Duration vs Year of Release")
ax.set_xlabel("Release year"); ax.set_ylabel("Duration (min)")

# Color by genre bucket:
colors = []
for _, row in movies.iterrows():
    if row["genre"] == "Children":      colors.append("red")
    elif row["genre"] == "Documentaries": colors.append("blue")
    elif row["genre"] == "Stand-Up":    colors.append("green")
    else:                               colors.append("grey")
# replot scatter with c=colors ...
```

## Gotchas
- **Always filter `type == "Movie"` first** — TV-show `duration` values are strings like `"3 Seasons"`, which break numeric plots.
- `genre` is single-valued in the DataCamp file (unlike Kaggle's multi-value `listed_in`).
- Several `netflix_data.csv` copies circulate on GitHub (1.7 vs 2.7 MB) — confirm 7,787 rows before analyzing.

## Resources (check these if stuck)
- [DataCamp — Exploratory Data Analysis in Python](https://www.datacamp.com/courses/exploratory-data-analysis-in-python)
- matplotlib docs: [`pyplot.scatter`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.scatter.html)
- Reference solutions: [slimanesedrati/Investigating-Netflix-Movies](https://github.com/slimanesedrati/Investigating-Netflix-Movies)

---

# Project 6 — Predicting Credit Card Approvals (Predictive Analytics)

**Category:** Predictive Analytics · **Source project:** DataCamp #17 (558)
**Difficulty:** Intermediate · **Est. time:** 2–3 hours

## Business Question
A bank wants to automate credit-card application screening. Build the best-performing machine-learning model to predict approval from applicant attributes — then tune it with grid search.

## Learning Objectives
- Load header-less data; recognize `?` as missing values
- Split train/test **before** preprocessing (avoid data leakage)
- Impute numeric (mean) and categorical (most-frequent) missing values
- Encode categoricals with `get_dummies`, scale numeric features with `MinMaxScaler`
- Train logistic regression; evaluate with accuracy + confusion matrix
- Tune with `GridSearchCV`

## Dataset
One file, **690 rows × 16 columns** (UCI Credit Approval, no header, `?` = missing):
```
https://archive.ics.uci.edu/static/public/27/credit+approval.zip
```
Direct no-login mirror of `crx.data`: `https://raw.githubusercontent.com/JLZml/Credit-Scoring-Data-Sets/master/1.%20UCI%20Repository/Japan/crx.data`

Features `A1–A15` (9 categorical, 6 continuous); target `A16` = `+` approved / `-` denied (≈ 44.5% / 55.5%). DataCamp loads as `cc_apps = pd.read_csv("datasets/cc_approvals.data", header=None)`.

## Requirements (Deliverables)
1. Load with `header=None`; inspect with `describe()`, `info()`, `tail()`.
2. **Split into train/test first** (80/20). Drop features 11 & 13 (0-indexed; DriversLicense, ZipCode).
3. Replace `?` with `np.nan`.
4. Impute numeric columns with the **train mean**; categorical with the train **most-frequent** value (apply train values to test).
5. `pd.get_dummies()` the categoricals (reindex test to train's columns).
6. Scale all features 0–1 with `MinMaxScaler` (fit on train, transform test).
7. Fit `LogisticRegression()`; report test **accuracy + confusion matrix**.
8. Tune with `GridSearchCV(cv=5)` over `tol=[0.01, 0.001, 0.0001]` and `max_iter=[100,150,200]`; report `best_params_` and score the best model on the test set.

## Starter Code
```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression

cc = pd.read_csv("data/cc_approvals.data", header=None)
cc = cc.replace("?", np.nan).drop(columns=[11, 13])       # ? = missing; drop cols 11 & 13

X_train, X_test, y_train, y_test = train_test_split(
    cc.iloc[:, :-1], (cc.iloc[:, -1] == "+").astype(int),
    test_size=0.2, random_state=42)

num_cols  = X_train.select_dtypes(include=np.number).columns    # may be empty until coerced
cat_cols  = X_train.select_dtypes(include="object").columns
# 1) Coerce numeric cols with pd.to_numeric(errors="coerce"), then mean-impute.
# 2) Most-frequent impute categorical cols.
# 3) get_dummies on cat cols (X_test = X_test.reindex(columns=X_train.columns, fill_value=0)).
# 4) MinMaxScaler (fit on train).
# 5) LogisticRegression → accuracy, confusion_matrix.
# 6) GridSearchCV(cv=5, param_grid={"tol":[0.01,0.001,0.0001], "max_iter":[100,150,200]}).
```

## Gotchas
- `?` = missing and **breaks dtype inference** — `A2`, `A3`, `A8`, `A11`, `A14`, `A15` must be coerced numeric after replacing `?`.
- **Split before** imputing/scaling to avoid leakage; fit imputers/scalers on train only.
- Test may contain unseen category levels — after `get_dummies`, `reindex(X_train.columns, fill_value=0)`.
- Scale before penalized LR — raw ranges span 0–28 to 100,000.
- Moderate imbalance (44.5/55.5) — read the confusion matrix, not just accuracy. (Gains from `tol`/`max_iter` tuning are small; try `C`/`solver` for real improvement.)

## Resources (check these if stuck)
- [DataCamp — Supervised Learning with scikit-learn](https://www.datacamp.com/courses/machine-learning-with-scikit-learn)
- [scikit-learn — GridSearchCV](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html) · [Pipeline](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html) · [ColumnTransformer](https://scikit-learn.org/stable/modules/generated/sklearn.compose.ColumnTransformer.html)
- Reference notebook: [rubayat-tithi/predicting-credit-card-approvals](https://github.com/rubayat-tithi/predicting-credit-card-approvals-datacamp-project/blob/main/notebook.ipynb)

---

# Project 7 — World Population Analysis (Final-Year Deep-Dive)

**Category:** Final-Year (Exploratory Deep-Dive) · **Source project:** #23 (Kaggle)
**Difficulty:** Intermediate · **Est. time:** 2–3 hours

## Business Question
You are a UN analyst building a briefing on global population trends. Explore 50+ years of country-level data and produce charts that tell the story of *which regions are growing, which are densest, and how population and area relate*. Deliverable: a set of clear, interpretable visualizations.

## Learning Objectives
- Structured EDA (shape, dtypes, summary stats, nulls)
- Comparing most/least populated countries and continents
- Distributions/density (histograms, KDE, scatter)
- Encoding categoricals and reading a correlation heatmap

## Dataset
One CSV, **234 rows × 17 columns** (233 countries). Download (no login):
```
https://www.kaggle.com/api/v1/datasets/download/iamsouravbanerjee/world-population-dataset   # zip → world_population.csv
```
No-login mirror:
```
https://raw.githubusercontent.com/Di-ivyanshu/Data_analyst_project/main/world_population.csv
```

Columns: `Rank, CCA3, Country/Territory, Capital, Continent, 2022 Population, 2020 Population, 2015 Population, 2010 Population, 2000 Population, 1990 Population, 1980 Population, 1970 Population, Area (km²), Density (per km²), Growth Rate, World Population Percentage`

## Requirements (Deliverables)
1. Load and explore: `shape`, `.info()`, `.head()`, `.describe()`, null check (zero nulls expected).
2. Bar charts of the **10 most** and **10 least** populated countries (2022).
3. Continent 2022 population — bar (try a log scale) + pie chart (Asia ≈ 59% share).
4. Continent timeline — line plot per continent 1970 → 2022 (`groupby` + transpose).
5. **Density** — histogram of `Density (per km²)` (symlog x); identify densest (Macau ≈ 23,172/km²) and least dense (Greenland ≈ 0.026/km²); scatter `Area` vs `Density`.
6. **Growth rate** — highest (Moldova ≈ 1.069) and lowest (Ukraine ≈ 0.912); fastest-growing continent on average (Africa).
7. **Rank distribution** — KDE of `Rank` per continent (6 facets).
8. **Correlation map** — `LabelEncoder` categoricals, then Pearson heatmap. Note population↔world-% correlation and negative rank correlations.

## Starter Code
```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("data/world_population.csv")
print(df.shape); print(df.info()); print(df.isnull().sum())

most  = df.nlargest(10, "2022 Population")
least = df.nsmallest(10, "2022 Population")
cont  = df.groupby("Continent")["2022 Population"].sum().sort_values(ascending=False)

years = ["1970 Population", "1980 Population", "1990 Population", "2000 Population",
         "2010 Population", "2015 Population", "2020 Population", "2022 Population"]
by_year = df.groupby("Continent")[years].sum().T          # years × continents → plot()

df_enc = df.copy()
for col in ["CCA3", "Country/Territory", "Capital", "Continent"]:
    df_enc[col] = LabelEncoder().fit_transform(df_enc[col])
sns.heatmap(df_enc.corr(numeric_only=True), cmap="coolwarm")
```

## Gotchas
- Column names contain **spaces and a superscript**: `Area (km²)`, `Density (per km²)` — reference exactly or rename.
- A numeric column loading as `object` means a mirror with comma-formatted numbers → `.str.replace(",", "").astype(float)`.
- `World Population Percentage` is a small float (0.52 = 0.52%), *not* 52.
- `Growth Rate` is a **ratio/multiplier** (1.0257 ≈ +2.57%/yr; <1 = decline).
- `Rank` is **inverse** (1 = most populous) → negative correlations.

## Resources (check these if stuck)
- [DataCamp — Intermediate Data Visualization with Seaborn](https://www.datacamp.com/courses/intermediate-data-visualization-with-seaborn)
- pandas: [GroupBy](https://pandas.pydata.org/docs/user_guide/groupby.html) · [corr](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.corr.html)
- Reference notebook: [Kaggle — World Population Analysis (hasibalmuzdadid)](https://www.kaggle.com/code/hasibalmuzdadid/world-population-analysis)

---

# Project 8 — Sentiment Analysis on Customer Reviews (AI-Powered / NLP)

**Category:** AI-Powered Data Analytics · **Source project:** #25 (Kaggle)
**Difficulty:** Intermediate–Advanced · **Est. time:** 2–3 hours

## Business Question
A retailer wants to automatically classify customer reviews as positive or negative so complaints get routed without staff reading every message. Preprocess thousands of text reviews, turn them into numeric features, and train a classifier.

> Note: The original Kaggle notebook referenced by DataCamp now returns 404, so this assignment uses a **public substitute dataset** that teaches the identical pipeline (preprocessing → TF-IDF → Naive Bayes → evaluation).

## Learning Objectives
- Text preprocessing: lowercasing, removing punctuation/URLs/@mentions/emojis, tokenization, stop words
- Vectorizing with TF-IDF
- Multinomial Naive Bayes in a scikit-learn `Pipeline`
- Evaluating with accuracy, classification report, confusion matrix

## Dataset (choose one)
**Option A — IMDB movie reviews (50k, balanced, recommended):**
```
https://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz
```
**Option B — Twitter US Airline Sentiment (14,640 tweets, public mirror):**
```
https://raw.githubusercontent.com/shosseini811/Twitter-US-Airline-Sentiment-Analysis/master/Tweets.csv
```
**Option C — E-commerce product reviews (closest to the original):** [Kaggle — E-Commerce Product Reviews](https://www.kaggle.com/datasets/asadullahcreative/e-commerce-product-reviews) (free Kaggle login).

## Requirements (Deliverables)
1. Load the text data; explore the sentiment distribution (`value_counts` + countplot). Note if it's balanced.
2. Write `clean_text()`: lowercase; remove URLs/@mentions/emojis/punctuation/numbers; tokenize with NLTK; remove stop words.
3. Show **before/after** of a few sample reviews to verify cleaning.
4. Split 80/20 with `train_test_split(..., stratify=y, random_state=42)`.
5. Build `Pipeline(TfidfVectorizer → MultinomialNB)`; train and predict.
6. Report **accuracy**, **classification report**, **confusion matrix**.
7. (Bonus) `GridSearchCV` over `ngram_range` and `alpha`; plot most informative words per class.

## Starter Code
```python
import pandas as pd
import re
import nltk
nltk.download("stopwords"); nltk.download("punkt")
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

df = pd.read_csv("data/Tweets.csv")
df = df[["text", "airline_sentiment"]]
df["airline_sentiment"] = (df["airline_sentiment"] == "positive").astype(int)

STOP = set(stopwords.words("english"))
def clean_text(t):
    t = str(t).lower()
    t = re.sub(r"http\S+|www\.\S+|@\w+", " ", t)      # URLs & mentions
    t = re.sub(r"[^a-z\s]", " ", t)                   # punctuation, numbers, emojis
    tokens = [w for w in word_tokenize(t) if w not in STOP and w != "not"]
    return " ".join(tokens)

df["clean"] = df["text"].apply(clean_text)

X_train, X_test, y_train, y_test = train_test_split(
    df["clean"], df["airline_sentiment"], test_size=0.2,
    stratify=df["airline_sentiment"], random_state=42)

pipe = Pipeline([("tfidf", TfidfVectorizer()), ("clf", MultinomialNB())])
pipe.fit(X_train, y_train)
pred = pipe.predict(X_test)
print(accuracy_score(y_test, pred)); print(classification_report(y_test, pred)); print(confusion_matrix(y_test, pred))
```

## Gotchas
- **Don't drop negation words** ("not", "never") — they flip sentiment; keep them or accuracy collapses.
- Read CSV with `encoding="utf-8"`/`latin-1` — reviews contain non-ASCII characters.
- With imbalanced data, always read per-class precision/recall, not just accuracy.
- `MultinomialNB` requires **non-negative** features — fine with TF-IDF/CountVectorizer, never negative-valued transforms.

## Resources (check these if stuck)
- [DataCamp — Introduction to Natural Language Processing in Python](https://www.datacamp.com/tracks/natural-language-processing-in-python)
- [NLTK — Chapter 3: Processing Raw Text](https://www.nltk.org/book/ch03.html)
- [scikit-learn — Working With Text Data](https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html)
- Reference pipeline: [github.com/AsadullahShehbaz/Sentiment-Analysis-on-Amazon-Product-Reviews](https://github.com/AsadullahShehbaz/Sentiment-Analysis-on-Amazon-Product-Reviews)

---

# Project 9 — Time Series Analysis & Forecasting (End-to-End)

**Category:** End-to-End Data Analytics · **Source project:** #29 (Towards Data Science)
**Difficulty:** Advanced · **Est. time:** 3–4 hours

## Business Question
A retail chain wants to forecast monthly sales for its **Furniture** and **Office Supplies** categories to plan inventory and promotions. You'll reshape transactional sales into a time series, analyze trend and seasonality, fit SARIMAX, and produce a forecast — from raw data to prediction.

## Learning Objectives
- Reshaping transactional data into a time series (`groupby` + `resample`)
- Seasonal decomposition (trend / seasonality / residual)
- Grid-searching SARIMAX parameters by AIC
- Backtesting forecast accuracy with RMSE
- Comparing two segments end-to-end

## Dataset
Tableau **Sample Superstore** — **9,994 rows × 21 columns**:
```
https://www.kaggle.com/datasets/vivek468/superstore-dataset-final
```
No-login mirrors: [yrehim7/sample-superstore-dataset](https://www.kaggle.com/datasets/yrehim7/sample-superstore-dataset) · [github.com/ushakamatham/superstore](https://github.com/ushakamatham/superstore)

Key columns: `Order ID, Order Date, Ship Date, Segment, City, State, Region, Category, Sub-Category, Sales, Quantity, Discount, Profit`. Date range ≈ **2014-01-06 → 2017-12-30**.

## Requirements (Deliverables)
1. Load; convert `Order Date` to `datetime`.
2. Filter `Category == "Furniture"`; keep only Sales; sort by `Order Date`; set as index.
3. Aggregate monthly with `resample("MS").mean()`.
4. `seasonal_decompose(model="additive")`; interpret trend/seasonal/residual.
5. Grid-search SARIMAX `(p,d,q) × (p,d,q,12)` (p,d,q ∈ 0–1) selecting lowest **AIC**.
6. Diagnostics; validate by forecasting from **2017-01-01**; report **RMSE** (reference furniture ≈ **151.64**).
7. Repeat for `Office Supplies`; forecast and compare — which trends stronger? When did Office Supplies first overtake Furniture? (Reference: **2014-07-01**.)
8. (Bonus) Plot forecasts with confidence intervals; interpret seasonality (furniture peaks ~December).

## Starter Code
```python
import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX

df = pd.read_csv("data/Sample - Superstore.csv", encoding="cp1252")
df["Order Date"] = pd.to_datetime(df["Order Date"])

furn = df[df["Category"] == "Furniture"].copy()
furn = furn.sort_values("Order Date")
y = furn.set_index("Order Date")["Sales"].resample("MS").mean()

seasonal_decompose(y, model="additive").plot()

best, best_aic = None, np.inf
for p in range(2):
    for d in range(2):
        for q in range(2):
            try:
                m = SARIMAX(y, order=(p, d, q), seasonal_order=(p, d, q, 12),
                            enforce_stationarity=False,
                            enforce_invertibility=False).fit(disp=False)
                if m.aic < best_aic:
                    best, best_aic = m, m.aic
            except Exception:
                continue
print("Best AIC:", best_aic, best.order, best.seasonal_order)
# ... train on data < 2017-01-01, forecast, compute RMSE against actuals
```

## Gotchas
- `Order Date`/`Ship Date` load as objects — convert before sorting/resampling.
- Set the datetime **index** before `resample()`; use `"MS"` (month start), not deprecated `"M"`.
- SARIMAX grid search frequently fails to converge — wrap in `try/except`, set `enforce_stationarity=False, enforce_invertibility=False`.
- The original article uses `df.ix[]` (old pandas) — replace with `.loc`/`.iloc`; add `scipy`/`sklearn.metrics` for RMSE.

## Resources (check these if stuck)
- [DataCamp — ARIMA Models in Python](https://www.datacamp.com/courses/arima-models-in-python)
- [statsmodels — SARIMAX docs](https://www.statsmodels.org/stable/generated/statsmodels.tsa.statespace.sarimax.SARIMAX.html) · [seasonal_decompose](https://www.statsmodels.org/stable/generated/statsmodels.tsa.seasonal.seasonal_decompose.html)
- Reference article + notebook: [Towards Data Science — End-to-End Time Series (Susan Li)](https://towardsdatascience.com/an-end-to-end-project-on-time-series-analysis-and-forecasting-with-python-4835e6bf050b) · [github notebook](https://github.com/susanli2016/Machine-Learning-with-Python/blob/master/Time%20Series%20Forecastings.ipynb)

---

## Suggested Completion Order

Bundled to build on each other:

1. **Project 1 (NYC Airbnb)** — pandas foundation: import, clean, merge, groupby.
2. **Project 5 (Netflix)** — first EDA + scatter plots.
3. **Project 2 (Nobel Prize)** — grouping, derived columns, seaborn trends.
4. **Project 7 (World Population)** — deeper EDA, distributions, correlations.
5. **Project 3 (Plotly stocks)** — interactive visualization.
6. **Project 4 (Car Insurance)** — first modeling + evaluation.
7. **Project 6 (Credit Card Approvals)** — full preprocessing + tuning pipeline.
8. **Project 8 (Sentiment)** — text data and NLP classification.
9. **Project 9 (Time Series)** — end-to-end pipeline, forecasting.

## Portfolio Tips
- Keep one notebook per project, with Markdown cells explaining *why* at each step.
- After each project, write a 3–4 sentence summary: business question → approach → key finding.
- Push each notebook + a short README to GitHub.
- Run `Kernel → Restart & Run All` before calling a notebook "done" to guarantee reproducibility.