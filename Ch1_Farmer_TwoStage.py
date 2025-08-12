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

yield_w_a = 2.5
yield_w_l = .8 * yield_w_a
yield_w_h = 1.2 * yield_w_a
yield_c_a = 3
yield_c_l = .8 * yield_c_a
yield_c_h = 1.2 * yield_c_a
yield_s_a = 20
yield_s_l = .8 * yield_s_a
yield_s_h = 1.2 * yield_s_a

prob_weather = (1/3)

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
w11 = solver.IntVar(0, solver.infinity(), 'Tons of Wheat Sold - Low Yield')
w12 = solver.IntVar(0, solver.infinity(), 'Tons of Wheat - Average Yield')
w13 = solver.IntVar(0, solver.infinity(), 'Tons of Wheat - High Yield')
w21 = solver.IntVar(0, solver.infinity(), 'Tons of Corn - Low Yield')
w22 = solver.IntVar(0, solver.infinity(), 'Tons of Corn - Average Yield')
w23 = solver.IntVar(0, solver.infinity(), 'Tons of Corn - High Yield')
w31 = solver.IntVar(0, solver.infinity(), 'Tons of Sugar Beet (High) - Low Yield')
w32 = solver.IntVar(0, solver.infinity(), 'Tons of Sugar Beet (High) - Average Yield')
w33 = solver.IntVar(0, solver.infinity(), 'Tons of Sugar Beet (High) - High Yield')
w41 = solver.IntVar(0, solver.infinity(), 'Tons of Sugar Beet (Low) - Low Yield')
w42 = solver.IntVar(0, solver.infinity(), 'Tons of Sugar Beet (Low) - Average Yield')
w43 = solver.IntVar(0, solver.infinity(), 'Tons of Sugar Beet (Low) - High Yield')

# Tons Purchased
y11 = solver.IntVar(0, solver.infinity(), 'Tons of Wheat Bought - Low Yield')
y12 = solver.IntVar(0, solver.infinity(), 'Tons of Wheat Bought - Average Yield')
y13 = solver.IntVar(0, solver.infinity(), 'Tons of Wheat Bought - High Yield')
y21 = solver.IntVar(0, solver.infinity(), 'Tons of Corn Bought - Low Yield')
y22 = solver.IntVar(0, solver.infinity(), 'Tons of Corn Bought - Average Yield')
y23 = solver.IntVar(0, solver.infinity(), 'Tons of Corn Bought - High Yield')

# ============================================
# OBJECTIVE FUNCTION
# ============================================
# Minimize Farmer Cost
solver.Minimize(plant_cost_w * x1 + plant_cost_c * x2 + plant_cost_s * x3 -
                prob_weather * (sell_price_w * w11 - purchase_price_w * y11 +
                                 sell_price_c * w21 - purchase_price_c * y21 +
                                 sell_price_s_high * w31 + sell_price_s_low * w41) -
                prob_weather * (sell_price_w * w12 - purchase_price_w * y12 +
                                 sell_price_c * w22 - purchase_price_c * y22 +
                                 sell_price_s_high * w32 + sell_price_s_low * w42) -
                prob_weather * (sell_price_w * w13 - purchase_price_w * y13 +
                                sell_price_c * w23 - purchase_price_c * y23 +
                                sell_price_s_high * w33 + sell_price_s_low * w43))

# ============================================
# CONSTRAINTS
# ============================================
solver.Add(x1 + x2 + x3 <= total_land)              # capacity
solver.Add(yield_w_l * x1 + y11 - w11 >= required_w) # ensure required wheat
solver.Add(yield_w_a * x1 + y12 - w12 >= required_w)
solver.Add(yield_w_h * x1 + y13 - w13 >= required_w)
solver.Add(yield_c_l * x2 + y21 - w21 >= required_c) # ensure required corn
solver.Add(yield_c_a * x2 + y22 - w22 >= required_c)
solver.Add(yield_c_h * x2 + y23 - w23 >= required_c)
solver.Add(w31 + w41 <= yield_s_l * x3)                 # beets sold do not exceed yield
solver.Add(w32 + w42 <= yield_s_a * x3)
solver.Add(w33 + w43 <= yield_s_h * x3)
solver.Add(w31 <= quota_s)                           # beets sold at high price limited by quota
solver.Add(w32 <= quota_s)
solver.Add(w33 <= quota_s)
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