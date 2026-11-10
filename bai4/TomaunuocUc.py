import sys
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from constraint import Problem

print("=" * 70)
print("BÀI TOÁN: TÔ MÀU BẢN ĐỒ NƯỚC ÚC (Map Coloring - Slide 5-7)")
print("=" * 70)
print("1. ĐẶT BÀI TOÁN:")
print("   - Tô màu 7 bang/vùng lãnh thổ của nước Úc bằng 3 màu.")
print("   - Quy tắc: Hai bang nào có chung đường biên giới thì KHÔNG được cùng màu.")
print("2. MÔ HÌNH CSP (X, D, C):")
print("   - Biến (Variables - 7 bang):")
print("       WA (Western Australia), NT (Northern Territory), SA (South Australia),")
print("       Q (Queensland), NSW (New South Wales), V (Victoria), T (Tasmania - đảo).")
print("   - Miền giá trị (Domains): {'red', 'green', 'blue'} (cho tất cả các bang)")
print("   - Ràng buộc (Constraints - 9 cặp biên giới kề nhau):")
print("       WA-NT, WA-SA, NT-SA, NT-Q, SA-Q, SA-NSW, SA-V, Q-NSW, NSW-V.")
print("       (Lưu ý: Tasmania là đảo tách rời, không giáp bang nào nên không có ràng buộc).")
print("-" * 70)

problem = Problem()

regions = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
colors = ['red', 'green', 'blue']

problem.addVariables(regions, colors)

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

print(f"3. KẾT QUẢ TÌM KIẾM: Tìm thấy {len(solutions)} phương án tô màu hợp lệ")
print("   * Giải thích toán học: Đất liền có 6 cách phối màu (3! hoán vị).")
print("     Đảo Tasmania (T) độc lập nên có 3 lựa chọn màu tùy ý -> Tổng cộng 6 x 3 = 18 nghiệm.\n")

print("   -> Nghiệm mẫu số 1 (Chi tiết):")
sample = solutions[0]
for r in regions:
    print(f"        {r:>4}: {sample[r]}")

print("\n   -> Kiểm tra 9 biên giới của nghiệm 1 (đảm bảo khác màu):")
all_valid = True
for v1, v2 in edges:
    valid = sample[v1] != sample[v2]
    all_valid = all_valid and valid
    print(f"        * {v1} ({sample[v1]}) != {v2} ({sample[v2]}) -> {valid}")

print("\n   -> Danh sách tóm tắt toàn bộ 18 nghiệm [WA, NT, SA, Q, NSW, V, T]:")
for idx, sol in enumerate(solutions, 1):
    vals = f"WA={sol['WA']:<5} NT={sol['NT']:<5} SA={sol['SA']:<5} Q={sol['Q']:<5} NSW={sol['NSW']:<5} V={sol['V']:<5} T={sol['T']}"
    print(f"      Cách {idx:>2}: {vals}")
print("=" * 70 + "\n")
