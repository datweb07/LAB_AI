"""Định nghĩa bài toán; 7 thuật toán được gọi từ simpleai.search."""
from simpleai.search import SearchProblem
from .puzzle_core import (
    lay_hanh_dong_hop_le,
    di_chuyen_o_trong,
    h1_so_o_sai_vi_tri,
    h2_khoang_cach_manhattan,
    TRANG_THAI_DICH,
)


class BaiToan8Puzzle(SearchProblem):
    def __init__(self, initial_state: tuple[int, ...], loai_heuristic: str = "h2"):
        if loai_heuristic not in ("h1", "h2"):
            raise ValueError("Heuristic phải là 'h1' hoặc 'h2'")
        super().__init__(initial_state=initial_state)
        self.loai_heuristic = loai_heuristic

    def actions(self, state: tuple[int, ...]) -> list[str]:
        return lay_hanh_dong_hop_le(state)

    def result(self, state: tuple[int, ...], action: str) -> tuple[int, ...]:
        return di_chuyen_o_trong(state, action)

    def is_goal(self, state: tuple[int, ...]) -> bool:
        return state == TRANG_THAI_DICH

    def cost(self, state: tuple[int, ...], action: str, state2: tuple[int, ...]) -> int:
        # Mỗi bước chuyển ô trống được tính chi phí = 1.
        return 1

    def heuristic(self, state: tuple[int, ...]) -> int:
        if self.loai_heuristic == "h1":
            return h1_so_o_sai_vi_tri(state)
        return h2_khoang_cach_manhattan(state)
