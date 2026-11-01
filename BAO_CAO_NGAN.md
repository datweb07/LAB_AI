# BÁO CÁO NGẮN — BÀI 1, 2, 3

**Học phần:** Trí tuệ nhân tạo — Tìm kiếm cơ bản và tìm kiếm heuristic.  
**Ngôn ngữ:** Python 3.10+. **Thư viện:** SimpleAI 0.8.3 cho Bài 2 và 3.

## Bài 1. Tự cài đặt 5 thuật toán

Tôi tự viết BFS (hàng đợi FIFO), DFS (ngăn xếp LIFO), UCS (hàng đợi ưu tiên theo tổng chi phí), DLS (DFS giới hạn độ sâu) và IDS (lặp DLS với các mức sâu tăng dần) để tìm đường trên đồ thị có trọng số. Với đồ thị ví dụ, BFS tìm đường `S -> A -> G`, chi phí 13, nhưng UCS tìm đường `S -> B -> A -> C -> G`, chi phí 6. Điều này cho thấy BFS ưu tiên ít bước đi, còn UCS ưu tiên chi phí thấp nhất.

## Bài 2. Ví dụ dùng thư viện SimpleAI

Từ tài liệu SimpleAI, tôi sử dụng bài toán tạo chuỗi "HELLO WORLD". Chương trình kế thừa `SearchProblem`, định nghĩa các hàm `actions`, `result`, `is_goal`, `heuristic`, rồi gọi `astar` có sẵn. Tôi bổ sung bản rút gọn tạo chuỗi "AI" chạy bằng BFS và A* để dễ trình diễn nhanh. Các thuật toán ở bài này là của thư viện, không phải tự cài lại.

## Bài 3. Giải bài toán 8-Puzzle

Bài toán sử dụng trạng thái đầu `[[2,1,0],[3,4,5],[7,8,6]]` và trạng thái đích `[[1,2,3],[8,0,4],[7,6,5]]` theo ảnh giảng viên. Ô 0 được coi là ô trống. Một thao tác hợp lệ di chuyển ô trống lên/xuống/trái/phải nếu không vượt biên, chi phí mỗi bước bằng 1.

Hai heuristic:

- `h1`: số ô nằm sai vị trí, không tính ô trống. Với đầu vào trên bảng: **7**.
- `h2`: tổng khoảng cách Manhattan từ từng ô số tới vị trí đích, không tính ô trống. Với đầu vào trên bảng: **10**.

Chương trình gọi trực tiếp 7 thuật toán từ SimpleAI: BFS, DFS, UCS, DLS, IDS, Greedy, A*. Với Greedy và A* chương trình chạy riêng hai loại heuristic h1, h2. Các thuật toán được gọi cùng bài toán để so sánh số bước và thời gian tìm kiếm. Bài toán có lời giải, đường đi tối ưu dài **20 bước** (đã xác nhận bằng BFS kiểm chứng riêng).

Tôi bổ sung giới hạn thời gian theo thuật toán, bởi DFS và IDS có thể phải duyệt rất nhiều trạng thái. Kết quả `TIMEOUT` chỉ có nghĩa là thuật toán chưa hoàn thành trong thời gian cấp, không đồng nghĩa với vô nghiệm. `--demo` là trạng thái dễ hơn, dành cho việc trình diễn đủ 7 thuật toán, không phải dữ liệu đề gốc.

**Cách chạy:**

```shell
python -m pip install -r requirements.txt
python main.py
python -m unittest discover -s tests -v
```

**Ghi chú kiểm chứng:** Đã kiểm thử các mô-đun Python thuần; phần chạy SimpleAI cần được chạy lại trên máy có cài gói do môi trường tạo không thể kết nối PyPI.
