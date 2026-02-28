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
femaleBetaDict = {
    "Never Married " : -0.02,
    "Single Living w/ S.O." : 0.01,
    "Seperated" : -0.09,
    "Divorced" : -0.05,
    "Widowed" : 0.01,
    "25-44" : -0.09,
    "45-64" : -0.13,
    "65+" : -0.13,
    "Black" : 0.02,
    "Hispanic" : 0.00,
    "Other" : -0.01
}

maleBetaDict = {
    "Never Married " : 0.06,
    "Single Living w/ S.O." : 0.09,
    "Seperated" : 0.03,
    "Divorced" : 0.07,
    "Widowed" : 0.04,
    "25-44" : -0.02,
    "45-64" : -0.14,
    "65+" : -0.12,
    "Black" : -0.1,
    "Hispanic" : -0.06,
    "Other" : -0.04
}

expectedOut = 0

#Risk tolerance calculation


#Output
print(f"Expected change : {"+" if expectedOut >= 0 else "-"}£{abs(expectedOut)} per year")