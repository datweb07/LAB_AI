"""Dữ liệu đồ thị có trọng số để thực hành 5 thuật toán Chương 3."""
from dataclasses import dataclass

# Hai thành phố/nút kề nhau có chi phí di chuyển theo hướng từ trái sang phải.
# Ví dụ: S -> A có chi phí 4, S -> B có chi phí 1.
DO_THI = {
    "S": [("A", 4), ("B", 1)],
    "A": [("C", 2), ("G", 9)],
    "B": [("A", 1), ("D", 5)],
    "C": [("G", 2)],
    "D": [("G", 1)],
    "G": [],
}
TRANG_THAI_DAU = "S"
TRANG_THAI_DICH = "G"


@dataclass
class KetQuaTimKiem:
    ten_thuat_toan: str
    duong_di: list[str] | None
    chi_phi: int | None
    so_nut_da_duyet: int
    thong_bao: str = ""


def tinh_chi_phi(duong_di: list[str]) -> int:
    """Tính tổng trọng số trên đường đi; trả lỗi nếu cạnh không tồn tại."""
    tong_chi_phi = 0
    for nut_hien_tai, nut_tiep_theo in zip(duong_di, duong_di[1:]):
        for nut_ke, chi_phi_canh in DO_THI[nut_hien_tai]:
            if nut_ke == nut_tiep_theo:
                tong_chi_phi += chi_phi_canh
                break
        else:
            raise ValueError(f"Không có cạnh từ {nut_hien_tai} tới {nut_tiep_theo}")
    return tong_chi_phi
