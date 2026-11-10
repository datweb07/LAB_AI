from constraint import Problem

problem = Problem()
queens = [0, 1, 2, 3]  # Đại diện cho 4 cột
problem.addVariables(queens, range(4))  # Hàng từ 0 đến 3

# Ràng buộc không ăn nhau: khác hàng và khác đường chéo
for q1 in queens:
    for q2 in queens:
        if q1 < q2:
            problem.addConstraint(
                lambda r1, r2, c1=q1, c2=q2: r1 != r2 and abs(r1 - r2) != abs(c1 - c2),
                (q1, q2)
            )

solutions = problem.getSolutions()
print(f"\n--- 4-Queens (Slide 42): Tìm thấy {len(solutions)} nghiệm ---")
for idx, sol in enumerate(solutions, 1):
    print(f"Nghiệm {idx}: {sol}")