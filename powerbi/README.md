# Power BI Setup

1. Open Power BI Desktop → **Get Data** → **SQLite** (install the SQLite ODBC driver
   from https://www.ch-werner.de/sqliteodbc/ on Windows).
2. Point to `data/kenya_employment.db`.
3. Load the four tables: `employment_fact`, `industry_dim`, `date_dim`, `macro_context`.
4. Open **Model view** and create the relationships per `data_model.md`.
5. Paste the contents of `dax_measures.dax` as new measures.
6. Build visuals per `data_model.md`.