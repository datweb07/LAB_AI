"""BÀI 3 - GIẢI 8-PUZZLE BẰNG 7 THUẬT TOÁN.

Chạy nhanh A* với SimpleAI:
    python -m bai3_8_puzzle.chay_bai_3

Chạy cả 7 thuật toán, với 5 thuật toán cơ bản đã tối ưu:
    python -m bai3_8_puzzle.chay_bai_3 --all

Chạy nguyên bản các thuật toán của thư viện SimpleAI:
    python -m bai3_8_puzzle.chay_bai_3 --all --engine simpleai --timeout 30

Chạy demo bảng gần đích:
    python -m bai3_8_puzzle.chay_bai_3 --all --demo

Chú ý: --engine optimized dùng 5 hàm tìm kiếm tự cài đặt hiệu quả
cho BFS, DFS, UCS, DLS và IDS; Greedy và A* vẫn gọi SimpleAI.
--engine simpleai gọi cả 7 thuật toán từ thư viện nguyên bản.
"""

import argparse
from collections import deque
import csv
import heapq
import json
from pathlib import Path
import subprocess
import sys
import time

from .puzzle_core import (
    TRANG_THAI_DAU,
    TRANG_THAI_DICH,
    TRANG_THAI_DEMO,
    co_the_giai_duoc,
    dem_nghich_the,
    di_chuyen_o_trong,
    h1_so_o_sai_vi_tri,
    h2_khoang_cach_manhattan,
    hien_thi_ma_tran,
    lay_hanh_dong_hop_le,
)

TEN_THUAT_TOAN = {
    "bfs": "BFS",
    "dfs": "DFS",
    "ucs": "UCS",
    "dls": "DLS",
    "ids": "IDS",
    "greedy": "Greedy Best-First",
    "astar": "A*",
}
CAC_THUAT_TOAN_CO_BAN = {"bfs", "dfs", "ucs", "dls", "ids"}


def tim_lai_duong_di(cha: dict, trang_thai_dich: tuple[int, ...]) -> list[str]:
    """Khôi phục danh sách hành động dựa vào bảng cha."""
    danh_sach_hanh_dong = []
    trang_thai = trang_thai_dich

    while cha[trang_thai][0] is not None:
        trang_thai_truoc, hanh_dong = cha[trang_thai]
        danh_sach_hanh_dong.append(hanh_dong)
        trang_thai = trang_thai_truoc

    danh_sach_hanh_dong.reverse()
    return danh_sach_hanh_dong


def tim_kiem_bfs_hoac_dfs(trang_thai_dau: tuple[int, ...], dung_bfs: bool) -> list[str] | None:
    """BFS dùng FIFO; DFS dùng LIFO; tập đã thấy được kiểm tra O(1) trung bình."""
    fringe = deque([trang_thai_dau]) if dung_bfs else [trang_thai_dau]
    da_thay = {trang_thai_dau}
    cha = {trang_thai_dau: (None, None)}

    while fringe:
        trang_thai = fringe.popleft() if dung_bfs else fringe.pop()
        if trang_thai == TRANG_THAI_DICH:
            return tim_lai_duong_di(cha, trang_thai)

        hanh_dong_hop_le = lay_hanh_dong_hop_le(trang_thai)
        for hanh_dong in hanh_dong_hop_le:
            trang_thai_moi = di_chuyen_o_trong(trang_thai, hanh_dong)
            if trang_thai_moi in da_thay:
                continue
            da_thay.add(trang_thai_moi)
            cha[trang_thai_moi] = (trang_thai, hanh_dong)
            fringe.append(trang_thai_moi)

    return None


