import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta, date
from faker import Faker

# Resolve paths relative to this script's directory for robust cross-directory execution
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
DATA_PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")

POLICIES_CSV_PATH = os.path.join(DATA_RAW_DIR, "insurance_policies.csv")
CLAIMS_CSV_PATH = os.path.join(DATA_PROCESSED_DIR, "insurance_claims.csv")


# Set seed for reproducibility
random.seed(42)
np.random.seed(42)
fake = Faker()
Faker.seed(42)

# Reference date aligned with the policies generation
REFERENCE_DATE = date(2026, 5, 9)

# Claim types matching insurance_data_generation.ipynb
CLAIM_TYPES_BY_POLICY = {
    'Auto': ['Collision', 'Comprehensive', 'Liability', 'Uninsured Motorist'],
    'Home': ['Wind/Hail', 'Water Damage', 'Fire', 'Theft', 'Liability'],
    'Life': ['Death Benefit'],
    'Renters': ['Theft', 'Fire', 'Water Damage'],
    'Umbrella': ['Liability'],
    'Motorcycle': ['Collision', 'Comprehensive', 'Liability'],
    'Boat': ['Collision', 'Storm Damage', 'Theft']
}

# Incident descriptions by policy type and claim type for premium look and feel
INCIDENT_DESCRIPTIONS = {
    'Auto': {
        'Collision': [
            "Rear-end collision at a traffic intersection.",
            "Collided with a stationary utility pole while parking.",
            "Sideswiped by another vehicle merging onto the highway.",
            "Multi-vehicle accident on wet roadway."
        ],
        'Comprehensive': [
            "Windshield cracked by a rock flying from a dump truck.",
            "Vehicle vandalized with spray paint in a public parking lot.",
            "Collided with a deer crossing the road at night.",
            "Hail storm caused extensive denting on hood and roof."
        ],
        'Liability': [
            "Backed into neighbor's parked car causing bumper damage.",
            "Ran a stop sign and hit a bicyclist, causing minor injuries.",
            "Third-party property damage to a storefront fence."
        ],
        'Uninsured Motorist': [
            "Rear-ended by an uninsured driver who fled the scene.",
            "Hit-and-run incident in a shopping mall parking structure."
        ]
    },
    'Home': {
        'Wind/Hail': [
            "Severe thunderstorm tore off several roof shingles.",
            "Hail storm damaged vinyl siding and cracked windows.",
            "Fallen tree limb damaged the backyard deck during a storm."
        ],
        'Water Damage': [
            "Burst pipe in the upstairs bathroom flooded the ceiling below.",
            "Water heater failed, leaking water across the laundry room floor.",
            "Dishwasher overflowed, damaging kitchen hardwood floors."
        ],
        'Fire': [
            "Grease fire in the kitchen caused severe cabinet and smoke damage.",
            "Electrical fire in the garage damaged walls and tools.",
            "Chimney fire caused attic and roof structure damage."
        ],
        'Theft': [
            "Break-in through rear window; jewelry and electronics stolen.",
            "Lawnmower and power tools stolen from locked backyard shed.",
            "Porch pirate stole high-value packages delivered to front door."
        ],
        'Liability': [
            "Mail carrier slipped on icy front steps and sprained ankle.",
            "Family dog bit a neighbor visiting the backyard.",
            "Guest tripped over a loose rug and fractured their wrist."
        ]
    },
    'Life': {
        'Death Benefit': [
            "Passed away due to natural causes.",
            "Fatal cardiovascular event.",
            "Passed away from complications of pneumonia.",
            "Accidental death in a domestic incident."
        ]
    },
    'Renters': {
        'Theft': [
            "Apartment burglary; laptop, tablet, and gaming console stolen.",
            "Bicycle stolen from the apartment complex bike rack."
        ],
        'Fire': [
            "Candle left unattended started a small bedroom fire.",
            "Toaster oven caught fire, causing kitchen smoke damage."
        ],
        'Water Damage': [
            "Leaking pipe in the wall damaged living room furniture.",
            "Bathtub overflow from the apartment above leaked through ceiling."
        ]
    },
    'Umbrella': {
        'Liability': [
            "Excess liability claim following a major multi-car auto accident.",
            "Settlement for personal injury lawsuit stemming from rental property.",
            "Defamation lawsuit settlement."
        ]
    },
    'Motorcycle': {
        'Collision': [
            "Lost control on gravel curve, laying down the motorcycle.",
            "Car turned left in front of motorcycle at an intersection.",
            "Collided with a guardrail while avoiding a sudden obstacle."
        ],
        'Comprehensive': [
            "Motorcycle blown over and damaged during a windstorm.",
            "Motorcycle stolen from apartment complex parking lot.",
            "Fuel tank dented and seat slashed while parked overnight."
        ],
        'Liability': [
            "Passenger injured when motorcycle slid on wet leaves.",
            "Accidentally scraped side of a parked luxury sedan."
        ]
    },
    'Boat': {
        'Collision': [
            "Collided with a floating log in the lake, damaging the hull.",
            "Scraped against the dock wall during high winds.",
            "Collided with another vessel while navigating a narrow channel."
        ],
        'Storm Damage': [
            "Boat filled with water and sank at its slip during a heavy storm.",
            "Lightning strike fried the onboard marine electronics."
        ],
        'Theft': [
            "Outboard motor stolen from boat parked in driveway.",
            "Fishing gear and GPS equipment stolen from locked cabin."
        ]
    }
}

