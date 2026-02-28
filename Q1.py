import pandas as pd

class UKModelRegional:
    def __init__(self, data_file):
        # Using encoding='latin1' to handle the pound sign and special characters
        self.df = pd.read_excel(data_file)
        self.essentials_data, self.quintile_income_map = self._parse_ons_data()
        self.regional_multipliers = self._calculate_regional_factors()
        
    def _parse_ons_data(self):
        """Parses Age/Income quintile essentials (same as before)"""
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
        quintile_incomes = {'Q1': income_row[0], 'Q2': income_row[1], 'Q3': income_row[2], 'Q4': income_row[3], 'Q5': income_row[4]}

        return parsed_essentials, quintile_incomes

    def _calculate_regional_factors(self):
        """Extracts the Regional Expenditure and creates a scaling factor relative to the 'All UK' average."""
        # Regional data is in rows 10-23, columns 9-13
        regional_subset = self.df.iloc[10:24, 8:14]
        regional_subset.columns = ['Category', 'England', 'Wales', 'Scotland', 'Northern Ireland', 'All UK']
        regional_subset = regional_subset.set_index('Category')
        
        # Total expenditure by region
        totals = regional_subset.apply(pd.to_numeric, errors='coerce').fillna(0).sum()
        
        # Factor = (Region Total) / (All UK Average)
        factors = totals / totals['All UK']
        return factors.to_dict()

    def estimate_disposable(self, salary, age, region="England"):
        # 1. Age Mapping
        if age < 30: age_key = "Under 30"
        elif age <= 49: age_key = "30-49"
        elif age <= 64: age_key = "50-64"
        else: age_key = "65-74" # Grouping 65+ for simplicity
        
        # 2. Quintile Mapping (Weekly)
        weekly_gross = salary / 52
        closest_q = 'Q1'
        for q, inc in self.quintile_income_map.items():
            if weekly_gross >= inc: closest_q = q
        
        # 3. Apply Regional Adjustment
        base_weekly_essentials = self.essentials_data[age_key][closest_q]
        adj_weekly_essentials = base_weekly_essentials * self.regional_multipliers.get(region, 1.0)
        yearly_essentials = adj_weekly_essentials * 52
        
        # 4. Tax (2024/25)
        taxable = max(0, salary - 12570)
        tax = (min(taxable, 37700) * 0.20) + (max(0, taxable - 37700) * 0.40)
        ni = max(0, (min(salary, 50270) - 12570) * 0.08)
        
        disposable = salary - tax - ni - yearly_essentials
        return {
            "Region": region,
            "Gross": round(salary, 2),
            "Essential_Costs": round(yearly_essentials, 2),
            "Disposable": round(max(0, disposable), 2)
        }

# Example: Same person, different regions
model = UKModelRegional('UK_Data.xlsx')
print(model.estimate_disposable(35000, 25, "England"))
print(model.estimate_disposable(35000, 55, "England"))
