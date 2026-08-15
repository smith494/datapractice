# Insurance Policy Data Generator

## Overview

This script generates synthetic insurance policy data using the Python `Faker` library. The data mimics a realistic insurance book of business with weighted distributions, conditional logic, and correlated fields suitable for data analysis practice and dashboard building.

## Requirements

```bash
pip install faker pandas numpy
```

## Purpose

- Practice data analysis, cleaning, and visualization skills
- Build dashboards (Streamlit, Plotly Dash, Power BI, Tableau, etc.)
- Test statistical methods on realistic-looking insurance data

## Dataset Characteristics

- **Volume:** 5,000 policies (configurable via `NUM_POLICIES`)
- **Reproducibility:** Seeded with `42` for consistent output across runs
- **Realism features:**
  - Premiums correlate with coverage amount and risk tier (not random)
  - Weighted distributions for policy types, statuses, and risk tiers
  - Conditional fields (claim details only populate when claims exist)
  - Policy-type-specific discounts (e.g., safe driver only for Auto/Motorcycle)

## Schema

### Identifiers
| Column | Type | Description |
|--------|------|-------------|
| `policy_id` | string | Unique policy identifier (POL-XXXXXXX) |
| `customer_id` | string | Unique customer identifier (CUST-XXXXXX) |
| `agent_id` | string | Assigned agent (AGT-XXXX) |

### Customer Demographics
| Column | Type | Description |
|--------|------|-------------|
| `first_name`, `last_name` | string | Customer name |
| `date_of_birth`, `age` | date / int | DOB and computed age |
| `gender` | string | M / F |
| `marital_status` | string | Single, Married, Divorced, Widowed |
| `education` | string | High School through Doctorate |
| `occupation` | string | Job title |
| `annual_income` | float | Lognormal distribution |
| `credit_score` | int | Normal distribution centered at 720, clipped 300–850 |

### Contact & Geography
| Column | Type | Description |
|--------|------|-------------|
| `email`, `phone` | string | Contact info |
| `address`, `city`, `state`, `zip_code` | string | Full US address |

### Policy Details
| Column | Type | Description |
|--------|------|-------------|
| `policy_type` | string | Auto, Home, Life, Renters, Umbrella, Motorcycle, Boat |
| `policy_status` | string | Active, Lapsed, Cancelled, Pending Renewal, Expired |
| `risk_tier` | string | Preferred, Standard, Substandard, High Risk |
| `coverage_amount` | float | Policy-type-appropriate ranges |
| `deductible` | int | 250, 500, 1000, 2500, or 5000 |
| `annual_premium`, `monthly_premium` | float | Calculated from coverage × risk × base rate |
| `payment_frequency` | string | Monthly, Quarterly, Semi-Annual, Annual |
| `policy_start_date`, `policy_end_date` | date | Policy term |
| `tenure_years` | float | Years since policy start |

### Acquisition & Engagement
| Column | Type | Description |
|--------|------|-------------|
| `acquisition_channel` | string | Agent, Online, Phone, Mobile App |
| `has_multi_policy_discount` | bool | Multi-line discount flag |
| `has_safe_driver_discount` | bool | Auto/Motorcycle only |
| `nps_score` | int | 0–10 |
| `customer_lifetime_value` | float | Estimated CLV |

### Claims
| Column | Type | Description |
|--------|------|-------------|
| `num_claims` | int | 0–5, weighted toward 0 |
| `total_claims_paid` | float | 0 if no claims |
| `last_claim_date` | date / null | Null if no claims |
| `primary_claim_type` | string / null | Policy-type-appropriate claim category |

## Distribution Weights

```
Policy Type:       Auto 45%, Home 25%, Life 12%, Renters 8%,
                   Umbrella 4%, Motorcycle 4%, Boat 2%
Policy Status:     Active 70%, Lapsed 10%, Cancelled 8%,
                   Pending Renewal 8%, Expired 4%
Risk Tier:         Preferred 35%, Standard 45%, Substandard 15%,
                   High Risk 5%
Channel:           Agent 50%, Online 30%, Phone 12%, Mobile App 8%
Claims:            0 claims 65%, 1 claim 20%, 2+ claims 15%
```

## Code

