"""Menu điều khiển 3 bài. Chạy bằng `python main.py` từ thư mục dự án."""
import subprocess
import sys


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    while True:
        print("\n" + "=" * 67)
        print("BÀI TẬP TRÍ TUỆ NHÂN TẠO - SIMPLEAI - CHƯƠNG 3 & 4")
        print("1. Bài 1: Tự cài đặt 5 thuật toán BFS, DFS, UCS, DLS, IDS")
        print("2. Bài 2: Chạy ví dụ SimpleAI gọn (HELLO rút còn AI)")
        print("3. Bài 3: Giải 8-Puzzle theo bảng bằng A* (h2), in từng bước")
        print("4. Bài 3: Thử toàn bộ 7 thuật toán SimpleAI (giới hạn 30s/lần)")
        print("5. Bài 3: Thử toàn bộ 7 thuật toán với trạng thái demo 1 bước")
        print("0. Thoát")
        lua_chon = input("Chọn chức năng: ").strip()
        cac_lenh = {
            "1": ["-m", "bai1_tu_cai_dat.chay_bai_1"],
            "2": ["-m", "bai2_vi_du_simpleai.vi_du_chay_nhanh"],
            "3": ["-m", "bai3_8_puzzle.chay_bai_3"],
            "4": ["-m", "bai3_8_puzzle.chay_bai_3", "--all"],
            "5": ["-m", "bai3_8_puzzle.chay_bai_3", "--all", "--demo"],
        }
        if lua_chon == "0":
            print("Kết thúc")
            return
        if lua_chon not in cac_lenh:
            print("Lựa chọn không hợp lệ")
            continue
        subprocess.run([sys.executable, *cac_lenh[lua_chon]], check=False)


if __name__ == "__main__":
    main()
