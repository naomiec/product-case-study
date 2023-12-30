import random
import math

# Constants for the case study
TOTAL_AGENTS = 20  # Total number of agents available each month
MONTHS = 24  # Total months
NEW_BUSINESS_NEW_CUSTOMERS = 5  # New customers per New Business agent
ACCOUNT_MANAGEMENT_GROWTH = 0.20  # Revenue growth per Account Management agent
SUPPORT_CHURN_REDUCTION = 0.01  # Churn rate reduction per Support agent
CHURN_RATE = 0.10  # Base churn rate
ORGANIC_GROWTH = 25  # Organic customer growth per month
BASE_CSAT = 0.70  # Base CSAT score
COMPOUNDING_MONTHS_MAX = 6  # Maximum number of months for compounding

def generate_initial_state():
    # Specific allocation for each month: 7 New Business, 7 Account Management, 6 Support
    specific_allocation = [7, 7, 6]
    state = [specific_allocation for _ in range(MONTHS)]
    return state

def calculate_revenue(state):
    customers = 1000  # Initial customers
    base_payment = 100  # Baseline fee per customer per month
    total_revenue = 0  # Total revenue over 24 months

    # Initialize all customers with 0 months under Account Management
    am_duration = [0] * customers  

    for month in state:
        N, A, S = month

        # Calculate new customers and update the customer base
        new_customers = N * 5
        customers += ORGANIC_GROWTH + new_customers  
        am_duration.extend([0] * new_customers)  

        # Support: Churn Rate Reduction
        csat_increase = BASE_CSAT + S * 0.01  
        churn_rate_reduction = csat_increase * 0.15
        effective_churn_rate = max(CHURN_RATE - churn_rate_reduction, 0)
        churned_customers = int(customers * effective_churn_rate)
        customers -= churned_customers
        am_duration = am_duration[:-churned_customers] if churned_customers else am_duration

        # Account Management: Revenue Increase
        max_customers_per_AM = 25
        total_AM_customers = min(A * max_customers_per_AM, customers)

        # Update AM duration for each customer
        for i in range(min(total_AM_customers, len(am_duration))):
            am_duration[i] = min(am_duration[i] + 1, COMPOUNDING_MONTHS_MAX) 

        # Calculate revenue for the month
        am_revenue = sum([base_payment * (1 + 0.20) ** duration for duration in am_duration[:total_AM_customers]])
        non_am_revenue = (customers - total_AM_customers) * base_payment
        monthly_revenue = am_revenue + non_am_revenue
        total_revenue += monthly_revenue

    return total_revenue

def get_neighbor(current_state, current_month):
    new_state = [list(month) for month in current_state]  # Copy the current state
    total_agents = TOTAL_AGENTS  # Total number of agents available

    # Modify the allocation for the current month
    while True:
        new_allocation = (random.randint(0, total_agents), random.randint(0, total_agents), random.randint(0, total_agents))
        if sum(new_allocation) == total_agents: # Only accept allocations that use all agents
            new_state[current_month] = new_allocation
            break
    return new_state

def acceptance_probability(old_cost, new_cost, temperature):
    if new_cost > old_cost:
        return 1.0
    else:
        return math.exp((new_cost - old_cost) / temperature)

# the good stuff
def simulated_annealing(initial_state):
    current_state = initial_state
    current_cost = calculate_revenue(current_state)
    current_month = 0
    temperature = 10000 # this is how much total revenue seems to vary by, so that's what we'll use
    alpha = 0.9 # I chose a higher alpha value to explore the solution space more thoroughly
    for _ in range(10000):  # Number of iterations (high because we have time and it appears to max out here)
        neighbor = get_neighbor(current_state, current_month)
        neighbor_cost = calculate_revenue(neighbor)
        if acceptance_probability(current_cost, neighbor_cost, temperature) > random.random():
            current_state = neighbor
            current_cost = neighbor_cost
        current_month = (current_month + 1) % MONTHS
        temperature *= alpha
    return current_state, current_cost

initial_state = generate_initial_state()
final_state, final_revenue = simulated_annealing(initial_state)
print("Optimal Staff Allocation [N, A, S]:" + str(final_state))
print("Maximum Revenue: $" + str(round(final_revenue, 2)))

