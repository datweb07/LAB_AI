"""Bài 3: gọi trực tiếp 7 thuật toán SimpleAI, tách tiến trình theo timeout."""
import argparse
import csv
import json
import math
from pathlib import Path
import subprocess
import sys
import time

from .puzzle_core import (
    TRANG_THAI_DAU, TRANG_THAI_DICH, TRANG_THAI_DEMO,
    co_the_giai_duoc, dem_nghich_the, di_chuyen_o_trong,
    h1_so_o_sai_vi_tri, h2_khoang_cach_manhattan,
    hien_thi_ma_tran,
)

TEN_THUAT_TOAN = {
    "bfs": "BFS", "dfs": "DFS", "ucs": "UCS", "dls": "DLS",
    "ids": "IDS", "greedy": "Greedy Best-First", "astar": "A*",
}
CAC_CAU_HINH = (
    ("bfs", "h2"), ("dfs", "h2"), ("ucs", "h2"),
    ("dls", "h2"), ("ids", "h2"), ("greedy", "h1"),
    ("greedy", "h2"), ("astar", "h1"), ("astar", "h2"),
)


def xac_minh_loi_giai(bai_toan, nut_dich) -> tuple[list, int]:
    """Phát lại toàn bộ path của SimpleAI; kiểm tra trạng thái, bước và cost."""
    duong_di = nut_dich.path()
    if not duong_di or duong_di[0] != (None, bai_toan.initial_state):
        raise AssertionError("Đường đi không bắt đầu từ trạng thái ban đầu")
    trang_thai = bai_toan.initial_state
    chi_phi = 0
    for hanh_dong, trang_thai_moi in duong_di[1:]:
        if hanh_dong not in bai_toan.actions(trang_thai):
            raise AssertionError("Đường đi chứa hành động không hợp lệ")
        if bai_toan.result(trang_thai, hanh_dong) != trang_thai_moi:
            raise AssertionError("Trạng thái kế tiếp không khớp result()")
        # Đối chiếu thêm với quy tắc chuyển trạng thái của bài toán.
        if di_chuyen_o_trong(trang_thai, hanh_dong) != trang_thai_moi:
            raise AssertionError("Phép đổi ô trống không khớp")
        chi_phi += bai_toan.cost(trang_thai, hanh_dong, trang_thai_moi)
        trang_thai = trang_thai_moi
    if not bai_toan.is_goal(trang_thai) or nut_dich.state != trang_thai:
        raise AssertionError("Đường đi chưa tới Goal")
    if nut_dich.depth != len(duong_di) - 1 or nut_dich.cost != chi_phi:
        raise AssertionError("Số bước hoặc tổng chi phí không khớp đường đi")
    return duong_di, chi_phi


def chay_thuat_toan_ben_trong(
    ten_thuat_toan: str, heuristic: str, depth_limit: int, demo: bool,
    engine: str = "simpleai",
) -> dict:
    """Không có thuật toán tự viết hoặc fallback; chỉ gọi package đã cài."""
    if engine != "simpleai":
        raise ValueError("Bài 3 chỉ hỗ trợ engine simpleai")
    from simpleai.search import (
        breadth_first, depth_first, uniform_cost, limited_depth_first,
        iterative_limited_depth_first, greedy, astar,
    )
    from .puzzle_problem import BaiToan8Puzzle

    bai_toan = BaiToan8Puzzle(
        TRANG_THAI_DEMO if demo else TRANG_THAI_DAU, heuristic)
    danh_sach_ham = {
        "bfs": breadth_first, "dfs": depth_first, "ucs": uniform_cost,
        "dls": limited_depth_first, "ids": iterative_limited_depth_first,
        "greedy": greedy, "astar": astar,
    }
    # DLS/IDS dùng tree search: closed set của SimpleAI không mở lại một
    # trạng thái gặp ở đường nông hơn, có thể bỏ sót lời giải trong giới hạn.
    tham_so = {"graph_search": ten_thuat_toan not in ("dls", "ids")}
    if ten_thuat_toan == "dls":
        tham_so["depth_limit"] = depth_limit
    bat_dau = time.perf_counter()
    nut_dich = danh_sach_ham[ten_thuat_toan](bai_toan, **tham_so)
    thoi_gian = time.perf_counter() - bat_dau
    ket_qua = {
        "algorithm": ten_thuat_toan, "source": "SimpleAI",
        "heuristic": heuristic if ten_thuat_toan in ("greedy", "astar") else "-",
        "graph_search": tham_so["graph_search"],
        "depth_limit": depth_limit if ten_thuat_toan == "dls" else None,
        "seconds": round(thoi_gian, 6), "steps": None, "cost": None,
    }
    if nut_dich is None:
        ket_qua["status"] = (
            "NO_SOLUTION_WITH_LIMIT" if ten_thuat_toan == "dls" else "NO_SOLUTION")
        return ket_qua
    duong_di, chi_phi = xac_minh_loi_giai(bai_toan, nut_dich)
    cac_hanh_dong = [hanh_dong for hanh_dong, _ in duong_di[1:]]
    ket_qua.update({
        "status": "SOLVED", "steps": len(cac_hanh_dong), "cost": chi_phi,
        "verified": True, "first_moves": cac_hanh_dong[:10],
        "last_moves": cac_hanh_dong[-10:], "all_moves": cac_hanh_dong,
        "states": [list(state) for _, state in duong_di],
    })
    return ket_qua


