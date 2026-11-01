"""Chạy: python -m bai1_tu_cai_dat.chay_bai_1"""
import sys
from .do_thi import DO_THI, TRANG_THAI_DAU, TRANG_THAI_DICH
from .thuat_toan import (
    tim_kiem_theo_chieu_rong,
    tim_kiem_theo_chieu_sau,
    tim_kiem_chi_phi_cuc_tieu,
    tim_kiem_gioi_han_do_sau,
    tim_kiem_sau_dan,
)


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    print("\nBÀI 1 - TỰ CÀI ĐẶT 5 THUẬT TOÁN TÌM KIẾM")
    print("Đồ thị có trọng số:")
    for nut_hien_tai, danh_sach_ke in DO_THI.items():
        print(f"  {nut_hien_tai}: {danh_sach_ke}")
    print(f"Bắt đầu: {TRANG_THAI_DAU} | Đích: {TRANG_THAI_DICH}\n")

    danh_sach_ket_qua = [
        tim_kiem_theo_chieu_rong(TRANG_THAI_DAU, TRANG_THAI_DICH),
        tim_kiem_theo_chieu_sau(TRANG_THAI_DAU, TRANG_THAI_DICH),
        tim_kiem_chi_phi_cuc_tieu(TRANG_THAI_DAU, TRANG_THAI_DICH),
        tim_kiem_gioi_han_do_sau(TRANG_THAI_DAU, TRANG_THAI_DICH, gioi_han=4),
        tim_kiem_sau_dan(TRANG_THAI_DAU, TRANG_THAI_DICH, do_sau_toi_da=10),
    ]
    for ket_qua in danh_sach_ket_qua:
        duong_di = " -> ".join(ket_qua.duong_di) if ket_qua.duong_di else "Không có"
        print(f"[{ket_qua.ten_thuat_toan}] Đường đi: {duong_di}")
        print(f"      Chi phí: {ket_qua.chi_phi}, số nút duyệt: {ket_qua.so_nut_da_duyet}")
        if ket_qua.thong_bao:
            print(f"      {ket_qua.thong_bao}")


if __name__ == "__main__":
    main()