```python
# Install if needed: pip install faker pandas numpy

from faker import Faker
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Initialize Faker with a seed for reproducibility
fake = Faker('en_US')
Faker.seed(42)
random.seed(42)
np.random.seed(42)

# ---------- Configuration ----------
NUM_POLICIES = 5000

POLICY_TYPES = ['Auto', 'Home', 'Life', 'Renters', 'Umbrella', 'Motorcycle', 'Boat']
POLICY_TYPE_WEIGHTS = [0.45, 0.25, 0.12, 0.08, 0.04, 0.04, 0.02]

POLICY_STATUSES = ['Active', 'Lapsed', 'Cancelled', 'Pending Renewal', 'Expired']
STATUS_WEIGHTS = [0.70, 0.10, 0.08, 0.08, 0.04]

PAYMENT_FREQUENCIES = ['Monthly', 'Quarterly', 'Semi-Annual', 'Annual']
PAYMENT_WEIGHTS = [0.55, 0.15, 0.20, 0.10]

CHANNELS = ['Agent', 'Online', 'Phone', 'Mobile App']
CHANNEL_WEIGHTS = [0.50, 0.30, 0.12, 0.08]

MARITAL_STATUSES = ['Single', 'Married', 'Divorced', 'Widowed']
EDUCATION = ['High School', 'Some College', 'Bachelor', 'Master', 'Doctorate']
RISK_TIERS = ['Preferred', 'Standard', 'Substandard', 'High Risk']
RISK_WEIGHTS = [0.35, 0.45, 0.15, 0.05]

CLAIM_TYPES_BY_POLICY = {
    'Auto': ['Collision', 'Comprehensive', 'Liability', 'Uninsured Motorist'],
    'Home': ['Wind/Hail', 'Water Damage', 'Fire', 'Theft', 'Liability'],
    'Life': ['Death Benefit'],
    'Renters': ['Theft', 'Fire', 'Water Damage'],
    'Umbrella': ['Liability'],
    'Motorcycle': ['Collision', 'Comprehensive', 'Liability'],
    'Boat': ['Collision', 'Storm Damage', 'Theft']
}

# ---------- Helper functions ----------
def generate_premium(policy_type, risk_tier, coverage_amount):
    """Generate realistic premium based on policy type and risk."""
    base_rates = {
        'Auto': 0.04, 'Home': 0.005, 'Life': 0.008, 'Renters': 0.015,
        'Umbrella': 0.002, 'Motorcycle': 0.05, 'Boat': 0.015
    }
    risk_multipliers = {
        'Preferred': 0.85, 'Standard': 1.0, 'Substandard': 1.35, 'High Risk': 1.75
    }
    base = coverage_amount * base_rates[policy_type] * risk_multipliers[risk_tier]
    # Add some noise
    return round(base * np.random.uniform(0.85, 1.15), 2)

def generate_coverage(policy_type):
    """Generate realistic coverage amounts by policy type."""
    ranges = {
        'Auto': (25000, 300000),
        'Home': (150000, 800000),
        'Life': (50000, 2000000),
        'Renters': (15000, 100000),
        'Umbrella': (1000000, 5000000),
        'Motorcycle': (15000, 50000),
        'Boat': (20000, 250000)
    }
    low, high = ranges[policy_type]
    return round(np.random.uniform(low, high), -3)  # Round to nearest 1000

# ---------- Generate the dataset ----------
records = []

for i in range(NUM_POLICIES):
    policy_type = np.random.choice(POLICY_TYPES, p=POLICY_TYPE_WEIGHTS)
    risk_tier = np.random.choice(RISK_TIERS, p=RISK_WEIGHTS)
    coverage = generate_coverage(policy_type)
    annual_premium = generate_premium(policy_type, risk_tier, coverage)

    # Dates
    policy_start = fake.date_between(start_date='-5y', end_date='today')
    policy_end = policy_start + timedelta(days=365 * random.choice([1, 1, 1, 2, 3]))

    # Customer demographics
    dob = fake.date_of_birth(minimum_age=22, maximum_age=85)
    age = (datetime.now().date() - dob).days // 365

    # Geography
    state = fake.state_abbr()

    record = {
        # Policy identifiers
        'policy_id': f'POL-{1000000 + i}',
        'customer_id': f'CUST-{500000 + i}',

        # Customer info
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'date_of_birth': dob,
        'age': age,
        'gender': np.random.choice(['M', 'F'], p=[0.49, 0.51]),
        'marital_status': random.choice(MARITAL_STATUSES),
        'education': random.choice(EDUCATION),
        'occupation': fake.job(),
        'annual_income': round(np.random.lognormal(11, 0.5), -2),
        'credit_score': int(np.clip(np.random.normal(720, 80), 300, 850)),

        # Contact
        'email': fake.email(),
        'phone': fake.phone_number(),
        'address': fake.street_address(),
        'city': fake.city(),
        'state': state,
        'zip_code': fake.zipcode(),

        # Policy details
        'policy_type': policy_type,
        'policy_status': np.random.choice(POLICY_STATUSES, p=STATUS_WEIGHTS),
        'risk_tier': risk_tier,
        'coverage_amount': coverage,
        'deductible': random.choice([250, 500, 1000, 2500, 5000]),
        'annual_premium': annual_premium,
        'monthly_premium': round(annual_premium / 12, 2),
        'payment_frequency': np.random.choice(PAYMENT_FREQUENCIES, p=PAYMENT_WEIGHTS),
        'policy_start_date': policy_start,
        'policy_end_date': policy_end,
        'tenure_years': round((datetime.now().date() - policy_start).days / 365, 1),

        # Acquisition
        'acquisition_channel': np.random.choice(CHANNELS, p=CHANNEL_WEIGHTS),
        'agent_id': f'AGT-{random.randint(1000, 1500)}',

        # Claims data
        'num_claims': np.random.choice([0, 1, 2, 3, 4, 5], p=[0.65, 0.20, 0.08, 0.04, 0.02, 0.01]),
        'has_multi_policy_discount': np.random.choice([True, False], p=[0.4, 0.6]),
        'has_safe_driver_discount': np.random.choice([True, False], p=[0.55, 0.45]) if policy_type in ['Auto', 'Motorcycle'] else False,

        # Customer satisfaction
        'nps_score': random.randint(0, 10),
        'customer_lifetime_value': round(annual_premium * np.random.uniform(3, 15), 2),
    }

    # Add claim total based on num_claims
    if record['num_claims'] > 0:
        record['total_claims_paid'] = round(np.random.uniform(500, 50000) * record['num_claims'], 2)
        record['last_claim_date'] = fake.date_between(start_date=policy_start, end_date='today')
        record['primary_claim_type'] = random.choice(CLAIM_TYPES_BY_POLICY[policy_type])
    else:
        record['total_claims_paid'] = 0.0
        record['last_claim_date'] = None
        record['primary_claim_type'] = None

    records.append(record)

# Create DataFrame
df = pd.DataFrame(records)

# Quick sanity check
print(f"Generated {len(df)} policies")
print(f"\nColumns: {list(df.columns)}")
print(f"\nPolicy type distribution:")
print(df['policy_type'].value_counts())
print(f"\nFirst few rows:")
df.head()
```

## Saving the Data

```python
# CSV (human-readable, larger file)
df.to_csv('insurance_policies.csv', index=False)

# Parquet (compressed, faster for analytics)
df.to_parquet('insurance_policies.parquet')

# JSON (for API/web use)
df.to_json('insurance_policies.json', orient='records', date_format='iso')
```

## Suggested Next Steps

1. **Exploratory Data Analysis** — distributions, missingness, correlations
2. **Data cleaning practice** — handle the intentional nulls in claim fields
3. **Aggregations** — premium by state, claim frequency by risk tier, channel performance
4. **Time series** — policy growth over time, claims by month
5. **Dashboard build** — Streamlit or Plotly Dash recommended; key views:
   - Portfolio overview (total policies, premium, active rate)
   - Geographic heatmap of policies/premiums by state
   - Claims analysis by policy type and risk tier
   - Customer segmentation by CLV and tenure
   - Acquisition channel performance funnel

## Customization Notes

- Increase `NUM_POLICIES` for larger datasets (tested up to 100k without issue)
- Remove `Faker.seed(42)`, `random.seed(42)`, and `np.random.seed(42)` for non-reproducible randomness
- Adjust weight arrays to simulate different portfolio compositions
- Add new policy types or claim categories by extending the dictionaries at the top
