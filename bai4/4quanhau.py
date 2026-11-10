import sys
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from constraint import Problem

print("=" * 65)
print("BÀI TOÁN: XẾP 4 QUÂN HẬU (4-Queens Problem - Slide 42)")
print("=" * 65)
print("1. ĐẶT BÀI TOÁN:")
print("   - Đặt 4 quân hậu lên bàn cờ kích thước 4x4.")
print("   - Quy tắc: Không có 2 quân hậu nào ăn nhau (không cùng hàng,")
print("     không cùng cột, không cùng đường chéo).")
print("2. MÔ HÌNH CSP (X, D, C):")
print("   - Biến (Variables)      : [0, 1, 2, 3] tương ứng 4 cột từ trái qua phải.")
print("   - Miền giá trị (Domains): {0, 1, 2, 3} tương ứng 4 hàng từ trên xuống dưới.")
print("   - Ràng buộc (Constraints cho mọi cặp cột c1 < c2):")
print("       [C1] Khác hàng     : r1 != r2")
print("       [C2] Khác đường chéo: abs(r1 - r2) != abs(c1 - c2)")
print("-" * 65)

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

def render_board(sol):
    """Vẽ bàn cờ 4x4 minh họa vị trí quân hậu Q."""
    lines = []
    lines.append("        Cột: 0   1   2   3")
    lines.append("            ┌───┬───┬───┬───┐")
    for r in range(4):
        row_str = f"    Hàng {r} │"
        for c in range(4):
            char = " Q " if sol[c] == r else " . "
            row_str += char + "│"
        lines.append(row_str)
        lines.append("            ├───┼───┼───┼───┤" if r < 3 else "            └───┴───┴───┴───┘")
    return "\n".join(lines)

print(f"3. KẾT QUẢ TÌM KIẾM: Tìm thấy {len(solutions)} nghiệm hợp lệ\n")
for idx, sol in enumerate(solutions, 1):
    positions = ", ".join(f"Cột {c}->Hàng {sol[c]}" for c in queens)
    print(f"   -> Nghiệm {idx}: ({positions})")
    print(render_board(sol))
    print()
print("=" * 65 + "\n")
