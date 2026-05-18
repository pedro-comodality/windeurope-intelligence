```python id="cfxw9q"
import pandas as pd
import os


WATCHLIST_FILE = "data/crm/watchlist.csv"


# =====================================================
# INIT WATCHLIST
# =====================================================

def init_watchlist():

    if not os.path.exists(WATCHLIST_FILE):

        df = pd.DataFrame(
            columns=[
                "company",
                "country",
                "status",
                "notes"
            ]
        )

        df.to_csv(
            WATCHLIST_FILE,
            index=False
        )


# =====================================================
# LOAD WATCHLIST
# =====================================================

def load_watchlist():

    init_watchlist()

    return pd.read_csv(
        WATCHLIST_FILE
    )


# =====================================================
# ADD TO WATCHLIST
# =====================================================

def add_to_watchlist(
    company,
    country,
    status,
    notes
):

    init_watchlist()

    df = pd.read_csv(
        WATCHLIST_FILE
    )

    new_row = pd.DataFrame([
        {
            "company": company,
            "country": country,
            "status": status,
            "notes": notes
        }
    ])

    df = pd.concat(
        [df, new_row],
        ignore_index=True
    )

    df.to_csv(
        WATCHLIST_FILE,
        index=False
    )
```
