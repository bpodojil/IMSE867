
# ==========
# Part A
# ==========

a_price_1 = 54
b_price_1 = 56
a_price_2 = 50
b_price_2 = 60
a_price_3 = 46
b_price_3 = 64

prob_1 = 0.3
prob_2 = 0.4
prob_3 = 0.3

a_expected = prob_1 * a_price_1 + prob_2 * a_price_2 + prob_3 * a_price_3
b_expected = prob_1 * b_price_1 + prob_2 * b_price_2 + prob_3 * b_price_3

print(f"The expected price for Product A: {a_expected}")
print(f"The expected price for Product B: {b_expected}")
