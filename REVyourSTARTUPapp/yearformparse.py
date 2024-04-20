# File for parsing and building the year_forms json

# Commonly called utility functions
def monthly_to_string(number_list):
    out_string = ""

    for i in range(len(number_list)):
        if i == len(number_list) - 1:
            out_string += str(number_list[i])
            break
        out_string += str(number_list[i]) + ","
    
    return out_string


def string_to_monthly(in_string, as_int=False):
    num_list = []

    string_list = in_string.split(",")

    if as_int:
        for i in string_list:
            num_list.append(int(i))
    else:
        for i in string_list:
            num_list.append(float(i))

    return num_list


def condense_string_list(string_list):
    out_string = ""

    for i in range(len(string_list)):
        if i == len(string_list) - 1:
            out_string += string_list[i]
            break
        out_string += string_list[i] + "~"

    return out_string


def build_string_list(in_string):
    string_list = in_string.split("~")

    return string_list


# Flatten and Build Functions

# Flatten
def flatten_expenses_list(tag_name, expenses_list_data):
    expenses_list = []
    for i in range(len(expenses_list_data)):
        source_name = expenses_list_data[i]["sourceName"]
        monthly_data = monthly_to_string(expenses_list_data[i]["monthlyData"])
        expenses_list.append({"tag_name": tag_name, "source_name": source_name, "monthly_data": monthly_data})


    return expenses_list


def flatten_additional_revenue_data(additional_revenue_data):
    total_monthly = monthly_to_string(additional_revenue_data["totalMonthly"])
    source_names = condense_string_list(additional_revenue_data["sourceNames"])
    sources = condense_string_list(additional_revenue_data["sources"])
    out_data = {
        "source_names" : source_names,
        "sources": sources,
        "total_monthly": total_monthly
    }

    return out_data


def flatten_banking_fees_data(banking_fees_data):
    total_monthly = monthly_to_string(banking_fees_data["totalMonthly"])
    expenses_list = flatten_expenses_list("banking_fees", banking_fees_data["expensesList"])
    out_data = {
        "expenses_list": expenses_list,
        "total_monthly": total_monthly
    }

    return out_data


def flatten_cash_on_hand_data(cash_on_hand_data):
    with_depreciation = monthly_to_string(cash_on_hand_data["withDepreciation"])
    without_depreciation = monthly_to_string(cash_on_hand_data["withoutDepreciation"])
    out_data = {
        "exclude_depreciation": cash_on_hand_data["excludeDepreciation"],
        "initial_cash_on_hand": cash_on_hand_data["initialCashOnHand"],
        "with_depreciation": with_depreciation,
        "without_depreciation": without_depreciation
    }

    return out_data

def flatten_monthly_data(monthly_data):
    out_data = {
        "numbers_sold": monthly_data["NumbersSold"],
        "deposit": monthly_data["Deposit"],
        "original": monthly_data["Original"],
        "extra_from_previous_months": monthly_data["ExtraFromPreviousMonths"],
        "commission": monthly_data["commission"]
    }

    return out_data


def flatten_customer_segments_data(customer_segments_data):
    out_list = []
    for i in range(len(customer_segments_data)):
        segment = {}
        # "inputData"
        segment["commission"] = customer_segments_data[i]["inputData"]["commission"]
        segment["delivered_in"] = customer_segments_data[i]["inputData"]["deliveredIn"]
        segment["deposit"] = customer_segments_data[i]["inputData"]["deposit"]
        segment["extra_months"] = customer_segments_data[i]["inputData"]["extraMonths"]
        segment["fixed_fees"] = customer_segments_data[i]["inputData"]["fixedFees"]
        segment["monthly_data"] = []
        for j in range(len(customer_segments_data[i]["monthlyData"])):
            segment["monthly_data"].append(flatten_monthly_data(customer_segments_data[i]["monthlyData"][j]))

        segment["name"] = customer_segments_data[i]["name"]
        segment["number_to_sell"] = customer_segments_data[i]["numberToSell"]
        segment["numbers_to_sell_original"] = customer_segments_data[i]["numbersToSellOriginal"]
        segment["price"] = customer_segments_data[i]["price"]
        segment["status"] = customer_segments_data[i]["status"]
        total_monthly_data_list = []
        for k in range(len(customer_segments_data[i]["totalMonthlyData"])):
            total_monthly_data_list.append(customer_segments_data[i]["totalMonthlyData"][k]["amount"])
        segment["total_monthly_data"] = monthly_to_string(total_monthly_data_list)

        out_list.append(segment)
    
    return out_list


