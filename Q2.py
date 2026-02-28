#Inputs
age = int(input("Age : "))
ethnicity = input("Ethnicity : ")
location = input("Location : ")
gender = input("Gender (M/F) : ").upper()
married = True if input("Married (Y/N) : ").upper() == "Y" else False
disposableIncome = float(input("Disposable Income / £ : "))
educationLevel = input("Higher Education Level : ").upper()

#Chosen sports
sports = []
sport = None 
while(sport != ""):
    sport = input("Betted on sport (Blank to close): ").strip()
    if(sport != ""):
        sports.append(sport)

#Calculation
"""Assumptions:
- women β = -0.13 compared to men
-  

"""
male_stats_dict = {
    "Never Married ": {"b": 0.69, "beta": 0.06},
    "Single Living w/ S.O.": {"b": 2.19, "beta": 0.09},
    "Seperated": {"b": 1.52, "beta": 0.03},
    "Divorced": {"b": 1.65, "beta": 0.07},
    "Widowed": {"b": 1.26, "beta": 0.04},
    "25-44": {"b": -0.18, "beta": -0.02},
    "45-64": {"b": -1.58, "beta": -0.14},
    "65+": {"b": -1.44, "beta": -0.12},
    "Black": {"b": -1.68, "beta": -0.10},
    "Hispanic": {"b": -1.22, "beta": -0.06},
    "Other": {"b": -0.64, "beta": -0.04}
}

female_stats_dict = {
    "Never Married ": {"b": -0.16, "beta": -0.02},
    "Single Living w/ S.O.": {"b": 0.22, "beta": 0.01},
    "Seperated": {"b": -3.44, "beta": -0.09},
    "Divorced": {"b": -0.85, "beta": -0.05},
    "Widowed": {"b": 0.34, "beta": 0.01},
    "25-44": {"b": -0.92, "beta": -0.09},
    "45-64": {"b": -1.36, "beta": -0.13},
    "65+": {"b": -1.99, "beta": -0.13},
    "Black": {"b": 0.31, "beta": 0.02},
    "Hispanic": {"b": 0.01, "beta": 0.00},
    "Other": {"b": -0.10, "beta": -0.01}
}

expectedOut = 0

#Risk tolerance calculation


#Output
print(f"Expected change : {"+" if expectedOut >= 0 else "-"}£{abs(expectedOut)} per year")