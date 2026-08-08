# Reflection

## What Copilot generated

I used Copilot to help write two of the four functions in `data_cleaning.py`:
`clean_column_names` and `handle_missing_values`. My workflow was to write a
short docstring above each empty function first, describing what I wanted
it to do, and then let Copilot suggest the body.

For `clean_column_names`, I wrote something like "standardize column names
to lowercase, underscore-separated names with no leading/trailing
whitespace," and Copilot suggested a one-liner:
`df.columns = df.columns.str.strip().str.lower()`. That got me most of the
way there, but it didn't account for the fact that some of the raw headers
in this dataset have extra internal spaces (like `"qty ,   date_sold"`),
which would've left me with a column literally named `qty` and another with
trailing junk instead of clean, consistent names.

For `handle_missing_values`, I described wanting to clean up the text
columns and deal with missing prices/quantities. Copilot's first suggestion
was basically `df.fillna(0)` applied across the whole DataFrame — quick,
but not something I actually wanted here.

## What I modified

I extended `clean_column_names` to also replace runs of internal whitespace
with underscores using a regex (`str.replace(r"\s+", "_", regex=True)`),
so headers like `"date_sold "` or anything with stray double spaces would
still come out clean and consistent.

The bigger change was in `handle_missing_values`. Filling every missing
value with 0 would have quietly turned a missing price into a $0.00 price
and a missing quantity into 0 units sold — both of which are functionally
identical to the invalid rows I was supposed to be removing in the next
step, just introduced by me instead of caught. Instead, I split the logic:
I strip and clean the text columns (`prodname`, `category`) separately,
and I explicitly drop rows that are missing a price or a quantity, since I
can't calculate revenue for a sale I don't have real numbers for. I also
kept that logic separate from `remove_invalid_rows`, which handles a
different problem — values that exist but are clearly wrong, like negative
prices or a $0.00 price that Copilot's version wouldn't have caught at all.

## What I learned

The biggest thing I took away is that Copilot is really good at giving you
a fast, syntactically correct starting point, but it doesn't know anything
about your specific dataset unless you show it. The `fillna(0)` suggestion
is a perfectly reasonable default in a lot of contexts, but for sales data
specifically, it would have silently corrupted the numbers I was supposed
to be cleaning — a $0.00 price and a "row we don't have a price for" are
two very different things, and Copilot treated them the same until I
changed the logic.

That made me a lot more careful about actually reading what Copilot
generates line by line instead of accepting the first suggestion, especially
for anything involving missing or invalid data, where a "helpful" default
can quietly hide a real problem instead of fixing it. It also reinforced
that data cleaning is less about writing clever code and more about making
and documenting deliberate decisions (drop vs. fill, strip vs. reformat) —
which is exactly why the comments explaining *why* each step exists ended
up mattering as much as the code itself.