def flatten_distributions_data(distributions_data):
    with_investments = monthly_to_string(distributions_data["withInvestments"])
    without_investments = monthly_to_string(distributions_data["withoutInvestments"])
    out_data = {
        "include_investments": distributions_data["includeInvestments"],
        "percent_of_income_distributed": distributions_data["percentOfIncomeDistributed"],
        "with_investments": with_investments,
        "without_investments": without_investments
    }

    return out_data


def flatten_fixed_assets_data(fixed_assets_data):
    out_data = {
        "new_acquisitions": monthly_to_string(fixed_assets_data["newAcquisitions"]),
        "depreciation": monthly_to_string(fixed_assets_data["depreciation"]),
        "total_monthly": monthly_to_string(fixed_assets_data["totalMonthly"])
    }

    return out_data


def flatten_founders_draw_data(founders_draw_data):
    pay_array = []
    for i in range(len(founders_draw_data["foundersDrawPayArray"])):
        pay_list = monthly_to_string(founders_draw_data["foundersDrawPayArray"][i])
        pay_array.append(pay_list)
    
    out_data = {
        "number_of_founders": founders_draw_data["numberOfFounders"],
        "founders_share": founders_draw_data["foundersShare"],
        "founders_draw_pay_array": pay_array,
        "total_monthly": monthly_to_string(founders_draw_data["totalMonthly"])
    }

    return out_data


def flatten_workers_list(tag_name, workers_list_data):
    workers_list = []
    for i in range(len(workers_list_data)):
        data = {
            "tag_name": tag_name,
            "description": workers_list_data[i]["description"],
            "monthly_salary": workers_list_data[i]["monthlySalary"],
            "monthly_data": monthly_to_string(workers_list_data[i]["monthlyData"])
        }
        workers_list.append(data)

    return workers_list


def flatten_full_time_workers_data(full_time_workers_data):
    out_data = {
        "workers_list": flatten_workers_list("full_time_workers", full_time_workers_data["workersList"]),
        "total_monthly": monthly_to_string(full_time_workers_data["totalMonthly"])
    }

    return out_data


def flatten_part_time_workers_data(part_time_workers_data):
    out_data = {
        "workers_list": flatten_workers_list("part_time_workers", part_time_workers_data["workersList"]),
        "total_monthly": monthly_to_string(part_time_workers_data["totalMonthly"])
    }

    return out_data


def flatten_salaried_workers_data(salaried_workers_data):
    out_data = {
        "workers_list": flatten_workers_list("salaried_workers", salaried_workers_data["workersList"]),
        "total_monthly": monthly_to_string(salaried_workers_data["totalMonthly"])
    }

    return out_data


def flatten_funding_investment_data(funding_investment_data):
    out_data = {
        "source_names": condense_string_list(funding_investment_data["sourceNames"]),
        "sources": monthly_to_string(funding_investment_data["sources"]),
        "total_monthly": monthly_to_string(funding_investment_data["totalMonthly"])
    }

    return out_data


def flatten_legal_and_profesisonal_services_data(legal_and_professional_services_data):
    total_monthly = monthly_to_string(legal_and_professional_services_data["totalMonthly"])
    expenses_list = flatten_expenses_list("legal_and_professional_services", legal_and_professional_services_data["expensesList"])
    out_data = {
        "expenses_list": expenses_list,
        "total_monthly": total_monthly
    }

    return out_data


