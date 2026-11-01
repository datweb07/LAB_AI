"""

BFS: hàng đợi FIFO; 
DFS: ngăn xếp LIFO;
UCS: hàng đợi ưu tiên theo chi phí; 
DLS: DFS có giới hạn;
IDS: lặp DLS với giới hạn 0,1,2,...

"""
from collections import deque
import heapq
from itertools import count

from .do_thi import DO_THI, KetQuaTimKiem, tinh_chi_phi


def tim_kiem_theo_chieu_rong(bat_dau: str, dich: str) -> KetQuaTimKiem:
    """BFS tìm đường đi ít cạnh nhất trên đồ thị hữu hạn."""
    hang_doi = deque([(bat_dau, [bat_dau])])
    da_phat_hien = {bat_dau}
    so_nut_da_duyet = 0

    while hang_doi:
        nut_hien_tai, duong_di = hang_doi.popleft()
        so_nut_da_duyet += 1
        if nut_hien_tai == dich:
            return KetQuaTimKiem("BFS", duong_di, tinh_chi_phi(duong_di), so_nut_da_duyet)
        for nut_ke, _ in DO_THI[nut_hien_tai]:
            if nut_ke not in da_phat_hien:
                da_phat_hien.add(nut_ke)
                hang_doi.append((nut_ke, duong_di + [nut_ke]))

    return KetQuaTimKiem("BFS", None, None, so_nut_da_duyet, "Không tìm thấy đường đi")


def tim_kiem_theo_chieu_sau(bat_dau: str, dich: str) -> KetQuaTimKiem:
    """DFS mở rộng con đầu tiên trước, có tập trạng thái đã xét."""
    ngan_xep = [(bat_dau, [bat_dau])]
    da_duyet = set()
    so_nut_da_duyet = 0

    while ngan_xep:
        nut_hien_tai, duong_di = ngan_xep.pop()
        if nut_hien_tai in da_duyet:
            continue
        da_duyet.add(nut_hien_tai)
        so_nut_da_duyet += 1
        if nut_hien_tai == dich:
            return KetQuaTimKiem("DFS", duong_di, tinh_chi_phi(duong_di), so_nut_da_duyet)
        # Đảo chiều trước khi push để nhánh đầu trong danh sách được xét trước.
        for nut_ke, _ in reversed(DO_THI[nut_hien_tai]):
            if nut_ke not in da_duyet:
                ngan_xep.append((nut_ke, duong_di + [nut_ke]))

    return KetQuaTimKiem("DFS", None, None, so_nut_da_duyet, "Không tìm thấy đường đi")


def tim_kiem_chi_phi_cuc_tieu(bat_dau: str, dich: str) -> KetQuaTimKiem:
    """UCS (Dijkstra): trả đường đi chi phí thấp nhất khi trọng số không âm."""
    thu_tu_vao_hang = count()
    hang_doi_uu_tien = [(0, next(thu_tu_vao_hang), bat_dau, [bat_dau])]
    chi_phi_tot_nhat = {bat_dau: 0}
    so_nut_da_duyet = 0

    while hang_doi_uu_tien:
        chi_phi_hien_tai, _, nut_hien_tai, duong_di = heapq.heappop(hang_doi_uu_tien)
        if chi_phi_hien_tai != chi_phi_tot_nhat.get(nut_hien_tai):
            continue
        so_nut_da_duyet += 1
        if nut_hien_tai == dich:
            return KetQuaTimKiem("UCS", duong_di, chi_phi_hien_tai, so_nut_da_duyet)
        for nut_ke, chi_phi_canh in DO_THI[nut_hien_tai]:
            if chi_phi_canh < 0:
                raise ValueError("UCS yêu cầu chi phí cạnh không âm")
            chi_phi_moi = chi_phi_hien_tai + chi_phi_canh
            if chi_phi_moi < chi_phi_tot_nhat.get(nut_ke, float("inf")):
                chi_phi_tot_nhat[nut_ke] = chi_phi_moi
                heapq.heappush(
                    hang_doi_uu_tien,
                    (chi_phi_moi, next(thu_tu_vao_hang), nut_ke, duong_di + [nut_ke]),
                )

    return KetQuaTimKiem("UCS", None, None, so_nut_da_duyet, "Không tìm thấy đường đi")


def tim_kiem_gioi_han_do_sau(bat_dau: str, dich: str, gioi_han: int) -> KetQuaTimKiem:
    """DLS theo đường đi: tránh vòng lặp trên nhánh, không cắt nhánh khác.

    Giới hạn độ sâu đếm từ nút gốc có độ sâu 0.
    """
    if gioi_han < 0:
        raise ValueError("Giới hạn độ sâu phải >= 0")
    so_nut_da_duyet = 0

    def duyet_sau(nut_hien_tai: str, duong_di: list[str]) -> list[str] | None:
        nonlocal so_nut_da_duyet
        so_nut_da_duyet += 1
        if nut_hien_tai == dich:
            return duong_di
        if len(duong_di) - 1 >= gioi_han:
            return None
        for nut_ke, _ in DO_THI[nut_hien_tai]:
            if nut_ke in duong_di:
                continue
            ket_qua_nhanh = duyet_sau(nut_ke, duong_di + [nut_ke])
            if ket_qua_nhanh is not None:
                return ket_qua_nhanh
        return None

    duong_di = duyet_sau(bat_dau, [bat_dau])
    if duong_di is None:
        return KetQuaTimKiem("DLS", None, None, so_nut_da_duyet, f"Không thấy đích trong độ sâu {gioi_han}")
    return KetQuaTimKiem("DLS", duong_di, tinh_chi_phi(duong_di), so_nut_da_duyet)


def tim_kiem_sau_dan(bat_dau: str, dich: str, do_sau_toi_da: int) -> KetQuaTimKiem:
    """IDS: gọi DLS với giới hạn tăng lần lượt từ 0 đến do_sau_toi_da."""
    if do_sau_toi_da < 0:
        raise ValueError("Độ sâu tối đa phải >= 0")
    tong_so_nut_da_duyet = 0
    for gioi_han in range(do_sau_toi_da + 1):
        ket_qua_dls = tim_kiem_gioi_han_do_sau(bat_dau, dich, gioi_han)
        tong_so_nut_da_duyet += ket_qua_dls.so_nut_da_duyet
        if ket_qua_dls.duong_di is not None:
            return KetQuaTimKiem(
                "IDS", ket_qua_dls.duong_di, ket_qua_dls.chi_phi,
                tong_so_nut_da_duyet, f"Tìm thấy ở độ sâu {gioi_han}",
            )
    return KetQuaTimKiem("IDS", None, None, tong_so_nut_da_duyet, "Đã đạt giới hạn số lần tăng độ sâu")
