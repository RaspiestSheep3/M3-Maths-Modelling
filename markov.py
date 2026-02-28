

import numpy as np
import matplotlib.pyplot as plt

gender_input = "male"
age_input = 22
marital_input = "single living w/ sig other"
ethnicity_input = "black"
annual_di_input = 120000

def get_frt_score(age, gender, marital, annual_di, ethnicity):
    """
    Calculates Financial Risk Tolerance (FRT) using unstandardized b-coefficients.
    Includes full ranges for Age, Ethnicity, and Marital Status from Tables 4 & 5.
    """
    is_female = 1 if gender.lower() == "female" else 0

    # Constants
    score = 18.35 if is_female else 18.09

    # Personal Income (scaled per £10k)
    inc_units = annual_di / 10000.0
    score += (0.08 if is_female else 0.25) * inc_units

    if not is_female:
        # Male b-values (Table 5)
        # Marital Status
        if marital == "never married": score += 0.69
        elif marital == "single living w/ sig other": score += 2.19
        elif marital == "separated": score += 1.52
        elif marital == "divorced": score += 1.65
        elif marital == "widowed": score += 1.26
        # Age
        if 25 <= age <= 44: score -= 0.18
        elif 45 <= age <= 64: score -= 1.58
        elif age >= 65: score -= 1.44
        # Ethnicity
        if ethnicity == "black": score -= 1.68
        elif ethnicity == "hispanic": score -= 1.22
        elif ethnicity == "other": score -= 0.64
    else:
        # Female b-values (Table 4)
        # Marital Status
        if marital == "never married": score -= 0.16
        elif marital == "single living w/ sig other": score += 0.22
        elif marital == "separated": score -= 3.44
        elif marital == "divorced": score -= 0.85
        elif marital == "widowed": score += 0.34
        # Age
        if 25 <= age <= 44: score -= 0.92
        elif 45 <= age <= 64: score -= 1.36
        elif age >= 65: score -= 1.99
        # Ethnicity
        if ethnicity == "black": score += 0.31
        elif ethnicity == "hispanic": score += 0.01
        elif ethnicity == "other": score -= 0.10

    return score

def run_frenzy_sim_comprehensive(age, gender, marital, ethnicity, annual_di, n_sims=10000):
    frt = get_frt_score(age, gender, marital, annual_di, ethnicity)
    frt_norm = (max(13, min(frt, 47)) - 13) / (47 - 13)

    # UK 2026 Stats
    anchor = 38400.0
    alpha = 0.45 if gender.lower() == "male" else 0.25
    income_pressure = (anchor / max(1000, annual_di)) ** alpha

    # Transition Matrix (Request specific weights)
    P = np.array([
        [0.98, 0.015, 0.005],
        [0.30, 0.45, 0.25],
        [0.05, 0.13, 0.82] # Highly sticky frenzy state
    ])
    P = P / P.sum(axis=1)[:, None]

    # UK Ethnicity Scalar (Participation adjustment)
    eth_map = {"black": 1.15, "asian": 0.65, "white": 1.0, "hispanic": 1.05}
    e_scalar = eth_map.get(ethnicity.lower(), 1.0)

    total_outcomes = []
    active_outcomes = []

    for _ in range(n_sims):
        # 50% Population Baseline: Probability someone is a "Gambler" vs "Non-Gambler"
        is_gambler = np.random.rand() < 0.50
        
        if not is_gambler:
            total_outcomes.append(0.0)
            continue

        state, annual_loss = 0, 0
        for _ in range(365):
            state = np.random.choice([0, 1, 2], p=P[state])
            if state > 0:
                edge = 0.05 if state == 1 else (0.05 + 0.12 * (income_pressure**0.25))
                # mu scales with DI but also with the State Intensity
                mu_base = annual_di * (0.00015 if state == 1 else 0.0025)
                stochastic_wager = np.random.lognormal(np.log(mu_base), 1.2)
                annual_loss += (stochastic_wager * edge * e_scalar)
                
                if annual_loss > annual_di:
                    annual_loss = annual_di
                    break
        
        total_outcomes.append(annual_loss)
        if annual_loss > 0:
            active_outcomes.append(annual_loss)

    return total_outcomes, active_outcomes, frt

# Simulation Parameters: 22yo Single living w/ Sig Other Black Male, £12k DI

results_total, results_active, final_frt = run_frenzy_sim_comprehensive(
    age_input, gender_input, marital_input, ethnicity_input, annual_di_input
)

# Visualization
plt.figure(figsize=(12, 7))
plt.hist(results_active, bins=80, color='teal', alpha=0.8, edgecolor='white', label='Annual Active Loss')

# Calculate Means
mean_total = np.mean(results_total)
mean_active = np.mean(results_active)

plt.axvline(mean_active, color='gold', linestyle='--', linewidth=3, label=f'Mean (Active Gamblers Only): £{mean_active:.2f}')
plt.axvline(mean_total, color='orange', linestyle=':', linewidth=3, label=f'Mean (Full Population incl. £0): £{mean_total:.2f}')

plt.title(f"Annual Loss Distribution for Active Gamblers\nProfile: {age_input}yo {gender_input} | {marital_input} | {ethnicity_input} | {annual_di_input} DI | FRT: {final_frt:.2f}", fontsize=14)
plt.xlabel("Annual Net Loss (£)")
plt.ylabel("Frenzy (Frequency of Outcome)")
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.savefig('comprehensive_distribution.png')
plt.show()

print(f"Mean (Active): {mean_active}")
print(f"Mean (Total): {mean_total}")
print(f"95th Percentile: {np.percentile(results_active, 95)}")
print(f"97.5th Percentile: {np.percentile(results_active, 97.5)}")
print(f"99th Percentile: {np.percentile(results_active, 99)}")