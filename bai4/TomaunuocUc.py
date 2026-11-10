from constraint import Problem

problem = Problem()

regions = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
colors = ['red', 'green', 'blue']

problem.addVariables(regions, colors)

# Ràng buộc các bang kề nhau khác màu (Slide 5 & 7)
edges = [
    ('WA', 'NT'), ('WA', 'SA'),
    ('NT', 'SA'), ('NT', 'Q'),
    ('SA', 'Q'), ('SA', 'NSW'), ('SA', 'V'),
    ('Q', 'NSW'),
    ('NSW', 'V')
]

for var1, var2 in edges:
    problem.addConstraint(lambda c1, c2: c1 != c2, (var1, var2))

solutions = problem.getSolutions()
print(f"\n--- Map Coloring (Slide 5-7): Tìm thấy {len(solutions)} nghiệm ---")
print("Ví dụ nghiệm đầu tiên:")
print(solutions[0])