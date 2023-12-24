import numpy as np
from scipy.optimize import linprog

# Coefficients of the objective function (average revenue per staff for each role)
c = np.array([-500, -104159, -150])  # Negative values for maximization

# Coefficients for inequality constraints (Total staff constraint)
A = np.array([[1, 1, 1]])
b = np.array([20])

# Bounds for each variable (number of staff in each role)
x_bounds = (0, 20)  
y_bounds = (0, 20) 
z_bounds = (0, 20) 

# Use linprog to solve the linear programming problem
res = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds, z_bounds], method='highs')

# Display the results
if res.success:
    optimal_staff_nb = res.x[0]
    optimal_staff_am = res.x[1]
    optimal_staff_support = res.x[2]
    max_revenue = -res.fun  # Convert to positive as we initially took negative for maximization
    print(f"Optimal Staff Allocation:")
    print(f"  New Business Acquisition: {optimal_staff_nb:.0f}")
    print(f"  Account Management: {optimal_staff_am:.0f}")
    print(f"  Support: {optimal_staff_support:.0f}")
    print(f"Maximum Revenue: ${max_revenue:.2f}")
else:
    print("Uh oh, something went wrong...")

