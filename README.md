# DataPractice 📊

A structured repository for practicing data generation, data engineering, validation, and analysis using Python, pandas, and the Faker library.

## Repository Directory Layout

The repository is structured following best practices for modular, maintainable data engineering practice projects:

```
DataPractice/
├── data/
│   ├── raw/                  # Source baseline datasets (e.g. policies, fake profile data)
│   └── processed/            # Dynamically generated claims data & partitioned CSV files
├── notebooks/                # Jupyter Notebooks for exploratory data generation & analysis
│   ├── faker_data_generation.ipynb
│   ├── insurance_data_generation.ipynb
│   ├── data_analysis_practice_pandas.ipynb
│   └── aws_test.ipynb
├── learning/                 # Python bootcamp learning material
│   ├── Bootcamp_Notebooks/   # Bootcamp course notebooks & milestone projects
│   ├── ABSP_PDA_Notebooks/   # Automate the Boring Stuff practice notebooks
│   ├── modules_packages/     # Modules & packages practice
│   └── python_bootcamp_files/ # Bootcamp scripts & tests
├── docs/                     # Documentation, guides, and raw text notes
│   ├── assignments/          # Data analytics practice assignments
│   └── context/              # Dataset generation specifications
├── scripts/                  # Production/utility Python execution scripts
│   ├── generate_claims.py    # Generates master claims and partitions from raw policies
│   └── verify_claims.py      # Performs comprehensive validation checks on data integrity
├── .venv/                    # Python virtual environment (git ignored)
├── requirements.txt          # Python library dependencies
└── LICENSE                   # MIT License details
```

---

## Getting Started

### 1. Prerequisites
Ensure you have Python 3.14.x installed.

### 2. Setup Virtual Environment
Create and activate a virtual environment, then install the package dependencies:

```bash
# Create the virtual environment
python -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate   # or use .venv/bin/python directly
# On Windows:
.venv\Scripts\activate

# Install dependencies
.venv/bin/pip install -r requirements.txt
```

---

## Running the Data Pipeline

Follow these steps in order to generate the initial mock datasets, compile claims, and run validations:

### Step 1: Generate Raw Data
Run the Jupyter notebooks in the `notebooks/` folder to generate the initial baseline data:
- `faker_data_generation.ipynb` generates mock profile records (`data/raw/fake_data.csv`).
- `insurance_data_generation.ipynb` generates mock insurance policy records (`data/raw/insurance_policies.csv`).

To run the notebook server:
```bash
.venv/bin/jupyter notebook
```

### Step 2: Generate Processed Claims
With the raw policies dataset populated, generate the insurance claims by running:
```bash
.venv/bin/python scripts/generate_claims.py
```
This updates the policies data with claim summaries and populates the processed claims files under `data/processed/` (including `insurance_claims.csv` and individual policy-type partitions).

### Step 3: Run Data Verification
Validate that all generated files respect the expected schema, sizes, logic, and integrity constraints:
```bash
.venv/bin/python scripts/verify_claims.py
```
You should see `ALL VERIFICATION CHECKS PASSED SUCCESSFULLY!` on terminal completion.

---

## Coding Guidelines & Standards

To keep the repository clean and maintainable, please adhere to standard Python conventions:
1. **PEP 8 Styling**: Use 4 spaces for indentation, write variables/functions in `snake_case`, and keep class names in `PascalCase`.
2. **Path Handling**: Never hardcode direct working-directory relative paths in scripts. Use `os.path.abspath` and `os.path.dirname(__file__)` to ensure scripts execute correctly regardless of where they are run from.
3. **Data Division**: Keep source datasets strictly isolated inside `data/raw/` and write code-generated/altered outputs into `data/processed/`.