def tim_kiem_ucs(trang_thai_dau: tuple[int, ...]) -> list[str] | None:
    """Uniform-Cost Search với hàng đợi ưu tiên và chi phí tốt nhất."""
    hang_doi_uu_tien = [(0, 0, trang_thai_dau)]
    chi_phi_tot_nhat = {trang_thai_dau: 0}
    cha = {trang_thai_dau: (None, None)}
    thu_tu = 0

    while hang_doi_uu_tien:
        chi_phi, _, trang_thai = heapq.heappop(hang_doi_uu_tien)
        if chi_phi != chi_phi_tot_nhat[trang_thai]:
            continue
        if trang_thai == TRANG_THAI_DICH:
            return tim_lai_duong_di(cha, trang_thai)

        for hanh_dong in lay_hanh_dong_hop_le(trang_thai):
            trang_thai_moi = di_chuyen_o_trong(trang_thai, hanh_dong)
            chi_phi_moi = chi_phi + 1
            if chi_phi_moi >= chi_phi_tot_nhat.get(trang_thai_moi, float("inf")):
                continue
            chi_phi_tot_nhat[trang_thai_moi] = chi_phi_moi
            cha[trang_thai_moi] = (trang_thai, hanh_dong)
            thu_tu += 1
            heapq.heappush(hang_doi_uu_tien, (chi_phi_moi, thu_tu, trang_thai_moi))

    return None


def tim_kiem_dls(trang_thai_dau: tuple[int, ...], gioi_han_do_sau: int) -> list[str] | None:
    """Depth-Limited Search, tránh mở lại trạng thái ở độ sâu không tốt hơn.

    Bảng độ sâu tốt nhất được tạo mới ở mỗi lượt tìm kiếm, nên IDS không
    dùng nhầm trạng thái đã xét ở vòng giới hạn độ sâu trước đó.
    """
    do_sau_tot_nhat: dict[tuple[int, ...], int] = {}
    duong_di_hien_tai: list[str] = []

    def duyet(trang_thai: tuple[int, ...], do_sau: int) -> bool:
        if trang_thai == TRANG_THAI_DICH:
            return True
        if do_sau >= gioi_han_do_sau:
            return False
        if do_sau >= do_sau_tot_nhat.get(trang_thai, float("inf")):
            return False

        do_sau_tot_nhat[trang_thai] = do_sau
        for hanh_dong in reversed(lay_hanh_dong_hop_le(trang_thai)):
            trang_thai_moi = di_chuyen_o_trong(trang_thai, hanh_dong)
            duong_di_hien_tai.append(hanh_dong)
            if duyet(trang_thai_moi, do_sau + 1):
                return True
            duong_di_hien_tai.pop()
        return False

    if duyet(trang_thai_dau, 0):
        return duong_di_hien_tai.copy()
    return None


def tim_kiem_ids(trang_thai_dau: tuple[int, ...], do_sau_toi_da: int = 31) -> list[str] | None:
    """Iterative Deepening: lần lượt chạy DLS với mức 0, 1, 2, ..."""
    for gioi_han in range(do_sau_toi_da + 1):
        duong_di = tim_kiem_dls(trang_thai_dau, gioi_han)
        if duong_di is not None:
            return duong_di
    return None