def chay_co_gioi_han_thoi_gian(
    ten_thuat_toan: str,
    heuristic: str,
    depth_limit: int,
    demo: bool,
    timeout: float,
    engine: str = "simpleai",
) -> dict:
    """subprocess.run kill và wait tiến trình trực tiếp khi hết timeout."""
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
            "heuristic": heuristic if ten_thuat_toan in ("greedy", "astar") else "-",
            "source": "SimpleAI",
            "cost": None,
            "status": "TIMEOUT",
            "steps": None,
            "seconds": round(time.perf_counter() - bat_dau, 3),
        }

    if tien_trinh.returncode != 0:
        return {
            "algorithm": ten_thuat_toan,
            "heuristic": heuristic if ten_thuat_toan in ("greedy", "astar") else "-",
            "source": "SimpleAI",
            "cost": None,
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
            "heuristic": heuristic if ten_thuat_toan in ("greedy", "astar") else "-",
            "source": "SimpleAI",
            "cost": None,
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
    if len(cac_trang_thai) <= 61:
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
    print(f"{'Thuật toán':<21} {'Nguồn':<13} {'Heuristic':<10} {'Trạng thái':<25} {'Số bước':>8} {'Chi phí':>8} {'Giây':>9}")
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
            f"{str(ket_qua.get('cost')) if ket_qua.get('cost') is not None else '-':>8} "
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

    danh_sach_chay = CAC_CAU_HINH if args.all else [(args.algorithm, args.heuristic)]

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
    if args.json:
        duong_dan_json = Path(args.json)
        duong_dan_json.parent.mkdir(parents=True, exist_ok=True)
        duong_dan_json.write_text(
            json.dumps(danh_sach_ket_qua, ensure_ascii=True, indent=2), encoding="utf-8")
    if args.csv:
        duong_dan_csv = Path(args.csv)
        duong_dan_csv.parent.mkdir(parents=True, exist_ok=True)
        with duong_dan_csv.open("w", newline="", encoding="utf-8-sig") as tep:
            cot = ["algorithm", "source", "heuristic", "status", "steps", "cost", "seconds"]
            writer = csv.DictWriter(tep, fieldnames=cot)
            writer.writeheader()
            for ket_qua in danh_sach_ket_qua:
                writer.writerow({ten_cot: ket_qua.get(ten_cot) for ten_cot in cot})
        print(f"\nĐã lưu báo cáo CSV: {duong_dan_csv}")


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Chạy 7 thuật toán cho 8-Puzzle")
    parser.add_argument("che_do", nargs="?", default="run", choices=["run", "_worker"])
    parser.add_argument("--algorithm", choices=list(TEN_THUAT_TOAN), default="astar")
    parser.add_argument("--heuristic", choices=["h1", "h2"], default="h2")
    parser.add_argument("--all", action="store_true", help="Chạy đủ 7 thuật toán với h1/h2")
    parser.add_argument("--demo", action="store_true", help="Ma trận gần đích để trình diễn")
    parser.add_argument("--timeout", type=float, default=30.0, help="Số giây tối đa mỗi thuật toán")
    parser.add_argument("--depth-limit", type=int, default=20, help="Giới hạn độ sâu DLS")
    parser.add_argument("--engine", choices=["simpleai"], default="simpleai",
                        help="Tương thích lệnh cũ; chỉ dùng SimpleAI nguyên bản")
    parser.add_argument("--json", default="", help="Lưu đầy đủ đường đi và kết quả JSON")
    parser.add_argument("--csv", default="", help="Đường dẫn lưu CSV")
    args = parser.parse_args()

    if not math.isfinite(args.timeout) or args.timeout <= 0 or args.depth_limit < 0:
        parser.error("--timeout phải > 0 và --depth-limit phải >= 0")

    if args.che_do == "_worker":
        try:
            ket_qua = chay_thuat_toan_ben_trong(
                args.algorithm, args.heuristic, args.depth_limit, args.demo, args.engine
            )
            print(json.dumps(ket_qua, ensure_ascii=True))
        except ImportError as exc:
            print(f"Thiếu thư viện: {exc}. Chạy python -m pip install -r requirements.txt", file=sys.stderr)
            raise SystemExit(2) from exc
    else:
        chay_bai_tap(args)


if __name__ == "__main__":
    main()
