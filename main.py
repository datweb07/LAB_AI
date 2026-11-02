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
        print("3. Bài 3: Chạy đủ 7 thuật toán SimpleAI, bảng so sánh và lời giải (không giới hạn thời gian)")
        print("0. Thoát")
        lua_chon = input("Chọn chức năng: ").strip()
        cac_lenh = {
            "1": ["-m", "bai1_tu_cai_dat.chay_bai_1"],
            "2": ["-m", "bai2_vi_du_simpleai.vi_du_chay_nhanh"],
            "3": ["-m", "bai3_8_puzzle.chay_bai_3"],
        }
        if lua_chon == "0":
            print("Kết thúc")
            return
        if lua_chon not in cac_lenh:
            print("Lựa chọn không hợp lệ")
            continue
        with subprocess.Popen([sys.executable, *cac_lenh[lua_chon]]) as tien_trinh:
            while True:
                try:
                    tien_trinh.wait()
                    break
                except KeyboardInterrupt:
                    # Bài 3 tự xử lý Ctrl+C; menu tiếp tục chờ thay vì kill child.
                    continue


if __name__ == "__main__":
    main()
