# ============================================
# PACKAGE MANAGEMENT
# ============================================
from ortools.linear_solver import pywraplp

# ============================================
# Subproblem Switches
# ============================================
deterministic = 1

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

# ============================================
# CREATE SOLVER
# ============================================
if deterministic == 1:
    solver = pywraplp.Solver.CreateSolver("Deterministic")
    if not solver:
        raise Exception("SCIP solver not available.")

    # ============================================
    # DECISION VARIABLES
    # ============================================
    x_a = solver.Var(0, solver.infinity(), 'Batches of Product A')
    x_b = solver.Var(0, solver.infinity(), 'Batches of Product B')
    x_cap1 = solver.Var(0, solver.infinity(), 'Capacity for Component 1')
    x_cap2 = solver.Var(0, solver.infinity(), 'Capacity for Component 2')
    x_c1 = solver.Var(0, solver.infinity(), 'Batches of Component 1')
    x_c2 = solver.Var(0, solver.infinity(), 'Batches of Component 2')

    # ============================================
    # OBJECTIVE FUNCTION
    # ============================================
    # Minimize Farmer Cost
    solver.Maximize(a_price * x_a + b_price * x_b
                    - c1_capacity_cost * x_cap1 - c2_capacity_cost * x_cap2
                    - c1_cost * x_c1 - c2_cost * x_c2)

    # ============================================
    # CONSTRAINTS
    # ============================================
    solver.Add(x_a <= a_demand)  # Demand for A
    solver.Add(x_b <= b_demand) # Demand for B
    solver.Add(x_c1 <= c1_batch * (x_cap1 + c1_current_capacity)) # Production of C1 cannot exceed capacity
    solver.Add(x_c2 <= c2_batch * (x_cap2 + c2_current_capacity)) # Production of C2 cannot exceed capacity
    solver.Add(x_a <= a_c1_req * x_c1 + a_c2_req * x_c2)  # Product A component requirements
    solver.Add(x_b <= b_c1_req * x_c1 + b_c2_req * x_c2)  # Product B component requirements

    # ============================================
    # SOLVE
    # ============================================
    status = solver.Solve()

    # ============================================
    # RESULTS
    # ============================================
    if status == pywraplp.Solver.OPTIMAL:
        print('Overall Profit = $', -1 * solver.Objective().Value())
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



else:
    pass

print("All Problems Solved!")