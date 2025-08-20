# ============================================
# PACKAGE MANAGEMENT
# ============================================
from ortools.linear_solver import pywraplp

# ============================================
# DECLARE CONSTANTS
# ============================================
a_c1_req = 6
a_c2_req = 8
b_c1_req = 10
b_c2_req = 5

c1_cost = 0.4
c2_cost = 1.2

c1_capacity_cost = 150
c2_capacity_cost = 180

c1_current_capacity = 40
c2_current_capacity = 20

capacity_limit = 120

c1_batch = 60
c2_batch = 90

a_demand = 500
b_demand = 200

a_price_1 = 70
b_price_1 = 50
prob_1 = 0.3

a_price_2 = 50
b_price_2 = 60
prob_2 = 0.4

a_price_3 = 30
b_price_3 = 70
prob_3 = 0.3

a_revenue_1 = a_price_1 - a_c1_req * c1_cost - a_c2_req * c2_cost
b_revenue_1 = b_price_1 - b_c1_req * c1_cost - b_c2_req * c2_cost

a_revenue_2 = a_price_2 - a_c1_req * c1_cost - a_c2_req * c2_cost
b_revenue_2 = b_price_2 - b_c1_req * c1_cost - b_c2_req * c2_cost

a_revenue_3 = a_price_3 - a_c1_req * c1_cost - a_c2_req * c2_cost
b_revenue_3 = b_price_3 - b_c1_req * c1_cost - b_c2_req * c2_cost


# ============================================
# CREATE SOLVER
# ============================================

solver = pywraplp.Solver.CreateSolver("SCIP")
if not solver:
    raise Exception("SCIP solver not available.")

# ============================================
# DECISION VARIABLES
# ============================================
x_c1 = solver.NumVar(0, solver.infinity(), 'Batches of Component 1')
x_c2 = solver.NumVar(0, solver.infinity(), 'Batches of Component 2')
x_a1 = solver.NumVar(0, solver.infinity(), 'Units of Product A - Case 1')
x_b1 = solver.NumVar(0, solver.infinity(), 'Units of Product B - Case 1')
x_a2 = solver.NumVar(0, solver.infinity(), 'Units of Product A - Case 2')
x_b2 = solver.NumVar(0, solver.infinity(), 'Units of Product B - Case 2')
x_a3 = solver.NumVar(0, solver.infinity(), 'Units of Product A - Case 3')
x_b3 = solver.NumVar(0, solver.infinity(), 'Units of Product B - Case 3')


# ============================================
# OBJECTIVE FUNCTION
# ============================================
# Maximize Profit
solver.Maximize(
    prob_1 * (a_revenue_1 * x_a1 + b_revenue_1 * x_b1) +
    prob_2 * (a_revenue_2 * x_a2 + b_revenue_2 * x_b2) +
    prob_3 * (a_revenue_3 * x_a3 + b_revenue_3 * x_b3)
    - c1_capacity_cost * x_c1 - c2_capacity_cost * x_c2
)

# ============================================
# CONSTRAINTS
# ============================================
solver.Add(x_a1 <= a_demand)  # Demand for A
solver.Add(x_a2 <= a_demand)  # Demand for A
solver.Add(x_a3 <= a_demand)  # Demand for A
solver.Add(x_b1 <= b_demand)  # Demand for B
solver.Add(x_b2 <= b_demand)  # Demand for B
solver.Add(x_b3 <= b_demand)  # Demand for B
solver.Add(x_c1 + x_c2 <= capacity_limit)
solver.Add(x_c1 >= c1_current_capacity)
solver.Add(x_c2 >= c2_current_capacity)
solver.Add(a_c1_req * x_a1 + b_c1_req * x_b1 <= c1_batch * x_c1)  # Use of component C1
solver.Add(a_c1_req * x_a2 + b_c1_req * x_b2 <= c1_batch * x_c1)  # Use of component C1
solver.Add(a_c1_req * x_a3 + b_c1_req * x_b3 <= c1_batch * x_c1)  # Use of component C1
solver.Add(a_c2_req * x_a1 + b_c2_req * x_b1 <= c2_batch * x_c2)  # Use of component C2
solver.Add(a_c2_req * x_a2 + b_c2_req * x_b2 <= c2_batch * x_c2)  # Use of component C2
solver.Add(a_c2_req * x_a3 + b_c2_req * x_b3 <= c2_batch * x_c2)  # Use of component C2


# ============================================
# SOLVE
# ============================================
status = solver.Solve()

# ============================================
# RESULTS
# ============================================
if status == pywraplp.Solver.OPTIMAL:
    print('Overall Profit = $', solver.Objective().Value())
    print()
    for var in solver.variables():
        print(f"{var.name()} = {var.solution_value()}")
elif status == pywraplp.Solver.INFEASIBLE:
    print("The problem is infeasible — no solution satisfies all constraints.")
elif status == pywraplp.Solver.UNBOUNDED:
    print("The problem is unbounded — the objective can increase indefinitely.")
elif status == pywraplp.Solver.ABNORMAL:
    print("Solver stopped due to an abnormal error.")
else:
    print("Solver ended with status code:", status)
