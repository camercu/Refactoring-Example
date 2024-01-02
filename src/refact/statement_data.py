from copy import copy


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


def create_PerformanceCalculator(performance, play):
    return PerformanceCalculator(performance, play)


class PerformanceCalculator:
    def __init__(self, performance, play) -> None:
        self.performance = performance
        self.play = play

    @property
    def amount(self):
        result = 0

        match self.play["type"]:
            case "tragedy":
                result = 40000
                if self.performance["audience"] > 30:
                    result += 1000 * (self.performance["audience"] - 30)
            case "comedy":
                result = 30000
                if self.performance["audience"] > 20:
                    result += 10000 + 500 * (self.performance["audience"] - 20)
                result += 300 * self.performance["audience"]
            case _:
                raise Exception(f"unknown type: ${self.play['type']}")
        return result

    @property
    def volume_credits(self):
        result = 0
        result += max(self.performance["audience"] - 30, 0)
        if "comedy" == self.play["type"]:
            result += self.performance["audience"] // 5
        return result
