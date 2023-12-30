NUM_PEOPLE = 20  # Total number of people available
NUM_ROLES = 3  # Three roles: New Business Acquisition, Account Management, Support
NUM_MONTHS = 24  # Duration of 24 months
BASE_CSAT = 0.70  # Base CSAT score
CHURN_RATE = 0.10  # Churn rate
COMPOUNDING_MONTHS_MAX = 6  # Maximum number of months for compounding
CSAT_INCREASE = 0.01  # CSAT increase per Support person
CUSTOMER_LOAD = 25  # Maximum number of customers per Account Manager
RELATIVE_CHURN_DECREASE = 0.15  # Relative churn decrease per Support person
COMPOUNDING_PERCENTAGE = 0.20  # Percentage increase in revenue per month under Account Management

# A chromosome is a 2D array where each row represents a month and each column a role.
# The values in the array are the number of people in each role for that month.
import random
import numpy as np

# Create Initial Population
def create_initial_population(pop_size, NUM_PEOPLE, NUM_ROLES, NUM_MONTHS):
    population = []
    for _ in range(pop_size):
        chromosome = np.random.randint(0, NUM_PEOPLE + 1, (NUM_MONTHS, NUM_ROLES))
        # Ensure total number of people does not exceed the available number
        chromosome = np.array([np.round(row / sum(row) * NUM_PEOPLE).astype(int) if sum(row) != 0 else row for row in chromosome])
        population.append(chromosome)
    return np.array(population)

pop_size = 100  # Population size
population = create_initial_population(pop_size, NUM_PEOPLE, NUM_ROLES, NUM_MONTHS)

def fitness_function(state):
    customers = 1000  # Initial customers
    base_payment = 100  # Baseline fee per customer per month
    total_revenue = 0  # Total revenue over 24 months

    # Initialize all customers with 0 months under Account Management
    am_duration = [0] * customers  

    for month in state:
        N, A, S = month

        # Calculate new customers and update the customer base
        new_customers = N * 5
        new_customers = int(new_customers)
        customers += CUSTOMER_LOAD + new_customers  
        am_duration.extend([0] * new_customers)  

        # Support: Churn Rate Reduction
        csat_increase = BASE_CSAT + S * CSAT_INCREASE 
        churn_rate_reduction = csat_increase * RELATIVE_CHURN_DECREASE
        effective_churn_rate = max(CHURN_RATE - churn_rate_reduction, 0)
        churned_customers = int(customers * effective_churn_rate)
        customers -= churned_customers
        am_duration = am_duration[:-churned_customers] if churned_customers else am_duration

        # Account Management: Revenue Increase
        total_AM_customers = min(A * CUSTOMER_LOAD, customers)
        total_AM_customers = int(total_AM_customers)

        # Update AM duration for each customer
        for i in range(min(total_AM_customers, len(am_duration))):
            am_duration[i] = min(am_duration[i] + 1, COMPOUNDING_MONTHS_MAX)

        # Calculate revenue for the month
        am_revenue = sum([base_payment * (1 + COMPOUNDING_PERCENTAGE) ** duration for duration in am_duration[:total_AM_customers]])
        non_am_revenue = (customers - total_AM_customers) * base_payment
        monthly_revenue = am_revenue + non_am_revenue
        total_revenue += monthly_revenue

    return total_revenue

# tournament selection should work fine for our purposes
def selection(population, fitness_scores, tournament_size=3):
    selected = []
    pop_size = len(population)

    for _ in range(pop_size):
        # Randomly select tournament competitors
        competitors = np.random.choice(pop_size, tournament_size, replace=False)
        best_competitor_idx = competitors[np.argmax(fitness_scores[competitors])]
        selected.append(population[best_competitor_idx])

    return np.array(selected)

def crossover(parent1, parent2):
    num_months = len(parent1)  # Number of months
    offspring = np.empty_like(parent1)

    # For each month, randomly choose the allocation from one of the parents
    for i in range(num_months):
        if random.random() < 0.5:
            offspring[i] = parent1[i]
        else:
            offspring[i] = parent2[i]

        # Adjustment step: Ensure the total remains 20
        while np.sum(offspring[i]) != NUM_PEOPLE:
            deficit = NUM_PEOPLE - np.sum(offspring[i])
            roles_to_adjust = np.where(offspring[i] < (NUM_PEOPLE - deficit))[0]
            if roles_to_adjust.size > 0:
                selected_role = random.choice(roles_to_adjust)
                offspring[i][selected_role] += np.sign(deficit)
            else:
                break  # Break the loop if there are no roles to adjust

    return offspring


def mutation(chromosome, mutation_rate=0.05):
    num_people = NUM_PEOPLE  # Total number of people available
    num_roles = 3    # Number of roles

    for month in chromosome:
        if random.random() < mutation_rate:
            # Randomly select two different roles
            role1, role2 = random.sample(range(num_roles), 2)

            # Determine mutation amount (up to 3 people)
            mutation_amount = random.randint(1, 3)

            # If the mutation is not possible, decrease the mutation_amount until it is
            while month[role1] < mutation_amount or (month[role2] + mutation_amount) > num_people:
                mutation_amount -= 1

            # If a valid mutation_amount is found, perform the mutation
            if mutation_amount > 0:
                month[role1] -= mutation_amount
                month[role2] += mutation_amount

    return chromosome


# Main Genetic Algorithm Loop
num_generations = 100
for generation in range(num_generations):
    # Evaluate fitness
    fitness_scores = np.array([fitness_function(chromosome) for chromosome in population])
    # print(fitness_scores)

    # Selection
    selected = selection(population, fitness_scores)

    # Crossover and Mutation
    new_population = []
    while len(new_population) < len(population):
        parents = random.sample(list(selected), 2) # Select 2 random parents instead of every pair to limit size (otherwise this thing runs forever)
        offspring = crossover(parents[0], parents[1])
        offspring = mutation(offspring)
        new_population.append(offspring)

    population = np.array(new_population)

# Final solution
best_solution = population[np.argmax([fitness_function(chromosome) for chromosome in population])]
print("Optimal Staff Allocation [N, A, S]:" + str(best_solution))
print("Maximum Revenue: $" + str(round(fitness_function(best_solution), 2)))