# Meta Ads Day-by-Day Detailed Dashboard

Streamlit dashboard built from the supplied **Meta Ads Team Dashboard** code. It keeps the existing Agent Code mapping, business-unit logic, audience/balance views, and optional WhatsApp refresh report, while adding a day-by-day ad-level reporting layer and Excel export.

## What changed

The date selector on the left is now:

- Today
- Yesterday
- Last 7 Days
- This Month
- Last Month
- Custom

The Meta Insights query runs at `level=ad` with `time_increment=1`, so a range such as **This Month** returns one row per **day × ad** rather than one aggregate row for the whole month.

The detailed table/export includes:

- Created Date (the Meta reporting day / `date_start`)
- Agent Code / Agent
- Ad Account
- Campaign
- Ad Set
- Ad
- Spend
- Results
- CPL
- Impressions
- CPM
- Link Clicks
- CPC (Spend / Link Clicks)
- CTR (Link Clicks / Impressions)
- Reach
- Frequency
- WhatsApp/Messaging conversations started
- WhatsApp Number
- Optimization Goal / Performance Goal
- ABO / CBO
- Primary Text
- Head line
- Campaign ID
- Adset ID
- AD ID
- AD Link

## Excel structure

The download button generates one workbook for the **currently selected Business Unit** and the **currently loaded snapshot range**.

Workbook order:

1. One sheet for every Agent, containing day-by-day ad-level rows with Campaign + Ad Set + Ad dimensions.
2. `Overall Campaigns`
3. `Overall Ad Sets`
4. `Overall Ads`

The three Overall sheets stay at the end as requested.

> Note: The base API pull is ad-level. Spend, results, impressions, link clicks and related calculated rates aggregate naturally. Reach is non-additive across ads, so Campaign/Ad Set Reach in the Excel summary is the sum of the ad-level daily reach rows and can be higher than a native Meta campaign-level Reach query when audiences overlap.

## Agent Code mapping

The mapping remains inside `app.py` in `MEDIA_BUYER_MAP`:

- AA → Abdallah Adel
- HM → Ahmed Hesham
- BM → Bassem Shalawy
- EK → Esraa Kamal
- MA → Mahmoud
- AF → Amr Fathy
- SQ → (R)Ahmed Sharkawy
- OS → (R)Osama Serwe
- MM → (R)Mohamed Mahmoud
- NB → (R)Mohamed Nabih

Accounts that do not match a known code appear as `Unknown` and are still exportable.

## Meta data sources

- Insights: Ad level, daily (`time_increment=1`)
- Campaign metadata: status, daily/lifetime budget, bid strategy
- Ad Set metadata: optimization goal, destination type, promoted object / WhatsApp number, ad-set budget
- Ad metadata / Creative: primary text, headline, story/permalink data

`ABO / CBO` rule used by the report:

- Campaign has a daily or lifetime budget > 0 → `CBO`
- Otherwise → `ABO`

## Local setup

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
copy .streamlit\secrets.example.toml .streamlit\secrets.toml
streamlit run app.py
```

macOS/Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
cp .streamlit/secrets.example.toml .streamlit/secrets.toml
streamlit run app.py
```

Fill in `.streamlit/secrets.toml` before running.

## Streamlit Community Cloud deployment

1. Create a GitHub repository.
2. Upload the contents of this folder to the repository root.
3. Do **not** upload `.streamlit/secrets.toml`.
4. In Streamlit Community Cloud, create a new app from the repository.
5. Main file path: `app.py`.
6. Open **App settings → Secrets** and paste the keys from `.streamlit/secrets.example.toml` with real values.
7. Deploy.

The project defaults to Meta Marketing API `v26.0`. You can override it with `META_API_VERSION` in Streamlit secrets.

## Meta token / permissions

The access token must be able to read the configured ad accounts and their insights/objects. In practice, this normally requires the appropriate business/ad-account access plus permissions such as `ads_read`; the exact access depends on how your Meta app/business assets are configured.

## Important refresh behavior

Changing the Time selector does **not** mutate the saved data by itself. Select the range and click **Refresh Data**. The Excel button exports the saved snapshot displayed in the dashboard.

The app stores its local snapshot files under `app_data/`. Streamlit Community Cloud local disk is not guaranteed to be permanent across restarts, so if the container restarts you may need to refresh the data again.
