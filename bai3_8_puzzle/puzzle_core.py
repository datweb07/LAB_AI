"""Quy tắc bài toán 8-Puzzle theo hình chụp bảng. Không phụ thuộc SimpleAI.

Trạng thái được hiểu là ma trận 3x3. Để graph_search=True của SimpleAI
làm việc được, nội bộ lưu dạng tuple 9 phần tử bất biến và có thể hash.
"""
from typing import Final

KICH_THUOC: Final = 3
O_TRONG: Final = 0
MA_TRAN_DAU: Final = ((2, 1, 0), (3, 4, 5), (7, 8, 6))
MA_TRAN_DICH: Final = ((1, 2, 3), (8, 0, 4), (7, 6, 5))


def chuyen_ma_tran_sang_tuple(ma_tran: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    return tuple(gia_tri for hang in ma_tran for gia_tri in hang)


TRANG_THAI_DAU: Final = chuyen_ma_tran_sang_tuple(MA_TRAN_DAU)
TRANG_THAI_DICH: Final = chuyen_ma_tran_sang_tuple(MA_TRAN_DICH)


def kiem_tra_trang_thai(trang_thai: tuple[int, ...]) -> None:
    if len(trang_thai) != 9 or set(trang_thai) != set(range(9)):
        raise ValueError("Trạng thái 8-Puzzle phải có đủ các giá trị 0..8, mỗi giá trị xuất hiện 1 lần")


# Tính một lần theo vị trí ô trống, giữ nguyên thứ tự sinh hành động.
_HANH_DONG_THEO_VI_TRI: Final = tuple(
    tuple(action for action, valid in (
        ("LEN", position // 3 > 0),
        ("XUONG", position // 3 < 2),
        ("PHAI", position % 3 < 2),
        ("TRAI", position % 3 > 0),
    ) if valid)
    for position in range(9)
)
_DO_LECH: Final = {"LEN": -3, "XUONG": 3, "TRAI": -1, "PHAI": 1}


def lay_hanh_dong_hop_le(trang_thai: tuple[int, ...]) -> list[str]:
    """Hướng di chuyển ô trống; tra bảng biên, không cắt hành động quay lui."""
    return list(_HANH_DONG_THEO_VI_TRI[trang_thai.index(O_TRONG)])


def di_chuyen_o_trong(trang_thai: tuple[int, ...], hanh_dong: str) -> tuple[int, ...]:
    """Đổi ô trống với ô kề, không sửa đầu vào hoặc thay đổi luật bài toán."""
    vi_tri_trong = trang_thai.index(O_TRONG)
    if hanh_dong not in _HANH_DONG_THEO_VI_TRI[vi_tri_trong]:
        raise ValueError(f"Hành động {hanh_dong!r} không hợp lệ")
    vi_tri_doi = vi_tri_trong + _DO_LECH[hanh_dong]
    trang_thai_moi = list(trang_thai)
    trang_thai_moi[vi_tri_trong], trang_thai_moi[vi_tri_doi] = (
        trang_thai_moi[vi_tri_doi], trang_thai_moi[vi_tri_trong]
    )
    return tuple(trang_thai_moi)


def h1_so_o_sai_vi_tri(trang_thai: tuple[int, ...]) -> int:
    """h1: số ô số 1..8 nằm sai vị trí (không tính ô trống 0)."""
    return sum(
        1 for vi_tri, gia_tri in enumerate(trang_thai)
        if gia_tri != O_TRONG and gia_tri != TRANG_THAI_DICH[vi_tri]
    )


VI_TRI_DICH = {
    gia_tri: divmod(vi_tri, KICH_THUOC)
    for vi_tri, gia_tri in enumerate(TRANG_THAI_DICH)
}


# Bảng khoảng cách của từng ô số tại từng vị trí, theo đúng Goal của đề.
_KHOANG_CACH_MANHATTAN: Final = tuple(
    tuple(
        0 if tile == O_TRONG else
        abs(position // 3 - VI_TRI_DICH[tile][0])
        + abs(position % 3 - VI_TRI_DICH[tile][1])
        for position in range(9)
    )
    for tile in range(9)
)


def h2_khoang_cach_manhattan(trang_thai: tuple[int, ...]) -> int:
    """Tổng Manhattan các ô 1..8; ô trống đóng góp 0."""
    return sum(_KHOANG_CACH_MANHATTAN[tile][position]
               for position, tile in enumerate(trang_thai))


def dem_nghich_the(trang_thai: tuple[int, ...]) -> int:
    cac_o_so = [gia_tri for gia_tri in trang_thai if gia_tri != O_TRONG]
    return sum(
        cac_o_so[vi_tri_dau] > cac_o_so[vi_tri_sau]
        for vi_tri_dau in range(len(cac_o_so))
        for vi_tri_sau in range(vi_tri_dau + 1, len(cac_o_so))
    )


def co_the_giai_duoc(bat_dau: tuple[int, ...], dich: tuple[int, ...]) -> bool:
    """Với bảng có 3 cột (số cột lẻ), parity nghịch thế phải bằng nhau."""
    kiem_tra_trang_thai(bat_dau)
    kiem_tra_trang_thai(dich)
    return dem_nghich_the(bat_dau) % 2 == dem_nghich_the(dich) % 2


def hien_thi_ma_tran(trang_thai: tuple[int, ...]) -> str:
    return "\n".join(
        "| " + " | ".join(str(gia_tri)
                         for gia_tri in trang_thai[hang * 3 : (hang + 1) * 3]) + " |"
        for hang in range(3)
    )
