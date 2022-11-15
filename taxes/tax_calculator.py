import json
import os

os.chdir("C:/Users/chuat/Documents/GitHub/financial_decisions/taxes")

with open('config.json') as file:
    config = json.load(file)

#deductions
monthly_insurance = sum(config["insurance"].values())
fica_tax = sum(config["fica"].values())
state_tax = config["state tax"]["IL"]

class Finance:
    def __init__(self, gross_income, filing_status, deduction_type, retirement, periods):
        self.filing_status = filing_status
        self.deduction_type = deduction_type
        self.gross_income = gross_income
        self.retirement = retirement
        self.periods = periods
        
    def agi(self):
        if self.deduction_type == "standard deduction":
            standard_deduction = config[self.filing_status]["standard deduction"]
            all_deductions = standard_deduction + (12 * monthly_insurance)
            adjusted_gross_income = self.gross_income - all_deductions
        elif self.deduction_type == "itemized deduction":
            while True:
                try:
                    itemized_deduction = int(input("Enter amount of itemized deductions: "))
                except ValueError:
                    print("Please enter a number (no commas).")
                    continue
                else:
                    break
            adjusted_gross_income = self.gross_income - itemized_deduction
            
        return adjusted_gross_income - (self.retirement * self.periods)

    def income_tax(self):
        taxable_income = self.agi()
        tax_rates = config[self.filing_status]["tax rate"]
        tax_brackets = config[self.filing_status]["tax bracket"]

        income_tax = 0
        for i in range(len(tax_rates)):
            current_rate = tax_rates[i]
            if i + 1 >= len(tax_brackets) or taxable_income < tax_brackets[i + 1]:
                income_tax+=current_rate * (taxable_income - tax_brackets[i])
                break
            else:
                income_tax+=current_rate * (tax_brackets[i + 1] - tax_brackets[i])
    
        return income_tax

    def take_home_pay(self):
        minus_state = (self.gross_income - (12 * monthly_insurance)) * state_tax
        minus_fica = (self.gross_income - (12 * monthly_insurance)) * fica_tax

        take_home = self.gross_income - self.income_tax() - minus_state - minus_fica

        return round(take_home / 12, 2)

    def summary(self):
        monthly_state_tax = ((self.gross_income - (12 * monthly_insurance)) * state_tax) / 12
        print("Annual Gross Income: ", self.gross_income)
        print("Taxable Income: ", self.agi())
        print("Take-home pay per month: ", self.take_home_pay())
        print("State tax per month: ", round(monthly_state_tax, 2))
        print("Federal Income Tax Liability: " + str(round(self.income_tax(), 2)) +  \
        " (" + str(round(self.income_tax() / 12,2)), " per month)")

my_income = config["annual gross income"]
contribution = config["monthly retirement contribution"]

ted = Finance(my_income, "single filer", "standard deduction", retirement = 0, periods = 0)
ted.summary()

ted1 = Finance(my_income, "single filer", "standard deduction", retirement = contribution, periods = 6)
ted1.summary()
