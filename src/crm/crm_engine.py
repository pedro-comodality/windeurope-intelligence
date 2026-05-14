import pandas as pd
import os


CRM_FILE = "data/crm/crm_data.csv"


# =====================================================
# INIT CRM
# =====================================================

def initialize_crm():

    os.makedirs("data/crm", exist_ok=True)

    if not os.path.exists(CRM_FILE):

        df = pd.DataFrame(
            columns=[
                "company",
                "status",
                "notes"
            ]
        )

        df.to_csv(
            CRM_FILE,
            index=False
        )


# =====================================================
# LOAD CRM
# =====================================================

def load_crm():

    initialize_crm()

    return pd.read_csv(CRM_FILE)


# =====================================================
# SAVE CRM ENTRY
# =====================================================

def save_crm(company, status, notes):

    initialize_crm()

    df = pd.read_csv(CRM_FILE)

    existing = df[
        df["company"] == company
    ]

    if len(existing) > 0:

        df.loc[
            df["company"] == company,
            "status"
        ] = status

        df.loc[
            df["company"] == company,
            "notes"
        ] = notes

    else:

        new_row = pd.DataFrame([
            {
                "company": company,
                "status": status,
                "notes": notes
            }
        ])

        df = pd.concat(
            [df, new_row],
            ignore_index=True
        )

    df.to_csv(
        CRM_FILE,
        index=False
    )