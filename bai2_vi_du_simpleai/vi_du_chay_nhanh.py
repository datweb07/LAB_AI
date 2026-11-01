"""Biến thể ngắn của ví dụ HelloProblem để chạy thực tế ngay trên lớp.

Thuật toán lấy trực tiếp từ thư viện SimpleAI, không phải tự viết.
"""
import sys
from simpleai.search import SearchProblem, astar, breadth_first

GOAL = "AI"


class HelloProblem(SearchProblem):
    def actions(self, state):
        if len(state) >= len(GOAL):
            return []
        return list(" ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def result(self, state, action):
        return state + action

    def is_goal(self, state):
        return state == GOAL

    def cost(self, state, action, state2):
        return 1

    def heuristic(self, state):
        sai_vi_tri = sum(
            1 for index, character in enumerate(state) if character != GOAL[index]
        )
        ky_tu_con_thieu = len(GOAL) - len(state)
        return sai_vi_tri + ky_tu_con_thieu


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    print("BÀI 2 - VÍ DỤ SIMPLEAI, TẠO CHUỖI 'AI'")
    for ten_thuat_toan, thuat_toan in [("BFS", breadth_first), ("A*", astar)]:
        problem = HelloProblem(initial_state="")
        result = thuat_toan(problem, graph_search=True)
        if result is None:
            print(f"{ten_thuat_toan}: không tìm thấy")
        else:
            print(f"{ten_thuat_toan}: {result.state}, đường đi = {result.path()}")


if __name__ == "__main__":
    main()
