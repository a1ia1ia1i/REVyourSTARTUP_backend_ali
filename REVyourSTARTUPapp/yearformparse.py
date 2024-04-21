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


# Build
def build_expenses_list(expenses_list):
    # Returns a list
    out_list = []
    for i in range(len(expenses_list)):
        expense = {
            "sourceName": expenses_list[i]['source_name'],
            "monthlyData": string_to_monthly(expenses_list[i]['monthly_data'])
        }
        out_list.append(expense)

    return out_list


def build_workers_list(workers_list):
    # Returns a list
    out_list = []
    for i in range(len(workers_list)):
        worker = {
            "description": workers_list[i]['description'],
            "monthlySalary": float(workers_list[i]['monthly_salary']),
            "monthlyData": string_to_monthly(workers_list[i]['monthly_data'])
        }
        out_list.append(worker)
    
    return out_list


def build_additional_revenue_json(additional_revenue_data):
    out_data = {
        "additionalRevenue": {
            "sourceNames": build_string_list(additional_revenue_data['source_names']),
            "sources": build_string_list(additional_revenue_data['sources']),
            "totalMonthly": string_to_monthly(additional_revenue_data['total_monthly'])
        }
    }

    return out_data


def build_banking_fees_json(banking_fees_data, expenses_list):
    out_data = {
        "bankingFees": {
            "expensesList": build_expenses_list(expenses_list),
            "totalMonthly": string_to_monthly(banking_fees_data['total_monthly'])
        }
    }

    return out_data


def build_cash_on_hand_json(cash_on_hand_data):
    out_data = {
        "cashOnHand": {
            "excludeDepreciation": cash_on_hand_data['exclude_depreciation'],
            "initialCashOnHand": float(cash_on_hand_data['initial_cash_on_hand']),
            "withDepreciation": string_to_monthly(cash_on_hand_data['with_depreciation']),
            "withoutDepreciation": string_to_monthly(cash_on_hand_data['without_depreciation'])
        }
    }

    return out_data


def build_customer_segments_json(segments_data):
    out_list = []
    out_data = {"customerSegments": out_list}

    for i in range(len(segments_data)):
        segment_dict = {
            "inputData": {
                "commission": float(segments_data[i]['segment']['commission']),
                "deliveredIn": segments_data[i]['segment']['delivered_in'],
                "deposit": float(segments_data[i]['segment']['deposit']),
                "extraMonths": segments_data[i]['segment']['extra_months'],
                "fixedFees": float(segments_data[i]['segment']['fixed_fees']),
            },
            "monthlyData": [],
            "name": segments_data[i]['segment']['name'],
            "numberToSell": segments_data[i]['segment']['number_to_sell'],
            "numbersToSellOriginal": segments_data[i]['segment']['numbers_to_sell_original'],
            "price": float(segments_data[i]['segment']['price']),
            "status": segments_data[i]['segment']['status'],
            "totalMonthlyData": []
        }
        total_monthly_data = string_to_monthly(segments_data[i]['segment']['total_monthly_data'])
        for j in range(len(total_monthly_data)):
            segment_dict["totalMonthlyData"].append({"amount": total_monthly_data[j]})

        for k in range(len(segments_data[i]['monthly_data'])):
            month = {
                "numbersSold": segments_data[i]['monthly_data'][k]['numbers_sold'],
                "deposit": float(segments_data[i]['monthly_data'][k]['deposit']),
                "original": float(segments_data[i]['monthly_data'][k]['original']),
                "extraFromPreviousMonths": float(segments_data[i]['monthly_data'][k]['extra_from_previous_months']),
                "commission": float(segments_data[i]['monthly_data'][k]['commission'])
            }
            segment_dict["monthlyData"].append(month)
        out_list.append(segment_dict)
    
    return out_data


def build_distributions_json(distributions_data):
    out_data = {
        "distributions": {
            "includeInvestments": distributions_data['include_investments'],
            "percentOfIncomeDistributed": float(distributions_data['percent_of_income_distributed']),
            "withInvestments": string_to_monthly(distributions_data['with_investments']),
            "withoutInvestments": string_to_monthly(distributions_data['without_investments'])
        }
    }

    return out_data


def build_fixed_assets_json(fixed_assets_data):
    out_data = {
        "fixedAssets": {
            "newAcquisitions": string_to_monthly(fixed_assets_data['new_acquisitions']),
            "depreciation": string_to_monthly(fixed_assets_data['depreciation']),
            "totalMonthly": string_to_monthly(fixed_assets_data['total_monthly'])
        }
    }

    return out_data


def build_founders_draw_json(founders_draw_data, founders_draw_pay_data):
    pay_list = []
    for i in range(len(founders_draw_pay_data)):
        pay_list.append(string_to_monthly(founders_draw_pay_data[i]['pay_array']))

    out_data = {
        "foundersDraw": {
            "numberOfFounders": founders_draw_data['number_of_founders'],
            "foundersShare": float(founders_draw_data['founders_share']),
            "foundersDrawPayArray": pay_list,
            "totalMonthly": string_to_monthly(founders_draw_data['total_monthly'])
        }
    }

    return out_data


