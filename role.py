# New Business Acquisituion Algorithm ++++++++++++++++++++++++++++++++++++++
def calculate_revenue_new_business(staff_nb, new_customers_per_staff, customer_fee):
    total_new_customers = staff_nb * new_customers_per_staff
    revenue_new_business = total_new_customers * customer_fee
    return revenue_new_business

rev_nb = calculate_revenue_new_business(1, 5, 100)
print("Revenue from NBA Staff: ", rev_nb) #comes out to 500


# Account Management Algorithm ++++++++++++++++++++++++++++++++++++++
def calculate_revenue_account_management(staff_am, managed_customers_per_staff, revenue_increase_rate, existing_customers, customer_fee, months):
    total_managed_customers = min(staff_am * managed_customers_per_staff, existing_customers)
    total_revenue_increase = 0

    for month in range(1, months + 1):  
        # Limit the compounding to a maximum of 6 months
        compound_month = min(month, 6)
        monthly_increase = (customer_fee * total_managed_customers) * (1 + revenue_increase_rate) ** compound_month
        total_revenue_increase += monthly_increase

    initial_revenue = customer_fee * total_managed_customers * months
    additional_revenue = total_revenue_increase - initial_revenue
    return additional_revenue

rev_am = calculate_revenue_account_management(1, 25, 0.2, 1000, 100, 24)
print("Revenue from AM Staff: ", rev_am) # comes out to 104159


# Support Algorithm ++++++++++++++++++++++++++++++++++++++++++++++++++
def calculate_revenue_support(staff_support, csat_increase_per_staff, churn_reduction_per_csat_point, initial_churn_rate, initial_customers, customer_fee, minimum_churn_rate):
    total_csat_increase = staff_support * csat_increase_per_staff
    new_churn_rate = max(initial_churn_rate * (1 - churn_reduction_per_csat_point * total_csat_increase), minimum_churn_rate)
    
    reduced_churn = (initial_churn_rate - new_churn_rate) * initial_customers
    revenue_support = reduced_churn * customer_fee
    return revenue_support

rev_support = calculate_revenue_support(1, 0.1, 0.15, 0.1, 1000, 100, 0.01)
print("Revenue from Support Staff: ", rev_support) # comes out to ~150


total_rev = rev_nb + rev_am + rev_support
print("Total Revenue: ", total_rev)