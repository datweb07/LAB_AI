# Bài tập 1, 2, 3 — Trí tuệ nhân tạo (Chương 3–4)

## 1. Yêu cầu và đối chiếu tài liệu

| Bài | Nội dung | Vị trí trong source |
| --- | --- | --- |
| **Bài 1** | **Tự viết** BFS, DFS, UCS, DLS, IDS theo slide Chương 3. Không dùng SimpleAI. | `bai1_tu_cai_dat/` |
| **Bài 2** | Lấy ví dụ **HELLO WORLD từ tài liệu SimpleAI** (thuật toán dùng sẵn); kèm bản `AI` chạy nhanh để thử. | `bai2_vi_du_simpleai/` |
| **Bài 3** | Dùng **7 hàm có sẵn của SimpleAI** giải 8-Puzzle trên bảng. Chạy Greedy/A* với h1 và h2 riêng biệt. | `bai3_8_puzzle/` |

**Nguồn tài liệu:**
- PDF người dùng cung cấp: *Chương 3 — Tìm kiếm cơ bản*, trang 30 và 64 (5 thuật toán).
- PDF người dùng cung cấp: *Chương 4 — Tìm kiếm heuristic*, trang 5–13, 25–27 (Greedy, A*, h1, h2).
- https://simpleai.readthedocs.io/en/latest/
- https://simpleai.readthedocs.io/en/latest/search_problems.html
- https://github.com/simpleai-team/simpleai

## 2. Cài đặt và chạy

Cần **Python 3.10+** và Internet khi cài lần đầu. Mở Terminal trong thư mục gốc của project.

**Windows:** chạy `CHAY_TREN_WINDOWS.bat`, hoặc chủ động chạy:

```powershell
python -m pip install -r requirements.txt
python main.py
```

**Lệnh riêng cho từng bài:**

```powershell
# Bài 1 — chạy 5 thuật toán tự viết
python -m bai1_tu_cai_dat.chay_bai_1

# Bài 2 — chạy ví dụ SimpleAI rút gọn để kiểm tra nhanh
python -m bai2_vi_du_simpleai.vi_du_chay_nhanh

# Bài 2 — mã ví dụ HELLO WORLD mô phỏng sát tài liệu gốc;
# có thể rất lâu do không gian tìm kiếm lớn, không dùng để benchmark:
python -m bai2_vi_du_simpleai.vi_du_goc_tai_lieu

# Bài 3 — giải ma trận từ ảnh bảng bằng A* + h2; in tất cả các bước
python -m bai3_8_puzzle.chay_bai_3

# Bài 3 — gọi đủ 7 thuật toán (tổng 9 lượt khi xét h1/h2)
# mỗi lượt tối đa 5 giây, lưu báo cáo CSV
python -m bai3_8_puzzle.chay_bai_3 --all --timeout 5 --csv ket_qua_bai_3.csv

# Bài 3 — trình diễn cả 7 thuật toán trên trạng thái 1 bước tới đích
python -m bai3_8_puzzle.chay_bai_3 --all --demo

# Bài 3 — thời gian rộng hơn và DLS có giới hạn 20
python -m bai3_8_puzzle.chay_bai_3 --all --timeout 30 --depth-limit 20

# Kiểm tra code bằng unittest, không yêu cầu cài SimpleAI
python -m unittest discover -s tests -v
```

**Lưu ý:** Chạy các lệnh từ thư mục chứa `main.py`. Bài 2, 3 yêu cầu cài `simpleai==0.8.3` từ PyPI; Bài 1 và unit tests chỉ dùng Python chuẩn.

## 3. Giải thích Bài 1

Dùng một đồ thị có trọng số nhỏ với trạng thái đầu `S` và đích `G`:

```text
S --4--> A --2--> C --2--> G
|         |               ^
1         +------9--------+
|\
v B --1--> A
  \
   5--> D --1--> G
```

Chú ý hình ASCII chỉ để gợi ý; danh sách cạnh **chính xác** nằm ở `bai1_tu_cai_dat/do_thi.py`.

