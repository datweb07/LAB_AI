"""Bài 3: chạy đủ 7 thuật toán SimpleAI, không giới hạn thời gian."""
import argparse
import csv
import json
from pathlib import Path
import sys
import time
import traceback

from .puzzle_core import (
    TRANG_THAI_DAU, TRANG_THAI_DICH,
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
    ("greedy", "h1"),
    ("greedy", "h2"), ("astar", "h1"), ("astar", "h2"),
    # Chạy hai lượt tree search có nhiều nhánh lặp sau các lượt còn lại.
    ("dls", "h2"), ("ids", "h2"),
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


def chay_thuat_toan(
    ten_thuat_toan: str, heuristic: str, depth_limit: int,
    trang_thai_dau: tuple[int, ...] = TRANG_THAI_DAU,
) -> dict:
    """Không có thuật toán tự viết hoặc fallback; chỉ gọi package đã cài."""
    from simpleai.search import (
        breadth_first, depth_first, uniform_cost, limited_depth_first,
        iterative_limited_depth_first, greedy, astar,
    )
    from .puzzle_problem import BaiToan8Puzzle

    bai_toan = BaiToan8Puzzle(
        trang_thai_dau, heuristic)
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
    ket_qua = {
        "algorithm": ten_thuat_toan, "source": "SimpleAI",
        "heuristic": heuristic if ten_thuat_toan in ("greedy", "astar") else "-",
        "graph_search": tham_so["graph_search"],
        "depth_limit": depth_limit if ten_thuat_toan == "dls" else None,
        "steps": None, "cost": None,
    }
    bat_dau = time.perf_counter()
    try:
        nut_dich = danh_sach_ham[ten_thuat_toan](bai_toan, **tham_so)
    except (KeyboardInterrupt, Exception) as exc:
        ket_qua["status"] = "INTERRUPTED" if isinstance(exc, KeyboardInterrupt) else "ERROR"
        if not isinstance(exc, KeyboardInterrupt):
            ket_qua["error"] = traceback.format_exc()
    # Chụp số liệu trước khi phát lại lời giải để không đếm lẫn phần kiểm chứng.
    ket_qua.update({
        "seconds": round(time.perf_counter() - bat_dau, 6),
        "expanded": bai_toan.expanded,
        "generated": bai_toan.generated,
        "goal_tests": bai_toan.goal_tests,
    })
    if "status" in ket_qua:
        return ket_qua
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


def hien_thi_bang_so_sanh(danh_sach_ket_qua: list[dict]) -> None:
    print("\nBẢNG SO SÁNH KẾT QUẢ")
    print(f"{'Thuật toán':<21} {'Nguồn':<13} {'Heuristic':<10} {'Trạng thái':<25} {'Bước lời giải':>13} {'Chi phí':>8} {'Expanded':>12} {'Generated':>12} {'Giây':>9}")
    print("-" * 132)
    for ket_qua in danh_sach_ket_qua:
        so_buoc = str(ket_qua.get("steps")) if ket_qua.get("steps") is not None else "-"
        heuristic = ket_qua["heuristic"] if ket_qua["algorithm"] in ("astar", "greedy") else "-"
        ten_hien_thi = TEN_THUAT_TOAN[ket_qua['algorithm']]
        if ket_qua['algorithm'] == 'dls':
            ten_hien_thi += f" (l={ket_qua.get('depth_limit', '?')})"
        print(
            f"{ten_hien_thi:<21} "
            f"{ket_qua.get('source', '-'):<13} "
            f"{heuristic:<10} "
            f"{ket_qua['status']:<25} "
            f"{so_buoc:>13} "
            f"{str(ket_qua.get('cost')) if ket_qua.get('cost') is not None else '-':>8} "
            f"{str(ket_qua.get('expanded', '-')):>12} "
            f"{str(ket_qua.get('generated', '-')):>12} "
            f"{ket_qua.get('seconds', 0):>9.3f}"
        )


def chay_bai_tap(args: argparse.Namespace) -> None:
    trang_thai_dau = TRANG_THAI_DAU
    print("\nBÀI 3 - 8-PUZZLE VỚI 7 THUẬT TOÁN")
    print("Chạy đủ 7 thuật toán SimpleAI / 9 cấu hình, không giới hạn thời gian.")
    print("Ctrl+C bỏ qua lượt đang chạy (INTERRUPTED); không đồng nghĩa vô nghiệm.")
    print("Bước lời giải = độ dài đường đi; Expanded/Generated = số lần mở rộng/sinh nút.")
    print("Số đếm IDS cộng dồn qua các lượt độ sâu, không tính phần kiểm chứng.")
    print(f"DLS giới hạn độ sâu {args.depth_limit}; IDS thử lại DLS từ 0 và tự tăng độ sâu.")
    print("Trạng thái ban đầu:\n" + hien_thi_ma_tran(trang_thai_dau))
    print("\nTrạng thái đích:\n" + hien_thi_ma_tran(TRANG_THAI_DICH))
    print(f"\nSố nghịch thế đầu/đích: {dem_nghich_the(trang_thai_dau)} / {dem_nghich_the(TRANG_THAI_DICH)}")
    print(f"Có thể giải: {co_the_giai_duoc(trang_thai_dau, TRANG_THAI_DICH)}")
    print(f"h1 (số ô sai vị trí): {h1_so_o_sai_vi_tri(trang_thai_dau)}")
    print(f"h2 (tổng Manhattan): {h2_khoang_cach_manhattan(trang_thai_dau)}")
    if not co_the_giai_duoc(trang_thai_dau, TRANG_THAI_DICH):
        print("Không chạy tìm kiếm: bài toán không có lời giải do parity nghịch thế.")
        return

    danh_sach_ket_qua = []
    for ten_thuat_toan, heuristic in CAC_CAU_HINH:
        ten_hien_thi = TEN_THUAT_TOAN[ten_thuat_toan]
        dung_h = heuristic if ten_thuat_toan in ("astar", "greedy") else "không dùng h"
        print(f"\nĐang chạy: {ten_hien_thi} ({dung_h})...", flush=True)
        bat_dau = time.perf_counter()
        try:
            ket_qua = chay_thuat_toan(
                ten_thuat_toan, heuristic, args.depth_limit, trang_thai_dau)
        except (KeyboardInterrupt, Exception) as exc:
            ket_qua = {
                "algorithm": ten_thuat_toan, "source": "SimpleAI",
                "heuristic": heuristic if ten_thuat_toan in ("astar", "greedy") else "-",
                "status": "INTERRUPTED" if isinstance(exc, KeyboardInterrupt) else "ERROR",
                "steps": None, "cost": None,
                "seconds": round(time.perf_counter() - bat_dau, 6),
            }
            if not isinstance(exc, KeyboardInterrupt):
                ket_qua["error"] = traceback.format_exc()
        danh_sach_ket_qua.append(ket_qua)
        # Mỗi lượt chỉ in bảng mới nhất, không in các trạng thái trên đường đi.
        hien_thi_bang_so_sanh(danh_sach_ket_qua)
        if ket_qua.get("error"):
            print("Lỗi:", ket_qua["error"])

    if args.json:
        duong_dan_json = Path(args.json)
        duong_dan_json.parent.mkdir(parents=True, exist_ok=True)
        duong_dan_json.write_text(
            json.dumps(danh_sach_ket_qua, ensure_ascii=True, indent=2), encoding="utf-8")
    if args.csv:
        duong_dan_csv = Path(args.csv)
        duong_dan_csv.parent.mkdir(parents=True, exist_ok=True)
        with duong_dan_csv.open("w", newline="", encoding="utf-8-sig") as tep:
            cot = ["algorithm", "source", "heuristic", "status", "steps", "cost", "expanded", "generated", "goal_tests", "seconds"]
            writer = csv.DictWriter(tep, fieldnames=cot)
            writer.writeheader()
            for ket_qua in danh_sach_ket_qua:
                writer.writerow({ten_cot: ket_qua.get(ten_cot) for ten_cot in cot})
        print(f"\nĐã lưu báo cáo CSV: {duong_dan_csv}")


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(
        description="Chạy đủ 7 thuật toán SimpleAI, không giới hạn thời gian")
    parser.add_argument("--depth-limit", type=int, default=20, help="Giới hạn độ sâu DLS (không phải thời gian)")
    parser.add_argument("--json", default="", help="Lưu đầy đủ kết quả và đường đi JSON")
    parser.add_argument("--csv", default="", help="Lưu bảng so sánh CSV")
    args = parser.parse_args()
    if args.depth_limit < 0:
        parser.error("--depth-limit phải >= 0")
    chay_bai_tap(args)


if __name__ == "__main__":
    main()
