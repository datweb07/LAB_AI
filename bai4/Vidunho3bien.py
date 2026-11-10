from constraint import Problem

problem = Problem()
problem.addVariables(['X', 'Y', 'Z'], [1, 2])

problem.addConstraint(lambda x, y: x == y, ('X', 'Y'))
problem.addConstraint(lambda x, z: x != z, ('X', 'Z'))
problem.addConstraint(lambda y, z: y > z, ('Y', 'Z'))

solutions = problem.getSolutions()
print(f"\n--- Slide 13: Tìm thấy {len(solutions)} nghiệm ---")
print(solutions)