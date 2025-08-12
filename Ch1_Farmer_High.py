# ============================================
# PACKAGE MANAGEMENT
# ============================================
from ortools.linear_solver import pywraplp

# ============================================
# DECLARE VARIABLES
# ============================================
total_land = 500

required_w = 200
required_c = 240

plant_cost_w = 150
plant_cost_c = 230
plant_cost_s = 260

sell_price_w = 170
sell_price_c = 150

purchase_price_w = 1.4 * sell_price_w
purchase_price_c = 1.4 * sell_price_c

sell_price_s_high = 36
sell_price_s_low = 10

quota_s = 6000

yield_w = 2.5 * 1.2
yield_c = 3 * 1.2
yield_s = 20 * 1.2

# ============================================
# CREATE SOLVER
# ============================================
solver = pywraplp.Solver.CreateSolver('SCIP')
if not solver:
    raise Exception("SCIP solver not available.")

# ============================================
# DECISION VARIABLES
# ============================================
# Land Allocation
x1 = solver.IntVar(0, solver.infinity(), 'Acres of Wheat')
x2 = solver.IntVar(0, solver.infinity(), 'Acres of Corn')
x3 = solver.IntVar(0, solver.infinity(), 'Acres of Sugar Beats')

# Tons Sold
w1 = solver.IntVar(0, solver.infinity(), 'Tons of Wheat Sold')
w2 = solver.IntVar(0, solver.infinity(), 'Tons of Corn Sold')
w3 = solver.IntVar(0, solver.infinity(), 'Tons of Sugar Beets Sold (Higher)')
w4 = solver.IntVar(0, solver.infinity(), 'Tons of Sugar Beets Sold (Lower)')

# Tons Purchased
y1 = solver.IntVar(0, solver.infinity(), 'Tons of Wheat Bought')
y2 = solver.IntVar(0, solver.infinity(), 'Tons of Corn Bought')

# ============================================
# OBJECTIVE FUNCTION
# ============================================
# Minimize Farmer Cost
solver.Minimize(plant_cost_w * x1 + plant_cost_c * x2 + plant_cost_s * x3 +
                purchase_price_w * y1 + purchase_price_c * y2 -
                sell_price_w * w1 - sell_price_c * w2 - sell_price_s_high * w3 - sell_price_s_low * w4)

# ============================================
# CONSTRAINTS
# ============================================
solver.Add(x1 + x2 + x3 <= total_land)              # capacity
solver.Add(yield_w * x1 + y1 - w1 >= required_w)    # minimum selection
solver.Add(yield_c * x2 + y2 - w2 >= required_c)    # ensure required corn
solver.Add(w3 + w4 <= yield_s * x3)                 # beets sold do not exceed yield
solver.Add(w3 <= quota_s)                           # beets sold at high price limited by quota
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