- **BFS:** dùng hàng đợi FIFO, tìm lời giải ít cạnh (không chắc rẻ nhất khi các cạnh có trọng số khác nhau).
- **DFS:** dùng stack LIFO và `visited` để tránh lặp; không đảm bảo đường đi ngắn nhất.
- **UCS:** dùng hàng đợi ưu tiên `heapq`; ưu tiên tổng chi phí đã đi `g(n)` nhỏ nhất.
- **DLS:** duyệt theo chiều sâu, cắt nhánh khi độ sâu đạt giới hạn đặt ra.
- **IDS:** lặp DLS từ độ sâu 0, 1, 2… đến khi thấy lời giải.

**Kết quả xác định:** BFS đi `S -> A -> G` (2 cạnh, chi phí **13**); UCS đi `S -> B -> A -> C -> G` (4 cạnh, chi phí **6**). Điều này minh họa BFS tìm đường có *ít bước* còn UCS tìm đường có *tổng chi phí thấp nhất*.

## 4. Bài 2 — Ví dụ SimpleAI

`vi_du_goc_tai_lieu.py` diễn đạt lại ví dụ `HelloProblem` trong **README/tài liệu**: `GOAL = 'HELLO WORLD'`, kế thừa `SearchProblem`, khai báo `actions`, `result`, `is_goal`, `heuristic` và gọi hàm `astar` **có sẵn** trong thư viện. Không copy hay tự viết lõi thuật toán.

Ví dụ có không gian trạng thái lớn do mỗi bước được chọn 27 ký tự, heuristic không chặt. Vì vậy dự án có thêm `vi_du_chay_nhanh.py` thay đích bằng `AI` để nhìn thấy BFS/A* chạy thực tế ngay. Bài 2 là code mẫu minh họa, không phải thuật toán tự viết.

## 5. Bài 3 — Phát biểu bài toán 8-Puzzle

Trên bảng, hai bảng 3×3 là:

```text
INITIAL STATE             GOAL STATE
 2 | 1 | 0                 1 | 2 | 3
---+---+---               ---+---+---
 3 | 4 | 5                 8 | 0 | 4
---+---+---               ---+---+---
 7 | 8 | 6                 7 | 6 | 5
```

Các thành phần của bài toán:

1. **Trạng thái:** một bảng 3×3 gồm 0..8, trong đó `0` là ô trống. Dữ liệu nguồn viết dạng **ma trận 2 chiều**, sau đó chuyển sang `tuple` 9 phần tử để tương thích `SimpleAI` và `graph_search=True`.
2. **Trạng thái ban đầu:** đúng `INITIAL STATE` được ghi trên bảng.
3. **Tập hành động:** chuyển ô trống **lên, xuống, trái, phải** nếu không vượt biên.
4. **Hàm chuyển trạng thái:** hoán đổi ô trống với ô kề theo hướng chọn.
5. **Kiểm tra đích:** so sánh trạng thái hiện tại và `GOAL STATE`.
6. **Chi phí mỗi bước:** 1; chi phí lời giải bằng số lần di chuyển.
7. **Điều kiện giải được:** hai cấu hình 3×3 có cùng parity nghịch thế. Bảng trên: số nghịch thế **3** và **7**, đều lẻ → **giải được**.

**h1 — Số ô sai vị trí** (không tính 0):

\[
  h_1(n)=\sum_{i=0}^{8}\mathbf{1}[n_i\ne 0\ \land\ n_i\ne goal_i]
\]

**h2 — Manhattan** (không tính 0):

\[
 h_2(n)=\sum_{v=1}^{8}\left(|row_n(v)-row_{goal}(v)|+|col_n(v)-col_{goal}(v)|\right)
\]

Với **trạng thái đầu trên bảng**:

- `h1(initial) = 7`.
- `h2(initial) = 10`.
- `h1(goal) = h2(goal) = 0`.