def chay_thuat_toan_ben_trong(
    ten_thuat_toan: str,
    heuristic: str,
    depth_limit: int,
    demo: bool,
    engine: str,
) -> dict:
    """Thực hiện thuật toán trong tiến trình con để có thể giới hạn thời gian."""
    trang_thai_dau = TRANG_THAI_DEMO if demo else TRANG_THAI_DAU
    su_dung_ham_toi_uu = engine == "optimized" and ten_thuat_toan in CAC_THUAT_TOAN_CO_BAN

    bat_dau_dem = time.perf_counter()
    if su_dung_ham_toi_uu:
        if ten_thuat_toan == "bfs":
            danh_sach_hanh_dong = tim_kiem_bfs_hoac_dfs(trang_thai_dau, dung_bfs=True)
        elif ten_thuat_toan == "dfs":
            danh_sach_hanh_dong = tim_kiem_bfs_hoac_dfs(trang_thai_dau, dung_bfs=False)
        elif ten_thuat_toan == "ucs":
            danh_sach_hanh_dong = tim_kiem_ucs(trang_thai_dau)
        elif ten_thuat_toan == "dls":
            danh_sach_hanh_dong = tim_kiem_dls(trang_thai_dau, depth_limit)
        else:
            danh_sach_hanh_dong = tim_kiem_ids(trang_thai_dau)
        nguon_thuat_toan = "Tự tối ưu"
    else:
        from simpleai.search import (
            astar,
            breadth_first,
            depth_first,
            greedy,
            iterative_limited_depth_first,
            limited_depth_first,
            uniform_cost,
        )
        from .puzzle_problem import BaiToan8Puzzle

        bai_toan = BaiToan8Puzzle(initial_state=trang_thai_dau, loai_heuristic=heuristic)
        danh_sach_ham = {
            "bfs": breadth_first,
            "dfs": depth_first,
            "ucs": uniform_cost,
            "dls": limited_depth_first,
            "ids": iterative_limited_depth_first,
            "greedy": greedy,
            "astar": astar,
        }
        su_dung_graph_search = ten_thuat_toan not in ("dls", "ids")
        tham_so = {"graph_search": su_dung_graph_search}
        if ten_thuat_toan == "dls":
            tham_so["depth_limit"] = depth_limit

        nut_dich = danh_sach_ham[ten_thuat_toan](bai_toan, **tham_so)
        danh_sach_hanh_dong = (
            [hanh_dong for hanh_dong, _ in nut_dich.path()[1:]]
            if nut_dich is not None else None
        )
        nguon_thuat_toan = "SimpleAI"

    thoi_gian = round(time.perf_counter() - bat_dau_dem, 6)
    if danh_sach_hanh_dong is None:
        return {
            "algorithm": ten_thuat_toan,
            "heuristic": heuristic,
            "source": nguon_thuat_toan,
            "status": "NO_SOLUTION_WITH_LIMIT",
            "steps": None,
            "seconds": thoi_gian,
        }

    # Kiểm chứng độc lập tính hợp lệ của mọi bước di chuyển.
    trang_thai = trang_thai_dau
    danh_sach_trang_thai = [list(trang_thai)] if len(danh_sach_hanh_dong) <= 60 else []
    for hanh_dong in danh_sach_hanh_dong:
        trang_thai = di_chuyen_o_trong(trang_thai, hanh_dong)
        if danh_sach_trang_thai:
            danh_sach_trang_thai.append(list(trang_thai))
    if trang_thai != TRANG_THAI_DICH:
        raise AssertionError("Đường đi tìm được không tới trạng thái đích")

    return {
        "algorithm": ten_thuat_toan,
        "heuristic": heuristic,
        "source": nguon_thuat_toan,
        "status": "SOLVED",
        "seconds": thoi_gian,
        "steps": len(danh_sach_hanh_dong),
        "first_moves": danh_sach_hanh_dong[:10],
        "last_moves": danh_sach_hanh_dong[-10:],
        "all_moves": danh_sach_hanh_dong if len(danh_sach_hanh_dong) <= 60 else [],
        "states": danh_sach_trang_thai,
    }


