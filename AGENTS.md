# AGENTS.md — DataPractice

## Environment

- Python 3.12.2 venv at `./.venv` — activate or use `.venv/bin/python` / `.venv/bin/pip` directly.
- Dependencies in `requirements.txt`: `faker`, `pandas`, `jupyter`.

## Commands

```sh
.venv/bin/pip install -r requirements.txt   # install deps
.venv/bin/jupyter notebook                  # launch notebook server
```

## Project

- Single notebook: `faker_data_generation.ipynb` — generates fake user data (name, email, job, address, company) via Faker, exports to `fake_data.csv`.
- No tests, no linters, no CI, no build system.
- No git commits yet.
