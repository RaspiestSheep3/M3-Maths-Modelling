#Inputs
age = (input("Age : "))
ethnicity = input("Ethnicity : ")
gender = input("Gender (M/F) : ").upper()
maritalStatus = input("Marital Status : ")
disposableIncome = float(input("Disposable Income / £ : "))
educationLevel = input("Higher Education Level : ").upper()

#Calculation
"""Assumptions:
- women β = -0.13 compared to men
-  

"""
maleStatsDict = {
    "Never Married": {"b": 0.69, "beta": 0.06},
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

femaleStatsDict = {
    "Never Married": {"b": -0.16, "beta": -0.02},
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
baseB = 18.09

if(gender == "M"):
    b = baseB + (maleStatsDict[maritalStatus]["b"] + maleStatsDict[age]["b"] + maleStatsDict[ethnicity]["b"])
else:
    b = baseB + (femaleStatsDict[maritalStatus]["b"] + femaleStatsDict[age]["b"] + femaleStatsDict[ethnicity]["b"])

print(b)

#Output
print(f"Expected change : {"+" if expectedOut >= 0 else "-"}£{abs(expectedOut)} per year")




def predictFinancialRiskTolerance(
    isFemale=0, neverMarried=0, singleLivingWithSo=0, separated=0, divorced=0, widowed=0,
    personalIncome=0.0, education=0.0, financialKnowledge=0.0, householdSize=1, contToHhIncome=0.0,
    age25To44=0, age45To64=0, age65AndOlder=0,
    africanAmerican=0, hispanicLatino=0, otherRace=0,
    partTime=0, fullTime=0, retired=0
):
    """
    Predicts Financial Risk Tolerance using split gender models (Tables 4 & 5).
    """
    riskTolerance = 0.0
    
    if isFemale == 1:
        # --- TABLE 4: FEMALE MODEL ---
        riskTolerance += 18.00  # Female Constant
        
        # Marital Status
        riskTolerance += (-0.16 * neverMarried)
        riskTolerance += (0.22 * singleLivingWithSo)
        riskTolerance += (-3.44 * separated)
        riskTolerance += (-0.85 * divorced)
        riskTolerance += (0.34 * widowed)
        
        # Continuous Variables
        riskTolerance += (0.20 * personalIncome)
        riskTolerance += (0.29 * education)
        riskTolerance += (1.05 * financialKnowledge)
        riskTolerance += (0.34 * householdSize)
        riskTolerance += (0.01 * contToHhIncome)
        
        # Age
        riskTolerance += (-0.92 * age25To44)
        riskTolerance += (-1.36 * age45To64)
        riskTolerance += (-1.99 * age65AndOlder)
        
        # Race
        riskTolerance += (0.31 * africanAmerican)
        riskTolerance += (0.01 * hispanicLatino)
        riskTolerance += (-0.10 * otherRace)
        
        # Employment
        riskTolerance += (0.00 * partTime) 
        riskTolerance += (0.82 * fullTime)
        riskTolerance += (0.02 * retired)
        
    else:
        # --- TABLE 5: MALE MODEL ---
        riskTolerance += 18.09  # Male Constant
        
        # Marital Status
        riskTolerance += (0.69 * neverMarried)
        riskTolerance += (2.19 * singleLivingWithSo)
        riskTolerance += (1.52 * separated)
        riskTolerance += (1.65 * divorced)
        riskTolerance += (1.26 * widowed)
        
        # Continuous Variables
        riskTolerance += (0.05 * personalIncome)
        riskTolerance += (0.17 * education)
        riskTolerance += (1.34 * financialKnowledge)
        riskTolerance += (0.18 * householdSize)
        riskTolerance += (0.02 * contToHhIncome)
        
        # Age
        riskTolerance += (-0.18 * age25To44)
        riskTolerance += (-1.58 * age45To64)
        riskTolerance += (-1.44 * age65AndOlder)
        
        # Race
        riskTolerance += (-1.68 * africanAmerican)
        riskTolerance += (-1.22 * hispanicLatino)
        riskTolerance += (-0.64 * otherRace)
        
        # Employment
        riskTolerance += (1.57 * partTime)
        riskTolerance += (1.20 * fullTime)
        riskTolerance += (-0.49 * retired)
        
    return riskTolerance

# You can still pipe this directly into your calculateMaxAcceptableLoss function!