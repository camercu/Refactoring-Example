import locale


def statement(invoice: dict, plays: dict):
    total_amount = 0
    volume_credits = 0
    result = f"Statement for {invoice['customer']}\n"

    def format(amount):
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
        return locale.currency(amount, grouping=True)

    for perf in invoice["performances"]:
        play = plays[perf["playID"]]
        this_amount = amount_for(perf, play)

        # add volume credits
        volume_credits += max(perf["audience"] - 30, 0)
        # add extra credit for every ten comedy attendees
        if "comedy" == play["type"]:
            volume_credits += perf["audience"] // 5

        # print line for this order
        result += (
            f"  {play['name']}: {format(this_amount/100)} ({perf['audience']} seats)\n"
        )
        total_amount += this_amount

    result += f"Amount owed is {format(total_amount/100)}\n"
    result += f"You earned {volume_credits} credits\n"
    return result


def amount_for(perf, play):
    result = 0

    match play["type"]:
        case "tragedy":
            result = 40000
            if perf["audience"] > 30:
                result += 1000 * (perf["audience"] - 30)
        case "comedy":
            result = 30000
            if perf["audience"] > 20:
                result += 10000 + 500 * (perf["audience"] - 20)
            result += 300 * perf["audience"]
        case _:
            raise Exception(f"unknown type: ${play['type']}")
    return result