Hai heuristic đều không đánh giá vượt chi phí còn lại (admissible) khi mỗi hành động có chi phí 1; `h2` thông tin mạnh hơn hoặc bằng `h1` trong từng trạng thái.

### 7 thuật toán / 9 lượt chạy

| Thuật toán | Hàm SimpleAI | Heuristic sử dụng |
| --- | --- | --- |
| BFS | `breadth_first` | Không |
| DFS | `depth_first` | Không |
| UCS | `uniform_cost` | Không |
| DLS | `limited_depth_first` | Không; có `depth_limit` |
| IDS | `iterative_limited_depth_first` | Không |
| Greedy | `greedy` | Chạy riêng h1 và h2 |
| A* | `astar` | Chạy riêng h1 và h2 |

**Quan trọng về thời gian**: Với hai bảng trên, độ dài *tối ưu* đã được kiểm chứng bằng BFS độc lập là **20** bước. DFS có thể đi theo đường rất dài; IDS có thể mất nhiều thời gian, vì thế mỗi lần chạy được bọc trong **một tiến trình con** và dừng khi quá `--timeout`. Khi kết quả là `TIMEOUT`, phải ghi **chưa xác định được lời giải trong thời gian cấp**, không được ghi 'vô nghiệm'. Khi DLS trả `NO_SOLUTION_WITH_LIMIT`, có thể vì giới hạn độ sâu hoặc thứ tự duyệt, không nhất thiết vô nghiệm.

Hàm `--demo` chỉ đổi **trạng thái đầu**, giữ nguyên **đích của thầy**. Mục đích là trình diễn cả 7 thuật toán trong thời gian ngắn; không được đánh đồng kết quả `--demo` với ma trận ban đầu của đề bài.

## 6. Cấu trúc dự án

```text
BT_Tri_Tue_Nhan_Tao_SimpleAI/
├── main.py                            # Menu 3 bài
├── requirements.txt                   # simpleai==0.8.3
├── CHAY_TREN_WINDOWS.bat
├── README.md                           # Hướng dẫn và cơ sở lý thuyết
├── BAO_CAO_NGAN.md                    # Nội dung ngắn để thuyết trình/nộp
├── bai1_tu_cai_dat/
│   ├── do_thi.py
│   ├── thuat_toan.py
│   └── chay_bai_1.py
├── bai2_vi_du_simpleai/
│   ├── vi_du_goc_tai_lieu.py
│   └── vi_du_chay_nhanh.py
├── bai3_8_puzzle/
│   ├── puzzle_core.py                  # Ma trận, phép chuyển, h1/h2
│   ├── puzzle_problem.py               # SearchProblem
│   └── chay_bai_3.py                  # Gọi 7 hàm SimpleAI + timeout
└── tests/
    ├── test_thuat_toan.py
    └── test_do_dai_loi_giai.py
```

## 7. Kiểm tra trước khi nộp

- [x] 5 thuật toán Bài 1 được cài đặt riêng, không dùng SimpleAI.
- [x] Bài 2 có ví dụ theo tài liệu SimpleAI và một bản rút gọn.
- [x] Bài 3 sử dụng đúng hai ma trận chụp từ bảng; thuật toán lấy từ SimpleAI.
- [x] h1 và h2 riêng; có chạy Greedy/A* mỗi loại hai lần.
- [x] Kết quả `h1=7`, `h2=10`, độ dài tối ưu **20** được kiểm tra bằng Python thuần.
- [x] Có kiểm soát timeout / trạng thái không giải được.
- [ ] **Cần chạy thử trên máy đã cài `simpleai==0.8.3`** để xác nhận tích hợp thực tế; môi trường tạo bài tập không truy cập được PyPI để cài và thử thư viện.

Các file chỉ dùng thư viện chuẩn đã được kiểm tra bằng unit tests trong môi trường tạo bài. Phần tích hợp SimpleAI đã đối chiếu chữ ký hàm theo tài liệu API chính thức, nhưng chưa được chạy thực với gói cài từ PyPI.
