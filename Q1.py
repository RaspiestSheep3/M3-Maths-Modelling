import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class UKModelRegional:
    def __init__(self, data_file, inflation_rate=0.04): # 4% projected inflation to 2026
        self.df = pd.read_excel(data_file)
        self.inflation_factor = 1.0 + inflation_rate
        self.essentials_data, self.quintile_income_map = self._parse_ons_data()
        self.regional_multipliers = self._calculate_regional_factors()
        
    def _parse_ons_data(self):
        age_ranges = {"Under 30": (2, 18), "30-49": (19, 35), "50-64": (36, 52), "65-74": (53, 69), "Over 74": (70, 86)}
        essential_categories = ["Food & non-alcoholic drinks", "Clothing & footwear", "Housing(net)², fuel & power", 
                                "Household goods & services", "Health", "Transport", "Communication", 
                                "Education", "Miscellaneous goods & services", "Other expenditure items"]
        
        parsed_essentials = {}
        for age, (start, end) in age_ranges.items():
            subset = self.df.iloc[start:end+1, 0:7]
            subset.columns = ['Category', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'All']
            subset = subset.set_index('Category')
            relevant_rows = subset.index.intersection(essential_categories)
            essentials_sum = subset.loc[relevant_rows].apply(pd.to_numeric, errors='coerce').fillna(0).sum()
            parsed_essentials[age] = essentials_sum.to_dict()
    
        income_row = self.df.iloc[3, 9:14].values.astype(float)
        # convert map to lists for numpy interpolation later
        quintile_incomes = {
            'x_incomes': [income_row[0], income_row[1], income_row[2], income_row[3], income_row[4]],
            'keys': ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']
        }
        return parsed_essentials, quintile_incomes

    def _calculate_regional_factors(self):
        regional_subset = self.df.iloc[10:24, 8:14]
        regional_subset.columns = ['Category', 'England ', 'Wales', 'Scotland', 'Northern Ireland', 'All UK']
        regional_subset = regional_subset.set_index('Category')
        totals = regional_subset.apply(pd.to_numeric, errors='coerce').fillna(0).sum()
        factors = totals / totals['All UK']
        return factors.to_dict()

    def _calculate_tax_and_ni(self, salary):
        #fiscal model including the 100k personal allowance taper

        personal_allowance = 12570
        if salary > 100000:
            taper_deduction = (salary - 100000) / 2
            personal_allowance = max(0, personal_allowance - taper_deduction)
            
        taxable = max(0, salary - personal_allowance)
        tax = 0
        
        if taxable > 0:
            basic_band = min(taxable, 37700)
            tax += basic_band * 0.20
            taxable -= basic_band
            
        if taxable > 0:
            higher_band = min(taxable, 125140 - 37700 - 12570)
            tax += higher_band * 0.40
            taxable -= higher_band
            
        if taxable > 0:
            tax += taxable * 0.45

        #NI calcs
        ni = 0
        if salary > 12570:
            ni_basic = min(salary - 12570, 50270 - 12570) * 0.08
            ni_higher = max(0, salary - 50270) * 0.02
            ni = ni_basic + ni_higher

        return tax, ni

    def estimate_disposable(self, salary, age, region="England "):
        if age < 30: age_key = "Under 30"
        elif age <= 49: age_key = "30-49"
        elif age <= 64: age_key = "50-64"
        else: age_key = "65-74" 
        
        weekly_gross = salary / 52
        
        #continuous interpolation for essentials
        x_vals = self.quintile_income_map['x_incomes']
        y_vals = [self.essentials_data[age_key][k] for k in self.quintile_income_map['keys']]
        
        base_weekly_essentials = np.interp(weekly_gross, x_vals, y_vals)
        
        #applying multipliers (for region and inflation)
        adj_weekly_essentials = base_weekly_essentials * self.regional_multipliers.get(region, 1.0) * self.inflation_factor
        yearly_essentials = adj_weekly_essentials * 52

        tax, ni = self._calculate_tax_and_ni(salary)
        
        #final calcs
        total_deductions = tax + ni
        disposable = salary - total_deductions - yearly_essentials
        
        return {
            "Region": region,
            "Gross": round(salary, 2),
            "Tax": round(tax, 2),
            "NI": round(ni, 2),
            "Essential_Costs": round(yearly_essentials, 2),
            "Disposable": round(max(0, disposable), 2)
        }


model = UKModelRegional('UK_Data.xlsx')

salaries = np.linspace(20000, 80000, 50) #generating 50 salaries from 20 to 80k