def chay_co_gioi_han_thoi_gian(
    ten_thuat_toan: str,
    heuristic: str,
    depth_limit: int,
    demo: bool,
    timeout: float,
    engine: str,
) -> dict:
    lenh = [
        sys.executable, "-m", "bai3_8_puzzle.chay_bai_3", "_worker",
        "--algorithm", ten_thuat_toan,
        "--heuristic", heuristic,
        "--depth-limit", str(depth_limit),
        "--engine", engine,
    ]
    if demo:
        lenh.append("--demo")

    bat_dau = time.perf_counter()
    try:
        tien_trinh = subprocess.run(
            lenh,
            cwd=Path(__file__).resolve().parents[1],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return {
            "algorithm": ten_thuat_toan,
            "heuristic": heuristic,
            "status": "TIMEOUT",
            "steps": None,
            "seconds": round(time.perf_counter() - bat_dau, 3),
        }

    if tien_trinh.returncode != 0:
        return {
            "algorithm": ten_thuat_toan,
            "heuristic": heuristic,
            "status": "ERROR",
            "steps": None,
            "seconds": round(time.perf_counter() - bat_dau, 3),
            "error": (tien_trinh.stderr or tien_trinh.stdout)[-800:],
        }
    try:
        return json.loads(tien_trinh.stdout)
    except json.JSONDecodeError:
        return {
            "algorithm": ten_thuat_toan,
            "heuristic": heuristic,
            "status": "ERROR",
            "steps": None,
            "seconds": round(time.perf_counter() - bat_dau, 3),
            "error": "Phản hồi không phải JSON: " + tien_trinh.stdout[-300:],
        }


def in_duong_di_chi_tiet(ket_qua: dict) -> None:
    if ket_qua.get("status") != "SOLVED":
        return
    cac_trang_thai = ket_qua.get("states", [])
    cac_hanh_dong = ket_qua.get("all_moves", [])
    if cac_trang_thai:
        print("\nQUÁ TRÌNH DI CHUYỂN (0 LÀ Ô TRỐNG)")
        for so_buoc, trang_thai in enumerate(cac_trang_thai):
            mo_ta = "Bắt đầu" if so_buoc == 0 else f"Bước {so_buoc}: {cac_hanh_dong[so_buoc-1]}"
            print(f"\n{mo_ta}\n{hien_thi_ma_tran(tuple(trang_thai))}")
    else:
        print("Đường đi dài, chỉ in 10 bước đầu/cuối để tránh tràn console:")
        print("Đầu:", ket_qua.get("first_moves", []))
        print("Cuối:", ket_qua.get("last_moves", []))


def hien_thi_bang_so_sanh(danh_sach_ket_qua: list[dict]) -> None:
    print("\nBẢNG SO SÁNH KẾT QUẢ")
    print(f"{'Thuật toán':<21} {'Nguồn':<13} {'Heuristic':<10} {'Trạng thái':<25} {'Số bước':>8} {'Giây':>9}")
    print("-" * 99)
    for ket_qua in danh_sach_ket_qua:
        so_buoc = str(ket_qua.get("steps")) if ket_qua.get("steps") is not None else "-"
        heuristic = ket_qua["heuristic"] if ket_qua["algorithm"] in ("astar", "greedy") else "-"
        print(
            f"{TEN_THUAT_TOAN[ket_qua['algorithm']]:<21} "
            f"{ket_qua.get('source', '-'):<13} "
            f"{heuristic:<10} "
            f"{ket_qua['status']:<25} "
            f"{so_buoc:>8} "
            f"{ket_qua.get('seconds', 0):>9.3f}"
        )
        if ket_qua.get("error"):
            print("  Lỗi:", ket_qua["error"])
    print("\nTIMEOUT = quá giới hạn thời gian, không đồng nghĩa bài toán vô nghiệm.")
    print("DLS trả None nếu không tìm thấy đích trong giới hạn độ sâu.")
    print("Thời gian có thể khác nhau tùy máy tính.")


def chay_bai_tap(args: argparse.Namespace) -> None:
    trang_thai_dau = TRANG_THAI_DEMO if args.demo else TRANG_THAI_DAU
    print("\nBÀI 3 - 8-PUZZLE VỚI 7 THUẬT TOÁN")
    if args.engine == "optimized":
        print("Chế độ: 5 thuật toán cơ bản tự tối ưu + Greedy/A* từ SimpleAI")
    else:
        print("Chế độ: tất cả thuật toán gọi SimpleAI nguyên bản")
    print("Trạng thái ban đầu:\n" + hien_thi_ma_tran(trang_thai_dau))
    print("\nTrạng thái đích:\n" + hien_thi_ma_tran(TRANG_THAI_DICH))
    print(f"\nSố nghịch thế đầu/đích: {dem_nghich_the(trang_thai_dau)} / {dem_nghich_the(TRANG_THAI_DICH)}")
    print(f"Có thể giải: {co_the_giai_duoc(trang_thai_dau, TRANG_THAI_DICH)}")
    print(f"h1 (số ô sai vị trí): {h1_so_o_sai_vi_tri(trang_thai_dau)}")
    print(f"h2 (tổng Manhattan): {h2_khoang_cach_manhattan(trang_thai_dau)}")
    if not co_the_giai_duoc(trang_thai_dau, TRANG_THAI_DICH):
        print("Không chạy tìm kiếm: bài toán không có lời giải do parity nghịch thế.")
        return

    danh_sach_chay = [
        ("bfs", "h2"), ("dfs", "h2"), ("ucs", "h2"),
        ("dls", "h2"), ("ids", "h2"),
        ("greedy", "h1"), ("greedy", "h2"),
        ("astar", "h1"), ("astar", "h2"),
    ] if args.all else [(args.algorithm, args.heuristic)]

    danh_sach_ket_qua = []
    for ten_thuat_toan, heuristic in danh_sach_chay:
        ten_hien_thi = TEN_THUAT_TOAN[ten_thuat_toan]
        dung_h = heuristic if ten_thuat_toan in ("astar", "greedy") else "không dùng h"
        print(f"\nĐang chạy: {ten_hien_thi} ({dung_h})...", flush=True)
        ket_qua = chay_co_gioi_han_thoi_gian(
            ten_thuat_toan, heuristic, args.depth_limit,
            args.demo, args.timeout, args.engine,
        )
        danh_sach_ket_qua.append(ket_qua)
        print(f"  -> {ket_qua['status']}, số bước = {ket_qua.get('steps')}, "
              f"thời gian = {ket_qua.get('seconds')} giây")

    hien_thi_bang_so_sanh(danh_sach_ket_qua)
    if not args.all:
        in_duong_di_chi_tiet(danh_sach_ket_qua[0])
    if args.csv:
        duong_dan_csv = Path(args.csv)
        duong_dan_csv.parent.mkdir(parents=True, exist_ok=True)
        with duong_dan_csv.open("w", newline="", encoding="utf-8-sig") as tep:
            cot = ["algorithm", "source", "heuristic", "status", "steps", "seconds"]
            writer = csv.DictWriter(tep, fieldnames=cot)
            writer.writeheader()
            for ket_qua in danh_sach_ket_qua:
                writer.writerow({ten_cot: ket_qua.get(ten_cot) for ten_cot in cot})
        print(f"\nĐã lưu báo cáo CSV: {duong_dan_csv}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Chạy 7 thuật toán cho 8-Puzzle")
    parser.add_argument("che_do", nargs="?", default="run", choices=["run", "_worker"])
    parser.add_argument("--algorithm", choices=list(TEN_THUAT_TOAN), default="astar")
    parser.add_argument("--heuristic", choices=["h1", "h2"], default="h2")
    parser.add_argument("--all", action="store_true", help="Chạy đủ 7 thuật toán với h1/h2")
    parser.add_argument("--demo", action="store_true", help="Ma trận gần đích để trình diễn")
    parser.add_argument("--timeout", type=float, default=5.0, help="Số giây tối đa mỗi thuật toán")
    parser.add_argument("--depth-limit", type=int, default=20, help="Giới hạn độ sâu DLS")
    parser.add_argument("--engine", choices=["optimized", "simpleai"], default="optimized",
                        help="optimized: tự tối ưu 5 thuật toán cơ bản; simpleai: gọi nguyên bản cả 7")
    parser.add_argument("--csv", default="", help="Đường dẫn lưu CSV")
    args = parser.parse_args()

    if args.timeout <= 0 or args.depth_limit < 0:
        parser.error("--timeout phải > 0 và --depth-limit phải >= 0")

    if args.che_do == "_worker":
        try:
            ket_qua = chay_thuat_toan_ben_trong(
                args.algorithm, args.heuristic, args.depth_limit, args.demo, args.engine
            )
            print(json.dumps(ket_qua, ensure_ascii=False))
        except ImportError as exc:
            print(f"Thiếu thư viện: {exc}. Chạy python -m pip install -r requirements.txt", file=sys.stderr)
            raise SystemExit(2) from exc
    else:
        chay_bai_tap(args)


if __name__ == "__main__":
    main()
