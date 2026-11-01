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

# Bài 3: mặc định A* + h2, in từng bước của lời giải
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
# Cả 7 thuật toán, tổng 9 cấu hình do Greedy/A* có riêng h1 và h2
python -m bai3_8_puzzle.chay_bai_3 --all

# Giới hạn thời gian riêng cho từng cấu hình (mặc định 30 giây)
python -m bai3_8_puzzle.chay_bai_3 --all --timeout 60

# Demo: trạng thái đầu cách Goal một bước, không thay thế dữ liệu đề chính
python -m bai3_8_puzzle.chay_bai_3 --all --demo

# Chọn thuật toán và heuristic
python -m bai3_8_puzzle.chay_bai_3 --algorithm astar --heuristic h1
python -m bai3_8_puzzle.chay_bai_3 --algorithm dls --depth-limit 20 --timeout 30

# Chỉ tạo file kết quả khi chủ động yêu cầu
python -m bai3_8_puzzle.chay_bai_3 --all --csv ket_qua.csv
python -m bai3_8_puzzle.chay_bai_3 --json duong_di.json
```

Demo có Initial `1 2 3 / 8 4 0 / 7 6 5`, giữ nguyên Goal của đề. `--algorithm` nhận `bfs`, `dfs`, `ucs`, `dls`, `ids`, `greedy`, `astar`. `--depth-limit` chỉ áp dụng DLS; IDS của SimpleAI tự tăng độ sâu. `--engine simpleai` được giữ tương thích lệnh cũ; tất cả lượt chạy luôn dùng SimpleAI.

Bảng hiển thị thuật toán, nguồn, heuristic, trạng thái, số bước, chi phí và thời gian:

- `SOLVED`: đã kiểm tra đường đi tới đúng Goal, số bước và chi phí.
- `TIMEOUT`: chưa hoàn thành trong thời gian cấp; không có nghĩa vô nghiệm.
- `NO_SOLUTION_WITH_LIMIT`: DLS không tìm thấy lời giải trong giới hạn độ sâu.
- `NO_SOLUTION`: tìm kiếm đã kết thúc mà không có lời giải.
- `ERROR`: hiển thị nguyên nhân lỗi worker hoặc phản hồi JSON.

BFS/UCS có thể chậm do SimpleAI quét các node trong hàng đợi để kiểm tra trùng trạng thái. DLS/IDS có thể duyệt rất nhiều nhánh lặp. Mỗi cấu hình được tách tiến trình để dừng khi hết giờ và tiếp tục lượt kế tiếp. Không thay thuật toán thư viện bằng thuật toán tự viết khi timeout.

Với lời giải, chi phí bằng số bước. DFS/Greedy không đảm bảo tối ưu. Đường dài chỉ hiển thị tóm tắt; tùy chọn JSON vẫn lưu đầy đủ. CSV dùng UTF-8 BOM cho Windows. Chạy mặc định hoặc chọn menu không tự tạo file kết quả.

```

```
