"""Chạy: python main.py --bai all --seed 42 (từ thư mục btvn_csp_ga)."""

import argparse

from csp_models import board_text, compare_backtracking, solve_equations
from genetic_queens import QueensSearchProblem, custom_genetic, simpleai_genetic


def print_ga(result, n):
    problem = QueensSearchProblem(n)
    print("Cấu hình (hàng theo cột 1..n):", result.state)
    print(board_text(result.state))
    print(f"Số cặp hậu xung đột: {problem.conflicts(result.state)}")
    print("Trạng thái:", "TÌM ĐƯỢC NGHIỆM" if result.solved else "CHƯA TÌM ĐƯỢC NGHIỆM trong giới hạn")
    print("Số thế hệ:", result.generations)
    print("Số lần khởi tạo / lai / đột biến:", result.calls)


def exercise_one(args):
    print(f"\nBÀI 1 - GA TỰ CÀI ĐẶT: {args.n} HẬU")
    print("Khởi tạo ngẫu nhiên; tournament; lai một điểm; đột biến một gene; elitism; nhập cư 10%.")
    demo = QueensSearchProblem(args.n, args.seed)
    parent1, parent2 = demo.generate_random_state(), demo.generate_random_state()
    child = demo.crossover(parent1, parent2)
    mutant = demo.mutate(child)
    print("Minh họa cha:", parent1, "| mẹ:", parent2)
    print("Con sau lai:", child, "| sau đột biến:", mutant)
    result = custom_genetic(args.n, args.seed, args.population, args.mutation, args.generations)
    print_ga(result, args.n)
    print("Lịch sử xung đột tốt nhất (tối đa 30 thế hệ đầu):", result.history[:30])


def print_backtracking_table(records):
    headers = ("Chiến lược", "AC-3", "Nghiệm (hàng theo cột)", "Số lần kiểm tra ràng buộc")
    rows = []
    for label, inference, solution, checks in records:
        state = tuple(solution[c] for c in range(1, 6)) if solution else None
        rows.append((label, str(inference), str(state), str(checks)))
    widths = [max(len(row[col]) for row in [headers, *rows]) for col in range(len(headers))]
    border = "+" + "+".join("-" * (width + 2) for width in widths) + "+"

    def format_row(row, header=False):
        cells = []
        for col, (value, width) in enumerate(zip(row, widths)):
            if header or col == 0:
                cells.append(value.ljust(width))
            elif col == 3:
                cells.append(value.rjust(width))
            else:
                cells.append(value.center(width))
        return "| " + " | ".join(cells) + " |"

    print(border)
    print(format_row(headers, header=True))
    print(border)
    for row in rows:
        print(format_row(row))
        print(border)


def exercise_two(args):
    print("\nBÀI 2 - CSP 5 HẬU VÀ CHUYỂN SANG SEARCH/GA")
    print("X = {Q1,..,Q5}; Di = {1,2,3,4,5}; Qi là hàng hậu ở cột i.")
    print("Với i<j: Qi != Qj và abs(Qi-Qj) != abs(i-j). Có 10 ràng buộc nhị phân.")
    records = compare_backtracking(5)
    print()
    print_backtracking_table(records)
    print("\nBàn cờ nghiệm backtrack mẫu:")
    print(board_text(tuple(records[0][2][c] for c in range(1, 6))))
    print("\nSearch: trạng thái đầy đủ; hành động đổi hàng một hậu; đích không xung đột.")
    print("Fitness = 1 + 10 - số cặp hậu xung đột. Giải bằng simpleai.search.genetic:")
    result, final = simpleai_genetic(5, args.seed, args.population, args.mutation, args.search_generations)
    print_ga(result, 5)
    print("Cá thể tốt nhất của thế hệ cuối do SimpleAI trả về:", final)
    print("Kết quả báo cáo ở trên là cá thể tốt nhất từng được đánh giá.")


def exercise_three():
    print("\nBÀI 3 - BACKTRACK GIẢI HỆ PHƯƠNG TRÌNH NGHIỆM NGUYÊN")
    print("Biến: x,y. D(x) = D(y) = {-10,-9,...,10} (21 giá trị).")
    print("C1: 3*x + 2*y == 25; C2: 2*x - y == 5.")
    solution = solve_equations(inference=False)
    print("Kết quả backtrack (inference=False):", solution)
    if solution is not None:
        x, y = solution["x"], solution["y"]
        print(f"Kiểm tra C1: 3*{x} + 2*{y} = {3*x+2*y}")
        print(f"Kiểm tra C2: 2*{x} - {y} = {2*x-y}")


def main():
    parser = argparse.ArgumentParser(description="BTVN CSP và GA sử dụng SimpleAI")
    parser.add_argument("--bai", choices=("all", "1", "2", "3"), default="all")
    parser.add_argument("--n", type=int, default=8, help="Kích thước N hậu bài 1; bài 2 luôn 5")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--population", type=int, default=120)
    parser.add_argument("--mutation", type=float, default=0.25)
    parser.add_argument("--generations", type=int, default=2000, help="Giới hạn GA tự cài bài 1")
    parser.add_argument("--search-generations", type=int, default=200, help="Giới hạn GA SimpleAI bài 2")
    args = parser.parse_args()
    if args.n < 1 or args.population < 2 or args.generations < 1 or args.search_generations < 1:
        parser.error("n >= 1, population >= 2, số thế hệ >= 1")
    if not 0 <= args.mutation <= 1:
        parser.error("mutation phải thuộc [0,1]")
    print(f"Seed = {args.seed}; quần thể = {args.population}; xác suất đột biến = {args.mutation}")
    if args.bai in ("all", "1"):
        exercise_one(args)
    if args.bai in ("all", "2"):
        exercise_two(args)
    if args.bai in ("all", "3"):
        exercise_three()


if __name__ == "__main__":
    main()
