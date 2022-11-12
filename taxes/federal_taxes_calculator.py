import json
import os

os.chdir("C:/Users/chuat/Desktop/projects/finance")

with open('config.json') as file:
    config = json.load(file)

gross_income = config["gross_income"]

#Taxable Income
def agi(deduction_type, filing_status):
    if deduction_type == "standard deduction":
        standard_deduction = config[filing_status]["standard deduction"]
        adjusted_gross_income = gross_income - standard_deduction
    elif deduction_type == "itemized deduction":
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

#Federal Income Tax Liability
def income_tax(taxable_income, filing_status):
    tax_rates = config[filing_status]["tax rate"]
    tax_brackets = config[filing_status]["tax bracket"]

    income_tax = 0
    for i in range(len(tax_rates)):
        current_rate = tax_rates[i]
        if i + 1 >= len(tax_brackets) or taxable_income < tax_brackets[i + 1]:
            income_tax+=current_rate * (taxable_income - tax_brackets[i])
            break
        else:
            income_tax+=current_rate * (tax_brackets[i + 1] - tax_brackets[i])
    
    return income_tax











