import sys
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from constraint import Problem, AllDifferentConstraint

print("=" * 70)
print("BÀI TOÁN: MẬT MÃ SỐ HỌC (Cryptarithmetic - Slide 10)")
print("=" * 70)
print("1. ĐẶT BÀI TOÁN:")
print("   - Khôi phục các chữ số bí ẩn trong phép cộng chữ:")
print("        T  W  O")
print("     +  T  W  O")
print("     ──────────")
print("      F  O  U  R")
print("2. MÔ HÌNH CSP (X, D, C):")
print("   - Biến (Variables - 6 chữ cái): T, W, O, F, U, R")
print("   - Miền giá trị (Domains): {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}")
print("   - Ràng buộc (Constraints):")
print("       [C1] Các chữ số đôi một khác nhau (AllDifferent).")
print("       [C2] Chữ đứng đầu không được bằng 0: T != 0 và F != 0.")
print("       [C3] Phép tính đúng: 2 * (100*T + 10*W + O) == 1000*F + 100*O + 10*U + R.")
print("-" * 70)

problem = Problem()

letters = ['T', 'W', 'O', 'F', 'U', 'R']
problem.addVariables(letters, range(10))

# Các chữ số đôi một khác nhau
problem.addConstraint(AllDifferentConstraint())

# Chữ số đứng đầu không được bằng 0
problem.addConstraint(lambda t: t != 0, ['T'])
problem.addConstraint(lambda f: f != 0, ['F'])

# Ràng buộc phép cộng TWO + TWO = FOUR
def sum_constraint(t, w, o, f, u, r):
    two = 100 * t + 10 * w + o
    four = 1000 * f + 100 * o + 10 * u + r
    return two + two == four

problem.addConstraint(sum_constraint, ['T', 'W', 'O', 'F', 'U', 'R'])

solutions = problem.getSolutions()

print(f"3. KẾT QUẢ TÌM KIẾM: Tìm thấy {len(solutions)} nghiệm thỏa mãn")
print("   * Nhận xét: F luôn bằng 1 trong mọi nghiệm (vì 999 + 999 = 1998, hàng nghìn tối đa là 1).\n")

for idx, sol in enumerate(solutions, 1):
    t, w, o = sol['T'], sol['W'], sol['O']
    f, u, r = sol['F'], sol['U'], sol['R']
    two = 100 * t + 10 * w + o
    four = 1000 * f + 100 * o + 10 * u + r
    print(f"   -> Nghiệm {idx}: T={t}, W={w}, O={o}, F={f}, U={u}, R={r}")
    print(f"        Phép tính: {two} + {two} = {four} ({two + two == four})")
print("=" * 70 + "\n")
