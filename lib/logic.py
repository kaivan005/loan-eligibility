from dataclasses import dataclass
from typing import Dict


def calculate_emi(principal: float, annual_rate: float, years: float) -> Dict[str, float]:
    if principal <= 0 or annual_rate <= 0 or years <= 0:
        return {
            "monthlyPayment": 0.0,
            "totalPayment": 0.0,
            "totalInterest": 0.0,
        }
    monthlyRate = annual_rate / 100.0 / 12.0
    n = int(years * 12)
    monthlyPayment = principal * (monthlyRate * (1 + monthlyRate) ** n) / ((1 + monthlyRate) ** n - 1)
    totalPayment = monthlyPayment * n
    totalInterest = totalPayment - principal
    return {
        "monthlyPayment": monthlyPayment,
        "totalPayment": totalPayment,
        "totalInterest": totalInterest,
    }
