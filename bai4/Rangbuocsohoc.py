from constraint import Problem

problem = Problem()

# Khai báo các biến và miền giá trị {0, 1}
variables = ['x1', 'x2', 'x3', 'x4', 'x5', 'x6']
problem.addVariables(variables, [0, 1])

# Khai báo các ràng buộc theo slide 4
problem.addConstraint(lambda x1, x2, x6: x1 + x2 + x6 == 1, ('x1', 'x2', 'x6'))
problem.addConstraint(lambda x1, x3, x4: x1 - x3 + x4 == 1, ('x1', 'x3', 'x4'))
problem.addConstraint(lambda x4, x5, x6: x4 + x5 - x6 > 0, ('x4', 'x5', 'x6'))
problem.addConstraint(lambda x2, x5, x6: x2 + x5 - x6 == 0, ('x2', 'x5', 'x6'))

solutions = problem.getSolutions()
print(f"--- Slide 4: Tìm thấy {len(solutions)} nghiệm ---")
for sol in solutions:
    print(sol)