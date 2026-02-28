#Inputs
age = (input("Age : "))
ethnicity = input("Ethnicity : ")
gender = input("Gender (M/F) : ").upper()
maritalStatus = input("Marital Status : ")
disposableIncome = float(input("Disposable Income / £ : "))

#Calculation
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

def PredictRiskTolerance():
    if(gender == "M"):
        r = 18.09
        r += maleStatsDict[age]["b"]
        r += maleStatsDict[ethnicity]["b"]
        r += maleStatsDict[maritalStatus]["b"]

        #r = -1 + 2 * (r - 15.52) / (19.46 - 15.52)

    else:
        r = 18.35
        r += femaleStatsDict[age]["b"]
        r += femaleStatsDict[ethnicity]["b"]
        r += femaleStatsDict[maritalStatus]["b"]

        #r = -1 + 2 * (r - 12.82) / (17.96 - 12.82)

    return r


#Frequency equation
riskTolerance = PredictRiskTolerance()

epsilon = 0.05

y = pow((disposableIncome ** 2 * riskTolerance **2)/(1-epsilon**2),0.25)

Ex = -y * (0.5 + epsilon/2) + y*(0.5 - epsilon/2)

betPerYearCoefficient = 0.3
numBetsPerYear = betPerYearCoefficient*abs(Ex)

print(f"r : {riskTolerance}")
print(f"Y : {y}")
print(f"E(x) : {Ex}")
print(f"No : {numBetsPerYear}")
print(f"Expected Loss : {Ex*numBetsPerYear}")