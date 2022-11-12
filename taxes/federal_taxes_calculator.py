import json
import os

os.chdir("C:/Users/chuat/Documents/GitHub/financial_decisions/taxes")

with open('config.json') as file:
    config = json.load(file)
        
gross_income = config["gross income"]

class Finance:
    def __init__(self, filing_status, deduction_type):
        self.filing_status = filing_status
        self.deduction_type = deduction_type

    #taxable income
    def agi(self):
        if self.deduction_type == "standard deduction":
            standard_deduction = config[self.filing_status]["standard deduction"]
            adjusted_gross_income = gross_income - standard_deduction
        elif self.deduction_type == "itemized deduction":
            while True:
                try:
                    itemized_deduction = int(input("Enter amount of itemized deductions: "))
                except ValueError:
                    print("Please enter a number (no commas).")
                    continue
                else:
                    break
            adjusted_gross_income = gross_income - itemized_deduction
            
        return adjusted_gross_income

    #federal income tax liability
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

ted = Finance("single filer", "standard deduction")

ted.agi()
ted.income_tax()