def generate_claim_amount(policy_type, coverage_amount):
    """Generates a realistic claim amount based on policy type and coverage amount."""
    if policy_type == 'Life':
        # Life insurance always pays the full coverage amount
        return float(coverage_amount)
    
    # Define typical loss distribution scale factors
    scales = {
        'Auto': 8000,
        'Home': 25000,
        'Renters': 4000,
        'Umbrella': 150000,
        'Motorcycle': 7000,
        'Boat': 15000
    }
    scale = scales.get(policy_type, 10000)
    
    # Use exponential distribution for claim amounts (most claims are small, few are very large)
    amount = np.random.exponential(scale=scale)
    # Ensure it's at least $500 and capped at the coverage amount
    amount = np.clip(amount, 500, coverage_amount)
    return round(float(amount), 2)

def generate_claim_date(start_date, end_date):
    """Generates a random date between start_date and end_date, capped at REFERENCE_DATE."""
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()
    
    # Cap the end date at REFERENCE_DATE to prevent future claims
    max_date = min(end, REFERENCE_DATE)
    
    if start >= max_date:
        return start
    
    days_range = (max_date - start).days
    random_days = random.randint(0, days_range)
    return start + timedelta(days=random_days)

def get_claim_status(claim_date):
    """Determines claim status based on age of the claim."""
    days_old = (REFERENCE_DATE - claim_date).days
    if days_old <= 15:
        return np.random.choice(['Under Review', 'Approved'], p=[0.70, 0.30])
    elif days_old <= 45:
        return np.random.choice(['Under Review', 'Approved', 'Paid', 'Denied'], p=[0.15, 0.15, 0.60, 0.10])
    else:
        # Older claims are almost all resolved (Paid or Denied)
        return np.random.choice(['Paid', 'Denied'], p=[0.90, 0.10])

def repair_policy_dates(policies_df):
    """Repairs any policies where policy_end_date is before policy_start_date."""
    repaired_count = 0
    for idx, row in policies_df.iterrows():
        start_dt = datetime.strptime(row['policy_start_date'], "%Y-%m-%d").date()
        end_dt = datetime.strptime(row['policy_end_date'], "%Y-%m-%d").date()
        
        if end_dt < start_dt:
            # Re-generate a valid end date
            status = row['policy_status']
            if status == 'Active':
                new_end = start_dt + timedelta(days=365)
            elif status == 'Pending Renewal':
                new_end = REFERENCE_DATE + timedelta(days=30)
            elif status in ['Lapsed', 'Cancelled']:
                new_end = start_dt + timedelta(days=180)
            else: # Expired
                new_end = start_dt + timedelta(days=180)
                
            policies_df.at[idx, 'policy_end_date'] = new_end.strftime("%Y-%m-%d")
            repaired_count += 1
            print(f"Repaired policy {row['policy_id']} dates: {row['policy_start_date']} to {new_end.strftime('%Y-%m-%d')} (Status: {status})")
    
    if repaired_count > 0:
        print(f"Repaired {repaired_count} policies with invalid date ranges.")

