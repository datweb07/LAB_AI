"""Quy tắc bài toán 8-Puzzle theo hình chụp bảng. Không phụ thuộc SimpleAI.

Trạng thái được hiểu là ma trận 3x3. Để graph_search=True của SimpleAI
làm việc được, nội bộ lưu dạng tuple 9 phần tử bất biến và có thể hash.
"""
from typing import Final

KICH_THUOC: Final = 3
O_TRONG: Final = 0
MA_TRAN_DAU: Final = ((2, 1, 0), (3, 4, 5), (7, 8, 6))
MA_TRAN_DICH: Final = ((1, 2, 3), (8, 0, 4), (7, 6, 5))
MA_TRAN_DEMO: Final = ((1, 2, 3), (8, 4, 0), (7, 6, 5))


def chuyen_ma_tran_sang_tuple(ma_tran: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    return tuple(gia_tri for hang in ma_tran for gia_tri in hang)


TRANG_THAI_DAU: Final = chuyen_ma_tran_sang_tuple(MA_TRAN_DAU)
TRANG_THAI_DICH: Final = chuyen_ma_tran_sang_tuple(MA_TRAN_DICH)
TRANG_THAI_DEMO: Final = chuyen_ma_tran_sang_tuple(MA_TRAN_DEMO)


def kiem_tra_trang_thai(trang_thai: tuple[int, ...]) -> None:
    if len(trang_thai) != 9 or set(trang_thai) != set(range(9)):
        raise ValueError("Trạng thái 8-Puzzle phải có đủ các giá trị 0..8, mỗi giá trị xuất hiện 1 lần")


def lay_hanh_dong_hop_le(trang_thai: tuple[int, ...]) -> list[str]:
    """Hành động là hướng dịch chuyển của Ô TRỐNG, không phải ô số."""
    vi_tri_trong = trang_thai.index(O_TRONG)
    hang, cot = divmod(vi_tri_trong, KICH_THUOC)
    danh_sach_hanh_dong = []
    if hang > 0:
        danh_sach_hanh_dong.append("LEN")
    if hang < KICH_THUOC - 1:
        danh_sach_hanh_dong.append("XUONG")
    if cot > 0:
        danh_sach_hanh_dong.append("TRAI")
    if cot < KICH_THUOC - 1:
        danh_sach_hanh_dong.append("PHAI")
    return danh_sach_hanh_dong


def di_chuyen_o_trong(trang_thai: tuple[int, ...], hanh_dong: str) -> tuple[int, ...]:
    """Trả về trạng thái mới. Không thay đổi tuple đầu vào."""
    if hanh_dong not in lay_hanh_dong_hop_le(trang_thai):
        raise ValueError(f"Hành động {hanh_dong!r} không hợp lệ")
    vi_tri_trong = trang_thai.index(O_TRONG)
    do_lech = {"LEN": -3, "XUONG": 3, "TRAI": -1, "PHAI": 1}[hanh_dong]
    vi_tri_doi = vi_tri_trong + do_lech
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


def h2_khoang_cach_manhattan(trang_thai: tuple[int, ...]) -> int:
    """h2: tổng |hàng-hiện-tại - hàng-đích| + |cột-hiện-tại - cột-đích|."""
    tong_khoang_cach = 0
    for vi_tri, gia_tri in enumerate(trang_thai):
        if gia_tri == O_TRONG:
            continue
        hang_hien_tai, cot_hien_tai = divmod(vi_tri, KICH_THUOC)
        hang_dich, cot_dich = VI_TRI_DICH[gia_tri]
        tong_khoang_cach += abs(hang_hien_tai - hang_dich) + abs(cot_hien_tai - cot_dich)
    return tong_khoang_cach


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
        "| " + " | ".join(" " if gia_tri == O_TRONG else str(gia_tri)
                         for gia_tri in trang_thai[hang * 3 : (hang + 1) * 3]) + " |"
        for hang in range(3)
    )
