import locale


def statement(invoice: dict, plays: dict):
    total_amount = 0
    volume_credits = 0
    result = f"Statement for {invoice['customer']}\n"

    def play_for(performance):
        return plays[performance["playID"]]

    def amount_for(performance):
        result = 0

        match play_for(performance)["type"]:
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
                raise Exception(f"unknown type: ${play_for(performance)['type']}")
        return result

    def volume_credits_for(performance):
        volume_credits = 0
        volume_credits += max(performance["audience"] - 30, 0)
        if "comedy" == play_for(performance)["type"]:
            volume_credits += performance["audience"] // 5
        return volume_credits

    def format(amount):
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
        return locale.currency(amount, grouping=True)

    for perf in invoice["performances"]:
        volume_credits += volume_credits_for(perf)

        # print line for this order
        result += f"  {play_for(perf)['name']}: {format(amount_for(perf)/100)} ({perf['audience']} seats)\n"
        total_amount += amount_for(perf)

    result += f"Amount owed is {format(total_amount/100)}\n"
    result += f"You earned {volume_credits} credits\n"
    return result
