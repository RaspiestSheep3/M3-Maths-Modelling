#Inputs
age = int(input("Age : "))
gender = input("Gender (M/F) : ").upper()
disposableIncome = float(input("Disposable Income / £ : "))
educationLevel = input("Higher Education Level : ").upper()
averageBetsPerWeek = float(input("Average number of bets per week : "))
riskTolerance = float(input("Risk tolerance -5 to 5 (-5 =very low, 5 = very high)"))
averageValuePerBet = float(input("Average value per best / £ : "))

#Chosen sports
sports = []
sport = None 
while(sport != ""):
    sport = input("Betted on sport (Blank to close): ").strip()
    if(sport != ""):
        sports.append(sport)
    


#Calculation
"""Assumptions:
- We can assume that someone with a higher risk tolerance will be more likely to focus on high-payout low-probability bets
"""

expectedOut = 0

#Risk tolerance calculation
riskToleranceProbabilityCoefficient = 0.05
riskToleranceValueCoefficient = -1
expectedOut = (0.5 - riskToleranceProbabilityCoefficient * riskTolerance) * (averageValuePerBet + riskToleranceValueCoefficient * riskTolerance) * averageBetsPerWeek - (1-(0.5 - riskToleranceProbabilityCoefficient * riskTolerance)) * (averageValuePerBet + riskToleranceValueCoefficient * riskTolerance) * averageBetsPerWeek * (365/7)

#Output
print(f"Expected change : {"+" if expectedOut >= 0 else "-"}£{abs(expectedOut)} per year")