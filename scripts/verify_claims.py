import pandas as pd
import os
from datetime import datetime

# Resolve paths relative to this script's directory for robust cross-directory execution
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
DATA_PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")

POLICIES_CSV_PATH = os.path.join(DATA_RAW_DIR, "insurance_policies.csv")
CLAIMS_CSV_PATH = os.path.join(DATA_PROCESSED_DIR, "insurance_claims.csv")

# Reference date aligned with the policies generation
REFERENCE_DATE = datetime.strptime("2026-05-09", "%Y-%m-%d").date()

def test_claims_data():
    print("Starting verification checks...")
    
    # 1. Check file existence
    assert os.path.exists(POLICIES_CSV_PATH), f"insurance_policies.csv not found at {POLICIES_CSV_PATH}!"
    assert os.path.exists(CLAIMS_CSV_PATH), f"insurance_claims.csv not found at {CLAIMS_CSV_PATH}!"
    
    policies = pd.read_csv(POLICIES_CSV_PATH)
    claims = pd.read_csv(CLAIMS_CSV_PATH)
    
    # 2. Check policy dataset shape
    assert len(policies) == 5000, f"Expected 5000 policies, got {len(policies)}"
    print("✓ Policies dataset contains exactly 5,000 rows.")
    
    # 3. Check claims ratio (exactly 30%)
    policies_with_claims = policies[policies['num_claims'] > 0]
    claims_ratio = len(policies_with_claims) / len(policies)
    assert len(policies_with_claims) == 1500, f"Expected 1500 policies with claims, got {len(policies_with_claims)}"
    assert claims_ratio == 0.30, f"Expected 0.30 claims ratio, got {claims_ratio}"
    print(f"✓ Exactly 30% of policies (1,500 of 5,000) have claims.")
    
    # 4. Check join integrity and matching keys
    policy_ids_in_claims = set(claims['policy_id'].unique())
    policy_ids_with_claims_field = set(policies_with_claims['policy_id'].unique())
    assert policy_ids_in_claims == policy_ids_with_claims_field, "Mismatch between policies with claims and policy_ids in claims table."
    print("✓ Join integrity verified: all policy IDs in claims match policies marked with claims.")
    
    # 5. Check claim count consistency
    claims_per_policy = claims.groupby('policy_id').size().to_dict()
    for _, row in policies.iterrows():
        p_id = row['policy_id']
        expected_claims = row['num_claims']
        actual_claims = claims_per_policy.get(p_id, 0)
        assert expected_claims == actual_claims, f"Claim count mismatch for {p_id}: policy has {expected_claims}, claims table has {actual_claims}"
    print("✓ Claim count column matches exact count of claims per policy in claims table.")
    
    # 6. Check claims paid summary consistency
    claims_paid_per_policy = claims.groupby('policy_id')['amount_paid'].sum().to_dict()
    for _, row in policies.iterrows():
        p_id = row['policy_id']
        expected_paid = row['total_claims_paid']
        actual_paid = round(claims_paid_per_policy.get(p_id, 0.0), 2)
        assert abs(expected_paid - actual_paid) < 0.01, f"Claims paid mismatch for {p_id}: policy says {expected_paid}, claims sum is {actual_paid}"
    print("✓ Total claims paid matches sum of paid claims per policy.")
    
    # 7. Check last claim date consistency
    last_claim_date_per_policy = claims.groupby('policy_id')['claim_date'].max().to_dict()
    for _, row in policies.iterrows():
        p_id = row['policy_id']
        if row['num_claims'] > 0:
            expected_date = row['last_claim_date']
            actual_date = last_claim_date_per_policy.get(p_id)
            assert expected_date == actual_date, f"Last claim date mismatch for {p_id}: policy says {expected_date}, claims table has {actual_date}"
        else:
            assert pd.isna(row['last_claim_date']), f"Policy {p_id} has 0 claims but non-null last_claim_date: {row['last_claim_date']}"
    print("✓ Last claim date matches the maximum claim date per policy.")
    
    # 8. Verify claim dates are within policy start/end dates and prior to reference date
    for _, row in claims.iterrows():
        p_id = row['policy_id']
        c_date_str = row['claim_date']
        c_date = datetime.strptime(c_date_str, "%Y-%m-%d").date()
        
        policy_row = policies[policies['policy_id'] == p_id].iloc[0]
        p_start = datetime.strptime(policy_row['policy_start_date'], "%Y-%m-%d").date()
        p_end = datetime.strptime(policy_row['policy_end_date'], "%Y-%m-%d").date()
        
        assert c_date >= p_start, f"Claim date {c_date} is before policy start date {p_start} for {p_id}"
        assert c_date <= p_end, f"Claim date {c_date} is after policy end date {p_end} for {p_id}"
        assert c_date <= REFERENCE_DATE, f"Claim date {c_date} is in the future relative to reference date {REFERENCE_DATE} for {p_id}"
    print("✓ All claim dates are strictly within policy periods and do not exceed the reference date.")
    
    # 9. Verify deductible and payment logic
    for _, row in claims.iterrows():
        p_id = row['policy_id']
        p_type = row['policy_type']
        deductible = row['deductible']
        c_amount = row['claim_amount']
        c_paid = row['amount_paid']
        status = row['claim_status']
        
        policy_row = policies[policies['policy_id'] == p_id].iloc[0]
        coverage_amount = policy_row['coverage_amount']
        
        if status == 'Denied':
            assert c_paid == 0.0, f"Denied claim {row['claim_id']} has non-zero payout {c_paid}"
        else:
            if p_type == 'Life':
                assert c_paid == c_amount, f"Life insurance claim payout should equal claim amount"
            else:
                expected_payout = max(0.0, c_amount - deductible)
                expected_payout = min(expected_payout, coverage_amount)
                assert abs(c_paid - expected_payout) < 0.01, f"Mismatch in payout logic for {row['claim_id']}: expected {expected_payout}, got {c_paid}"
    print("✓ Claim status, deductible application, and coverage limits correctly applied to payouts.")
    
    # 10. Check partitioned files consistency
    policy_types = ['Auto', 'Home', 'Life', 'Renters', 'Umbrella', 'Motorcycle', 'Boat']
    for p_type in policy_types:
        filename = f"claims_{p_type.lower()}.csv"
        partition_path = os.path.join(DATA_PROCESSED_DIR, filename)
        assert os.path.exists(partition_path), f"Partition file does not exist at {partition_path}!"
        type_df = pd.read_csv(partition_path)
        master_subset = claims[claims['policy_type'] == p_type]
        assert len(type_df) == len(master_subset), f"Row count mismatch in {filename}: partition has {len(type_df)}, master subset has {len(master_subset)}"
        assert set(type_df['claim_id']) == set(master_subset['claim_id']), f"ID mismatch in {filename}"
        print(f"✓ Partition file {filename} verified successfully ({len(type_df)} rows).")

    print("\nALL VERIFICATION CHECKS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_claims_data()
