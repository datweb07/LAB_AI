# Bài tập Trí tuệ nhân tạo

| Bài | Nội dung                                                 | Thư mục                |
| --- | -------------------------------------------------------- | ---------------------- |
| 1   | Tự cài BFS, DFS, UCS, DLS, IDS theo slide Chương 3       | `bai1_tu_cai_dat/`     |
| 2   | Sử dụng example và thuật toán có sẵn của SimpleAI        | `bai2_vi_du_simpleai/` |
| 3   | Giải 8-Puzzle bằng 7 thuật toán SimpleAI, có riêng h1/h2 | `bai3_8_puzzle/`       |

## Cài đặt

Cần **Python 3.10+**. Mở PowerShell, Git Bash hoặc terminal VS Code tại thư mục chứa `main.py`:

```powershell
python -m pip install -r requirements.txt
python main.py
```

## Chạy từng bài

```powershell
# Bài 1: năm thuật toán tự viết trên đồ thị có trọng số
python -m bai1_tu_cai_dat.chay_bai_1

# Bài 2: ví dụ HELLO WORLD theo tài liệu SimpleAI
python -m bai2_vi_du_simpleai.vi_du_goc_tai_lieu

# Bài 2: biến thể AI để trình diễn ngắn gọn bằng BFS và A*
python -m bai2_vi_du_simpleai.vi_du_chay_nhanh

# Bài 3: cả 7 thuật toán và bảng so sánh, không giới hạn thời gian
python -m bai3_8_puzzle.chay_bai_3
```

## Bài 3 - Dữ liệu và tùy chọn

`0` là ô trống:

```text
Initial State       Goal State
2 1 0               1 2 3
3 4 5               8 0 4
7 8 6               7 6 5
```

Ma trận nguồn khai báo hai chiều; nội bộ chuyển sang tuple bất biến để dùng với SimpleAI. h1 của Initial = **7**, h2 = **10**. Cả hai bằng 0 tại Goal.

```powershell
# Một luồng duy nhất: chạy 7 thuật toán / 9 cấu hình trên ma trận của giảng viên
python -m bai3_8_puzzle.chay_bai_3

# DLS vẫn cần giới hạn độ sâu; đây không phải giới hạn thời gian
python -m bai3_8_puzzle.chay_bai_3 --depth-limit 20

# Chỉ tạo file khi chủ động yêu cầu
python -m bai3_8_puzzle.chay_bai_3 --csv ket_qua.csv --json duong_di.json
```

Menu `python main.py` chỉ có một lựa chọn Bài 3 (mục 3). Không còn chế độ A* riêng, demo hoặc tham số `--all`, `--algorithm`, `--heuristic`, `--engine`, `--timeout`.

Cả 7 thuật toán đều gọi trực tiếp SimpleAI. Greedy và A* chạy riêng với h1/h2, tổng cộng 9 lượt. Thứ tự: BFS, DFS, UCS, Greedy–h1/h2, A*–h1/h2, DLS, IDS. Hai lượt tree search DLS/IDS được đặt cuối để không chặn hiển thị kết quả của các thuật toán còn lại. Không giới hạn thời gian; thuật toán chạy đến khi trả kết quả hoặc người dùng nhấn **Ctrl+C** để dừng lượt hiện tại và chuyển sang lượt tiếp theo. Lượt bị dừng được ghi `INTERRUPTED`, không được xem là đã giải được hay vô nghiệm.

Chương trình chỉ in thông tin đầu vào trước khi chạy, tên cấu hình đang chạy và bảng so sánh cập nhật sau mỗi lượt. Bảng sau lượt cuối là bảng đủ 9 cấu hình, không in lặp lại. Không in các bước di chuyển hoặc tóm tắt đường đi. Lời giải vẫn được kiểm chứng bên trong; lời giải tối ưu của đề chính là 20 bước, DFS/Greedy không đảm bảo tối ưu.

Bảng gồm thuật toán, nguồn, heuristic, trạng thái, bước lời giải, chi phí, Expanded, Generated và thời gian:

- `SOLVED`: đường đi, Goal, số bước và chi phí đã được kiểm tra.
- `INTERRUPTED`: người dùng chủ động dừng lượt đang chạy bằng Ctrl+C.
- `NO_SOLUTION_WITH_LIMIT`: DLS không tìm được đích trong giới hạn độ sâu.
- `NO_SOLUTION`: tìm kiếm kết thúc mà không có lời giải.
- `ERROR`: hiển thị traceback để xác định lỗi và tiếp tục cấu hình tiếp theo.

BFS/UCS có thể mất nhiều phút; DLS/IDS tree search có thể lâu hơn rất nhiều vì duyệt các nhánh lặp. Không có cam kết tất cả lượt sẽ hoàn thành nhanh. Chương trình không thay thuật toán hoặc thay trạng thái đầu để tăng tốc.

Nếu cần xem đường đi ngoài console, dùng `--json` để lưu toàn bộ trạng thái và hành động. CSV dùng UTF-8 BOM. Chạy mặc định không tạo file kết quả. Không còn tùy chọn `--full-path`.

## Hiểu đúng thời gian và số bước

**Bước lời giải** là số hành động trên đường đi cuối cùng, không phải số nút thuật toán đã duyệt. BFS có thể mở rộng hàng chục nghìn nút để tìm đường tối ưu 20 bước; DFS có thể tìm một đường hàng nghìn bước nhanh hơn vì thứ tự duyệt và frontier khác nhau. Không suy ra thời gian chạy từ độ dài lời giải.

- `Expanded`: số lần gọi `actions` khi thư viện mở rộng nút; không phải số trạng thái khác nhau.
- `Generated`: số lần `result` tạo trạng thái con, gồm cả trạng thái bị thư viện loại do trùng; không tính gốc.
- JSON/CSV có thêm `goal_tests`: số lần thư viện kiểm tra đích.
- IDS cộng dồn các lần đếm qua tất cả lượt DLS, kể cả trạng thái bị xét lặp. Lượt bị Ctrl+C vẫn giữ các số đếm đã thu được.
- Các số liệu và thời gian tìm kiếm được chụp trước khi kiểm chứng/in đường đi, nên không tính phần phát lại lời giải.

DLS ở giới hạn 6 hoặc IDS bị dừng ở độ sâu 8 không thể giải đề có khoảng cách tối ưu 20; kết quả không tìm thấy ở giới hạn thấp không so trực tiếp với một lượt tìm đến độ sâu 20. IDS nguyên bản SimpleAI không nhận tham số giới hạn độ sâu tối đa.

Các tối ưu trong `puzzle_core.py` chỉ tính trước hành động hợp lệ theo 9 vị trí ô trống và khoảng cách Manhattan. Không lọc bước quay lui, không thay thứ tự hành động, không sửa frontier hoặc thuật toán SimpleAI. Vì vậy DLS/IDS tree search vẫn có thể rất chậm; không cam kết hoàn thành nhanh chỉ nhờ các tối ưu này.