def main():
    print(f"Loading {POLICIES_CSV_PATH}...")
    policies_df = pd.read_csv(POLICIES_CSV_PATH)
    num_policies = len(policies_df)
    print(f"Loaded {num_policies} policies.")
    
    # Repair date range anomalies if any
    repair_policy_dates(policies_df)
    
    # Reset all claims columns in the policies table to represent the starting state
    policies_df['num_claims'] = 0
    policies_df['total_claims_paid'] = 0.0
    policies_df['last_claim_date'] = pd.NA
    policies_df['primary_claim_type'] = pd.NA
    
    # Select exactly 30% of policies to have claims
    target_claims_policies_count = int(num_policies * 0.30)
    claims_policy_indices = np.random.choice(policies_df.index, size=target_claims_policies_count, replace=False)
    print(f"Selected {len(claims_policy_indices)} policies (30%) to have claims.")
    
    claims_records = []
    claim_counter = 100001
    
    for idx in claims_policy_indices:
        policy = policies_df.loc[idx]
        policy_id = policy['policy_id']
        customer_id = policy['customer_id']
        policy_type = policy['policy_type']
        deductible = float(policy['deductible'])
        coverage_amount = float(policy['coverage_amount'])
        start_date = policy['policy_start_date']
        end_date = policy['policy_end_date']
        
        # Determine number of claims for this policy (1 to 3 claims)
        num_claims = np.random.choice([1, 2, 3], p=[0.75, 0.20, 0.05])
        
        policy_claims = []
        for _ in range(num_claims):
            c_date = generate_claim_date(start_date, end_date)
            c_type = random.choice(CLAIM_TYPES_BY_POLICY[policy_type])
            c_amount = generate_claim_amount(policy_type, coverage_amount)
            c_status = get_claim_status(c_date)
            
            # Calculate amount paid based on status and deductible
            if c_status == 'Denied':
                c_amount_paid = 0.0
            else:
                # Deductible applies to everything except Life Insurance
                if policy_type == 'Life':
                    c_amount_paid = c_amount
                else:
                    c_amount_paid = max(0.0, c_amount - deductible)
                # Cap the payout at coverage limit
                c_amount_paid = min(c_amount_paid, coverage_amount)
            
            desc = random.choice(INCIDENT_DESCRIPTIONS[policy_type][c_type])
            
            claim_record = {
                'claim_id': f"CLM-{claim_counter}",
                'policy_id': policy_id,
                'customer_id': customer_id,
                'policy_type': policy_type,
                'claim_date': c_date.strftime("%Y-%m-%d"),
                'claim_type': c_type,
                'claim_amount': round(c_amount, 2),
                'deductible': deductible,
                'amount_paid': round(c_amount_paid, 2),
                'claim_status': c_status,
                'incident_description': desc
            }
            policy_claims.append(claim_record)
            claim_counter += 1
            
        # Sort claims by date for this policy to find the last claim correctly
        policy_claims.sort(key=lambda x: x['claim_date'])
        claims_records.extend(policy_claims)
        
        # Calculate summary statistics for the policies table
        num_claims_val = len(policy_claims)
        total_paid_val = sum(c['amount_paid'] for c in policy_claims if c['claim_status'] != 'Denied')
        last_claim_date_val = policy_claims[-1]['claim_date']
        primary_claim_type_val = policy_claims[-1]['claim_type']  # Latest claim type
        
        # Update policy row
        policies_df.at[idx, 'num_claims'] = num_claims_val
        policies_df.at[idx, 'total_claims_paid'] = round(total_paid_val, 2)
        policies_df.at[idx, 'last_claim_date'] = last_claim_date_val
        policies_df.at[idx, 'primary_claim_type'] = primary_claim_type_val

    # Convert claims records to DataFrame
    claims_df = pd.DataFrame(claims_records)
    print(f"Generated {len(claims_df)} total claims.")
    
    # Save the updated policies DataFrame back to insurance_policies.csv
    policies_df.to_csv(POLICIES_CSV_PATH, index=False)
    print(f"Updated {POLICIES_CSV_PATH} successfully.")
    
    # Save master claims file
    claims_df.to_csv(CLAIMS_CSV_PATH, index=False)
    print(f"Saved master claims to {CLAIMS_CSV_PATH}.")
    
    # Save partitioned claims by policy type
    for policy_type in CLAIM_TYPES_BY_POLICY.keys():
        type_claims_df = claims_df[claims_df['policy_type'] == policy_type]
        filename = f"claims_{policy_type.lower()}.csv"
        partition_path = os.path.join(DATA_PROCESSED_DIR, filename)
        type_claims_df.to_csv(partition_path, index=False)
        print(f"Saved {len(type_claims_df)} claims to {partition_path}.")

if __name__ == "__main__":
    main()
