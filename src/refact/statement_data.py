from copy import copy


def create_statement_data(invoice, plays):
    def play_for(performance):
        return plays[performance["playID"]]

    def amount_for(performance):
        result = 0

        match performance["play"]["type"]:
            case "tragedy":
                result = 40000
                if performance["audience"] > 30:
                    result += 1000 * (performance["audience"] - 30)
            case "comedy":
                result = 30000
                if performance["audience"] > 20:
                    result += 10000 + 500 * (performance["audience"] - 20)
                result += 300 * performance["audience"]
            case _:
                raise Exception(f"unknown type: ${performance['play']['type']}")
        return result

    def volume_credits_for(performance):
        result = 0
        result += max(performance["audience"] - 30, 0)
        if "comedy" == performance["play"]["type"]:
            result += performance["audience"] // 5
        return result

    def total_volume_credits(data):
        return sum(p["volume_credits"] for p in data["performances"])

    def total_amount(data):
        return sum(p["amount"] for p in data["performances"])

    def enrich_performance(performance):
        calculator = PerformanceCalculator(performance)
        result = copy(performance)
        result["play"] = play_for(result)
        result["amount"] = amount_for(result)
        result["volume_credits"] = volume_credits_for(result)
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
    def __init__(self, performance) -> None:
        self.performance = performance