def flatten_marketing_expenses_data(marketing_expenses_data):
    total_monthly = monthly_to_string(marketing_expenses_data["totalMonthly"])
    expenses_list = flatten_expenses_list("marketing_expenses", marketing_expenses_data["expensesList"])
    out_data = {
        "expenses_list": expenses_list,
        "total_monthly": total_monthly
    }

    return out_data

def flatten_office_general_business_data(office_general_business_data):
    total_monthly = monthly_to_string(office_general_business_data["totalMonthly"])
    expenses_list = flatten_expenses_list("office_general_business", office_general_business_data["expensesList"])
    out_data = {
        "expenses_list": expenses_list,
        "total_monthly": total_monthly
    }

    return out_data


def flatten_other_expenses_data(other_expenses_data):
    total_monthly = monthly_to_string(other_expenses_data["totalMonthly"])
    expenses_list = flatten_expenses_list("other_expenses", other_expenses_data["expensesList"])
    out_data = {
        "expenses_list": expenses_list,
        "total_monthly": total_monthly
    }

    return out_data


def flatten_property_related_data(property_related_data):
    total_monthly = monthly_to_string(property_related_data["totalMonthly"])
    expenses_list = flatten_expenses_list("property_related", property_related_data["expensesList"])
    out_data = {
        "expenses_list": expenses_list,
        "total_monthly": total_monthly
    }

    return out_data


def flatten_return_reworks_data(return_reworks_data):
    expenses_list = flatten_expenses_list("return_reworks", return_reworks_data)

    return expenses_list


def flatten_travel_vehicle_related_data(travel_vehicle_related_data):
    total_monthly = monthly_to_string(travel_vehicle_related_data["totalMonthly"])
    expenses_list = flatten_expenses_list("travel_vehicle_related", travel_vehicle_related_data["expensesList"])
    out_data = {
        "expenses_list": expenses_list,
        "total_monthly": total_monthly
    }

    return out_data


def flatten_pay_roll_taxes_and_benefits_data(pay_roll_taxes_and_benefits_data):
    pay_roll_list = []
    for i in range(len(pay_roll_taxes_and_benefits_data["payrollList"])):
        data = {
            "source_name": pay_roll_taxes_and_benefits_data["payrollList"][i]["sourceName"],
            "value": pay_roll_taxes_and_benefits_data["payrollList"][i]["value"],
            "monthly_data": monthly_to_string(pay_roll_taxes_and_benefits_data["payrollList"][i]["monthlyData"])
        }
        pay_roll_list.append(data)

    out_data = {
        "pay_roll_list": pay_roll_list,
        "total_monthly": monthly_to_string(pay_roll_taxes_and_benefits_data["totalMonthly"])
    }

    return out_data


def flatten_production_related_data(production_related_data):
    production_list = []
    for i in range(len(production_related_data)):
        expenses_list = []
        for j in range(len(production_related_data[i]["expensesList"])):
            expense_data = {
                "source_name": production_related_data[i]["expensesList"][j]["sourceName"],
                "monthly_data": monthly_to_string(production_related_data[i]["expensesList"][j]["monthlyData"])
            }
            expenses_list.append(expense_data)
        data = {
            "name": production_related_data[i]["name"],
            "expenses_list": expenses_list,
            "total_monthly": monthly_to_string(production_related_data[i]["totalMonthly"])
        }
        production_list.append(data)

    return production_list


def flatten_workers_head_count_data(workers_head_count_data):
    out_data = {
        "founders_head_count": monthly_to_string(workers_head_count_data["foundersHeadCount"]),
        "salaried_head_count": monthly_to_string(workers_head_count_data["salariedHeadCount"]),
        "full_time_head_count": monthly_to_string(workers_head_count_data["fullTimeHeadCount"]),
        "part_time_head_count": monthly_to_string(workers_head_count_data["partTimeHeadCount"]),
        "total_monthly": monthly_to_string(workers_head_count_data["totalMonthly"])
    }

    return out_data



