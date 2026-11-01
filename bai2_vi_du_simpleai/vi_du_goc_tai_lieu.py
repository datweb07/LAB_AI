"""Ví dụ HELLO WORLD có trong README / tài liệu chính thức của SimpleAI.

Nguồn: https://simpleai.readthedocs.io/en/latest/
       https://github.com/simpleai-team/simpleai
Bản viết lại tương đương với đoạn ví dụ trong tài liệu, KHÔNG tự cài thuật toán.
Lưu ý: A* với hàm heuristic đơn giản này và GOAL dài có thể rất chậm.
Dùng `vi_du_chay_nhanh.py` để kiểm chứng nhanh trong lớp.
"""
from simpleai.search import SearchProblem, astar

GOAL = "HELLO WORLD"


class HelloProblem(SearchProblem):
    def actions(self, state):
        if len(state) < len(GOAL):
            return list(" ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        return []

    def result(self, state, action):
        return state + action

    def is_goal(self, state):
        return state == GOAL

    def heuristic(self, state):
        wrong = sum(1 for index in range(len(state)) if state[index] != GOAL[index])
        missing = len(GOAL) - len(state)
        return wrong + missing


def main():
    problem = HelloProblem(initial_state="")
    result = astar(problem)
    if result is not None:
        print("Kết quả:", result.state)
        print("Đường đi:", result.path())
    else:
        print("Không tìm được lời giải")


if __name__ == "__main__":
    main()