def build_full_time_workers_json(full_time_workers_data, workers_list):
    out_data = {
        "fullTimeWorkers": {
            "workersList": build_workers_list(workers_list),
            "totalMonthly": string_to_monthly(full_time_workers_data['total_monthly'])
        }
    }

    return out_data


def build_funding_investment_json(funding_investment_data):
    out_data = {
        "fundingInvestment": {
            "sourceNames": build_string_list(funding_investment_data['source_names']),
            "sources": string_to_monthly(funding_investment_data['sources']),
            "totalMonthly": string_to_monthly(funding_investment_data['total_monthly'])
        }
    }

    return out_data


def build_legal_and_professional_services_json(legal_and_professional_services_data, expenses_list):
    out_data = {
        "legalAndProfessionalServices": {
            "expensesList": build_expenses_list(expenses_list),
            "totalMonthly": string_to_monthly(legal_and_professional_services_data['total_monthly'])
        }
    }

    return out_data


def build_marketing_expenses_json(marketing_expenses_data, expenses_list):
    out_data = {
        "marketingExpenses": {
            "expensesList": build_expenses_list(expenses_list),
            "totalMonthly": string_to_monthly(marketing_expenses_data['total_monthly'])
        }
    }

    return out_data


def build_office_general_business_json(office_general_business_data, expenses_list):
    out_data = {
        "officeGeneralBusiness": {
            "expensesList": build_expenses_list(expenses_list),
            "totalMonthly": string_to_monthly(office_general_business_data['total_monthly'])
        }
    }

    return out_data


def build_other_expenses_json(other_expenses_data, expenses_list):
    out_data = {
        "otherExpenses": {
            "expensesList": build_expenses_list(expenses_list),
            "totalMonthly": string_to_monthly(other_expenses_data['total_monthly'])
        }
    }

    return out_data


def build_part_time_workers_json(part_time_workers_data, workers_list):
    out_data = {
        "partTimeWorkers": {
            "workersList": build_workers_list(workers_list),
            "totalMonthly": string_to_monthly(part_time_workers_data['total_monthly'])
        }
    }

    return out_data


def build_pay_roll_taxes_and_benefits_json(pay_roll_taxes_and_benefits_data, pay_roll_list):
    pay_list = []
    for i in range(len(pay_roll_list)):
        data = {
            "sourceName": pay_roll_list[i]['source_name'],
            "value": float(pay_roll_list[i]['value']),
            "monthlyData": string_to_monthly(pay_roll_list[i]['monthly_data'])
        }
        pay_list.append(data)

    out_data = {
        "payRollTaxesAndBenefits": {
            "payrollList": pay_list,
            "totalMonthly": string_to_monthly(pay_roll_taxes_and_benefits_data['total_monthly'])
        }
    }

    return out_data


def build_production_related_json(production_related_data_entries):
    out_list = []
    out_data = {
        "productionRelated": out_list
    }
    
    for i in range(len(production_related_data_entries)):
        data = {
            "name": production_related_data_entries[i]['production_related']['name'],
            "expensesList": build_expenses_list(production_related_data_entries[i]['expenses_list']),
            "totalMonthly": string_to_monthly(production_related_data_entries[i]['production_related']['total_monthly'])
        }
        out_list.append(data)

    return out_data


def build_property_related_json(property_related_data, expenses_list):
    out_data = {
        "propertyRelated": {
            "expensesList": build_expenses_list(expenses_list),
            "totalMonthly": string_to_monthly(property_related_data['total_monthly'])
        }
    }

    return out_data


def build_return_reworks_json(expenses_list):
    expenses_list = build_expenses_list(expenses_list)
    out_data = {
        "returnReworks": expenses_list
    }

    return out_data


def build_salaried_workers_json(salaried_workers_data, workers_list):
    out_data = {
        "salariedWorkers": {
            "workersList": build_workers_list(workers_list),
            "totalMonthly": string_to_monthly(salaried_workers_data['total_monthly'])
        }
    }

    return out_data


def build_travel_vehicle_related_json(travel_vehicle_related_data, expenses_list):
    out_data = {
        "travelVehicleRelated": {
            "expensesList": build_expenses_list(expenses_list),
            "totalMonthly": string_to_monthly(travel_vehicle_related_data['total_monthly'])
        }
    }

    return out_data


def build_workers_head_count_json(workers_head_count_data):
    out_data = {
        "workersHeadCount": {
            "foundersHeadCount": string_to_monthly(workers_head_count_data['founders_head_count'], True),
            "salariedHeadCount": string_to_monthly(workers_head_count_data['salaried_head_count'], True),
            "fullTimeHeadCount": string_to_monthly(workers_head_count_data['full_time_head_count'], True),
            "partTimeHeadCount": string_to_monthly(workers_head_count_data['part_time_head_count'], True),
            "totalMonthly": string_to_monthly(workers_head_count_data['total_monthly'], True)
        }
    }

    return out_data
