from copy import copy
from urllib.parse import parse_qs


def create_statement_data(invoice, plays):
    def play_for(performance):
        return plays[performance["playID"]]

    def total_volume_credits(data):
        return sum(p["volume_credits"] for p in data["performances"])

    def total_amount(data):
        return sum(p["amount"] for p in data["performances"])

    def enrich_performance(performance):
        calculator = create_PerformanceCalculator(performance, play_for(performance))
        result = copy(performance)
        result["play"] = calculator.play
        result["amount"] = calculator.amount
        result["volume_credits"] = calculator.volume_credits
        return result

    statement_data = {}
    statement_data["customer"] = invoice["customer"]
    statement_data["performances"] = [
        enrich_performance(p) for p in invoice["performances"]
    ]
    statement_data["total_volume_credits"] = total_volume_credits(statement_data)
    statement_data["total_amount"] = total_amount(statement_data)
    return statement_data


class PerformanceCalculator:
    def __init__(self, performance, play) -> None:
        self.performance = performance
        self.play = play

    @property
    def amount(self):
        raise Exception("Subclass responsibility")

    @property
    def volume_credits(self):
        result = 0
        result += max(self.performance["audience"] - 30, 0)
        if "comedy" == self.play["type"]:
            result += self.performance["audience"] // 5
        return result


class ComedyCalculator(PerformanceCalculator):
    @property
    def amount(self):
        result = 30000
        if self.performance["audience"] > 20:
            result += 10000 + 500 * (self.performance["audience"] - 20)
        result += 300 * self.performance["audience"]
        return result


class TragedyCalculator(PerformanceCalculator):
    @property
    def amount(self):
        result = 40000
        if self.performance["audience"] > 30:
            result += 1000 * (self.performance["audience"] - 30)
        return result


def create_PerformanceCalculator(performance, play) -> PerformanceCalculator:
    match play["type"]:
        case "comedy":
            return ComedyCalculator(performance, play)
        case "tragedy":
            return TragedyCalculator(performance, play)
        case _:
            raise Exception(f"Unknown performance type: {play['type']}")
