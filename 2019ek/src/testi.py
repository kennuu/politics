import numpy as np

series = [np.math.factorial(n) * (1103 + 26390 * n) / (np.math.factorial(n)**4 * 396**(4*n)) for n in range(10)]

print(series)
print(1./(4 * np.sqrt(8) / 9801 * np.cumsum(series)))