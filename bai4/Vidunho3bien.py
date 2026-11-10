import sys
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from constraint import Problem

print("=" * 60)
print("BÀI TOÁN: VÍ DỤ NHỎ 3 BIẾN (Slide 13)")
print("=" * 60)
print("1. ĐẶT BÀI TOÁN:")
print("   - Tìm giá trị của 3 biến X, Y, Z thỏa mãn các điều kiện quan hệ.")
print("2. MÔ HÌNH CSP (X, D, C):")
print("   - Biến (Variables)      : X, Y, Z")
print("   - Miền giá trị (Domains): {1, 2} (cho cả 3 biến)")
print("   - Ràng buộc (Constraints):")
print("       [C1] X == Y  (X có giá trị bằng Y)")
print("       [C2] X != Z  (X có giá trị khác Z)")
print("       [C3] Y > Z   (Y có giá trị lớn hơn Z)")
print("-" * 60)

problem = Problem()
problem.addVariables(['X', 'Y', 'Z'], [1, 2])

problem.addConstraint(lambda x, y: x == y, ('X', 'Y'))
problem.addConstraint(lambda x, z: x != z, ('X', 'Z'))
problem.addConstraint(lambda y, z: y > z, ('Y', 'Z'))

solutions = problem.getSolutions()

print(f"3. KẾT QUẢ TÌM KIẾM: Tìm thấy {len(solutions)} nghiệm")
for idx, sol in enumerate(solutions, 1):
    x, y, z = sol['X'], sol['Y'], sol['Z']
    print(f"   -> Nghiệm {idx}: X = {x}, Y = {y}, Z = {z}")
    print("   -> Kiểm chứng điều kiện:")
    print(f"        * X == Y : {x} == {y} -> {x == y}")
    print(f"        * X != Z : {x} != {z} -> {x != z}")
    print(f"        * Y > Z  : {y} > {z}  -> {y > z}")
print("=" * 60 + "\n")