#plotting correlation of region and disposable income
regions = ['England ', 'Wales', 'Scotland', 'Northern Ireland']
plt.figure(figsize=(10, 6))
for r in regions:
    disp = [model.estimate_disposable(s, 25, r)['Disposable'] for s in salaries]
    plt.plot(salaries, disp, label=r.strip(), linewidth=2)

plt.title('Impact of Region on Disposable Income (Age 25)', fontsize=14)
plt.xlabel('Gross Annual Salary (£)', fontsize=12)
plt.ylabel('Disposable Income (£)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.savefig('Figure1_Regional_Impact.png')
plt.close()


#plotting correlation of age and disposable income
ages = [22, 40, 60]
labels = ['Under 30', '30-49', '50-64']

plt.figure(figsize=(10, 6))
for a, l in zip(ages, labels):
    disp = [model.estimate_disposable(s, a, 'England ')['Disposable'] for s in salaries]
    plt.plot(salaries, disp, label=l, linewidth=2)

plt.title('Impact of Age Bracket on Disposable Income (England)', fontsize=14)
plt.xlabel('Gross Annual Salary (£)', fontsize=12)
plt.ylabel('Disposable Income (£)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.savefig('Figure2_Age_Impact.png')
plt.close()


#4-part financial breakdown
res = model.estimate_disposable(40000, 28, 'England ')

labels = ['Income Tax', 'National Insurance', 'Essential Costs', 'Disposable Income']
sizes = [res['Tax'], res['NI'], res['Essential_Costs'], res['Disposable']]
colors = ['#ff9999', '#ffcc99', '#66b3ff', '#99ff99']

plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, 
        wedgeprops={'edgecolor': 'black', 'linewidth': 1})
plt.title('Financial Breakdown: 28-year-old earning £40,000 (England)', fontsize=14)
plt.tight_layout()
plt.savefig('Figure3_Breakdown.png')
plt.close()

#layer stacked bar chart for test cases
test_profiles = [
    {"salary": 21571, "age": 30, "region": "Wales", "label": "Profile A\n(£21.5k, Age 30, Wales)"},
    {"salary": 34199, "age": 25, "region": "England ", "label": "Profile B\n(£34.1k, Age 25, England)"},
    {"salary": 45918, "age": 45, "region": "Northern Ireland", "label": "Profile C\n(£45.9k, Age 45, NI)"},
    {"salary": 73519, "age": 65, "region": "Scotland", "label": "Profile D\n(£73.5k, Age 65, Scotland)"}
]

# Run the model on the test cases
results = []
for p in test_profiles:
    res = model.estimate_disposable(p['salary'], p['age'], p['region'])
    results.append({
        'label': p['label'],
        'Taxes': res['Tax'],
        'NI': res['NI'],
        'Essentials': res['Essential_Costs'],
        'Disposable': res['Disposable'],
        'Gross': res['Gross']
    })

#preparing data for the 4-layer stacked bar chart
labels = [r['label'] for r in results]
taxes = np.array([r['Taxes'] for r in results])
ni = np.array([r['NI'] for r in results])
essentials = np.array([r['Essentials'] for r in results])
disposable = np.array([r['Disposable'] for r in results])

fig, ax = plt.subplots(figsize=(11, 7))
width = 0.55
x = np.arange(len(labels))

#stack the bars from bottom to top
p1 = ax.bar(x, taxes, width, label='Income Tax', color='#ff9999', edgecolor='black')
p2 = ax.bar(x, ni, width, bottom=taxes, label='National Insurance', color='#ffcc99', edgecolor='black')
p3 = ax.bar(x, essentials, width, bottom=taxes+ni, label='Essential Costs', color='#66b3ff', edgecolor='black')
p4 = ax.bar(x, disposable, width, bottom=taxes+ni+essentials, label='Disposable Income', color='#99ff99', edgecolor='black')

#formatting
ax.set_ylabel('Annual Amount (£)', fontsize=12)
ax.set_title('Salary Breakdown by Demographic Test Cases', fontsize=14, pad=20)
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=11)
ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

for i in range(len(labels)):
    total_height = taxes[i] + ni[i] + essentials[i] + disposable[i]
    if disposable[i] > 0:
        ax.text(x[i], total_height - (disposable[i]/2), f"£{disposable[i]:,.0f}", 
                ha='center', va='center', color='black', fontweight='bold')
    else:
        ax.text(x[i], taxes[i] + ni[i] + essentials[i] + 500, f"£0", 
                ha='center', va='bottom', color='red', fontweight='bold')

plt.tight_layout()
plt.savefig('Figure4_Test_Cases.png')
