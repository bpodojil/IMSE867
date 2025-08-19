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

a_price = 50
b_price = 60

a_revenue = a_price - a_c1_req * c1_cost - a_c2_req * c2_cost
b_revenue = b_price - b_c1_req * c1_cost - b_c2_req * c2_cost

# ============================================
# CREATE SOLVER
# ============================================

solver = pywraplp.Solver.CreateSolver("SCIP")
if not solver:
    raise Exception("SCIP solver not available.")

# ============================================
# DECISION VARIABLES
# ============================================
x_c1 = solver.NumVar(0, solver.infinity(), 'Batches_of_Component_1')
x_c2 = solver.NumVar(0, solver.infinity(), 'Batches_of_Component_2')
x_a = solver.NumVar(0, solver.infinity(), 'Batches_of_Product_A')
x_b = solver.NumVar(0, solver.infinity(), 'Batches_of_Product_B')

# ============================================
# OBJECTIVE FUNCTION
# ============================================
# Maximize Profit
solver.Maximize(
    a_revenue * x_a + b_revenue * x_b
    - c1_capacity_cost * x_c1 - c2_capacity_cost * x_c2
)

# ============================================
# CONSTRAINTS
# ============================================
solver.Add(x_a <= a_demand)  # Demand for A
solver.Add(x_b <= b_demand)  # Demand for B
solver.Add(x_c1 + x_c2 <= capacity_limit)
solver.Add(x_c1 >= c1_current_capacity)
solver.Add(x_c2 >= c2_current_capacity)
solver.Add(a_c1_req * x_a + b_c1_req * x_b <= c1_batch * x_c1)  # Use of component C1
solver.Add(a_c2_req * x_a + b_c2_req * x_b <= c2_batch * x_c2)  # Use of component C2


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
