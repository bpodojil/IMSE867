from ortools.linear_solver import pywraplp

# ============================================
# CONSTANTS
# ============================================
a_c1_req, a_c2_req = 6, 8
b_c1_req, b_c2_req = 10, 5

c1_cost, c2_cost = 0.4, 1.2
c1_capacity_cost, c2_capacity_cost = 150, 180
c1_current_capacity, c2_current_capacity = 40, 20
capacity_limit = 120
c1_batch, c2_batch = 60, 90
a_demand, b_demand = 500, 200

# Scenarios: (a_price, b_price, probability)
scenarios = [
    (70, 50, 0.3),
    (50, 60, 0.4),
    (30, 70, 0.3),
]

# ============================================
# CREATE SOLVER
# ============================================
solver = pywraplp.Solver.CreateSolver("SCIP")
if not solver:
    raise Exception("SCIP solver not available.")

# ============================================
# DECISION VARIABLES
# ============================================
x_c1 = solver.NumVar(0, solver.infinity(), "Batches of Component 1")
x_c2 = solver.NumVar(0, solver.infinity(), "Batches of Component 2")

x_a, x_b = {}, {}
for i in range(len(scenarios)):
    x_a[i] = solver.NumVar(0, solver.infinity(), f"Units of Product A - Case {i+1}")
    x_b[i] = solver.NumVar(0, solver.infinity(), f"Units of Product B - Case {i+1}")

# ============================================
# OBJECTIVE FUNCTION
# ============================================
objective_terms = []
for i, (a_price, b_price, prob) in enumerate(scenarios):
    a_revenue = a_price - a_c1_req * c1_cost - a_c2_req * c2_cost
    b_revenue = b_price - b_c1_req * c1_cost - b_c2_req * c2_cost
    objective_terms.append(prob * (a_revenue * x_a[i] + b_revenue * x_b[i]))

solver.Maximize(sum(objective_terms) - c1_capacity_cost * x_c1 - c2_capacity_cost * x_c2)

# ============================================
# CONSTRAINTS
# ============================================
for i in range(len(scenarios)):
    solver.Add(x_a[i] <= a_demand)  # Demand for A
    solver.Add(x_b[i] <= b_demand)  # Demand for B
    solver.Add(a_c1_req * x_a[i] + b_c1_req * x_b[i] <= c1_batch * x_c1)  # C1 usage
    solver.Add(a_c2_req * x_a[i] + b_c2_req * x_b[i] <= c2_batch * x_c2)  # C2 usage

solver.Add(x_c1 + x_c2 <= capacity_limit)
solver.Add(x_c1 >= c1_current_capacity)
solver.Add(x_c2 >= c2_current_capacity)

# ============================================
# SOLVE
# ============================================
status = solver.Solve()

# ============================================
# RESULTS
# ============================================
if status == pywraplp.Solver.OPTIMAL:
    print("Overall Profit = $", solver.Objective().Value())
    print()
    for var in solver.variables():
        print(f"{var.name()} = {var.solution_value()}")
else:
    print("Solver ended with status code:", status)
