import sys
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from constraint import Problem

print("=" * 65)
print("BÀI TOÁN: HỆ RÀNG BUỘC SỐ HỌC NHỊ PHÂN (Slide 4)")
print("=" * 65)
print("1. ĐẶT BÀI TOÁN:")
print("   - Tìm các giá trị nhị phân cho 6 biến x1..x6 thỏa mãn hệ điều kiện số học.")
print("2. MÔ HÌNH CSP (X, D, C):")
print("   - Biến (Variables)      : x1, x2, x3, x4, x5, x6")
print("   - Miền giá trị (Domains): {0, 1} (cho tất cả 6 biến)")
print("   - Ràng buộc (Constraints):")
print("       [C1] x1 + x2 + x6 == 1")
print("       [C2] x1 - x3 + x4 == 1")
print("       [C3] x4 + x5 - x6 > 0")
print("       [C4] x2 + x5 - x6 == 0")
print("-" * 65)

problem = Problem()

variables = ['x1', 'x2', 'x3', 'x4', 'x5', 'x6']
problem.addVariables(variables, [0, 1])

problem.addConstraint(lambda x1, x2, x6: x1 + x2 + x6 == 1, ('x1', 'x2', 'x6'))
problem.addConstraint(lambda x1, x3, x4: x1 - x3 + x4 == 1, ('x1', 'x3', 'x4'))
problem.addConstraint(lambda x4, x5, x6: x4 + x5 - x6 > 0, ('x4', 'x5', 'x6'))
problem.addConstraint(lambda x2, x5, x6: x2 + x5 - x6 == 0, ('x2', 'x5', 'x6'))

solutions = problem.getSolutions()

print(f"3. KẾT QUẢ TÌM KIẾM: Tìm thấy {len(solutions)} nghiệm")
for idx, sol in enumerate(solutions, 1):
    x1, x2, x3 = sol['x1'], sol['x2'], sol['x3']
    x4, x5, x6 = sol['x4'], sol['x5'], sol['x6']
    print(f"\n   -> Nghiệm {idx}: (x1={x1}, x2={x2}, x3={x3}, x4={x4}, x5={x5}, x6={x6})")
    print("      Kiểm chứng các phương trình:")
    print(f"        * [C1] x1 + x2 + x6 = {x1} + {x2} + {x6} = {x1 + x2 + x6} (kết quả == 1 -> {x1 + x2 + x6 == 1})")
    print(f"        * [C2] x1 - x3 + x4 = {x1} - {x3} + {x4} = {x1 - x3 + x4} (kết quả == 1 -> {x1 - x3 + x4 == 1})")
    print(f"        * [C3] x4 + x5 - x6 = {x4} + {x5} - {x6} = {x4 + x5 - x6} (kết quả > 0  -> {x4 + x5 - x6 > 0})")
    print(f"        * [C4] x2 + x5 - x6 = {x2} + {x5} - {x6} = {x2 + x5 - x6} (kết quả == 0 -> {x2 + x5 - x6 == 0})")
print("=" * 65 + "\n")
