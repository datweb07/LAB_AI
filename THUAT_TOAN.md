# Mô tả thuật toán và cách triển khai

## Tài liệu đối chiếu

- [SimpleAI SearchProblem và API tìm kiếm](https://simpleai.readthedocs.io/en/latest/search_problems.html).
- [Mã nguồn SimpleAI](https://simpleai.readthedocs.io/en/latest/_modules/simpleai/search/traditional.html).
- [Ví dụ HELLO WORLD](https://simpleai.readthedocs.io/en/latest/).

## Bài 1 - Năm thuật toán tự cài đặt

Mã nằm trong `bai1_tu_cai_dat/thuat_toan.py`, dữ liệu ở `do_thi.py`. Không sử dụng SimpleAI.

| Thuật toán | Nguyên lý                                    | Cấu trúc trong mã                                     | Tính tối ưu                                                           |
| ---------- | -------------------------------------------- | ----------------------------------------------------- | --------------------------------------------------------------------- |
| BFS        | Mở rộng theo độ sâu tăng dần                 | `deque`, lấy đầu và thêm cuối; đánh dấu khi phát hiện | Ít cạnh nhất; tối ưu chi phí nếu mọi bước có cùng chi phí             |
| DFS        | Đi sâu trước, quay lại khi hết nhánh         | Stack LIFO, tập đã duyệt                              | Không đảm bảo tối ưu                                                  |
| UCS        | Mở rộng đường có tổng chi phí g(n) thấp nhất | `heapq`, bảng chi phí tốt nhất, bỏ bản ghi cũ         | Tối ưu với trọng số không âm trên đồ thị hữu hạn này                  |
| DLS        | DFS nhưng không mở rộng vượt giới hạn        | Đệ quy, kiểm tra độ sâu, tránh lặp trên từng đường    | Phụ thuộc giới hạn và thứ tự nhánh                                    |
| IDS        | Chạy lại DLS với giới hạn 0, 1, 2, ...       | Vòng lặp đến độ sâu tối đa do người gọi truyền        | Ít bước nhất nếu lời giải nằm trong phạm vi và chi phí bước bằng nhau |

BFS tìm đường `S → A → G` có 2 cạnh, chi phí 13. UCS tìm `S → B → A → C → G` có 4 cạnh, chi phí 6: ít bước không đồng nghĩa ít chi phí.

DFS dùng tập đã duyệt để tránh chu trình trong đồ thị hữu hạn. DLS tránh chu trình theo từng nhánh, cho phép xét lại một trạng thái ở nhánh khác; gốc có độ sâu 0. Kết quả DLS chứa đường đi hoặc `None`, không tách riêng CUTOFF/FAILURE. IDS có giới hạn tối đa rõ ràng để dừng nếu không tìm thấy lời giải, thay vì lặp vô hạn; nguyên lý lặp DLS phù hợp slide Chương 3 trang PDF 52-54.

Slide nêu tính hoàn chỉnh tổng quát của UCS khi chi phí mỗi cạnh có cận dưới dương ε. Với đồ thị hữu hạn và kiểm tra chi phí tốt nhất trong mã, cạnh chi phí 0 vẫn được xử lý; không dùng thuật toán này cho cạnh âm.

## Bài 2 - Example SimpleAI

`vi_du_goc_tai_lieu.py` giữ ví dụ tạo chuỗi HELLO WORLD. Class `HelloProblem` kế thừa `SearchProblem` và định nghĩa:

- `actions(state)`: các ký tự có thể nối thêm khi chưa đủ độ dài.
- `result(state, action)`: nối ký tự vào chuỗi.
- `is_goal(state)`: so sánh với chuỗi đích.
- `heuristic(state)`: số ký tự sai cộng số ký tự còn thiếu.

Ví dụ gọi `astar` từ SimpleAI. Chi phí mỗi hành động dùng mặc định 1 của `SearchProblem`. Bản ngắn `vi_du_chay_nhanh.py` dùng đích AI, khai báo `cost` bằng 1 và gọi cả BFS/A\*. Không tự triển khai thuật toán tìm kiếm.

SimpleAI trả solution node hoặc `None`. `node.state` là đích tìm được, `node.path()` là danh sách `(hành động, trạng thái)` từ gốc đến đích. Gốc có hành động `None`, nên số bước là `len(node.path()) - 1`.

## Bài 3 - Phát biểu bài toán

Dữ liệu nguồn là ma trận 3×3 theo ảnh bảng. `puzzle_core.py` chuyển ma trận sang tuple 9 phần tử bất biến; cách lưu nội bộ này giữ nguyên dữ liệu hai chiều và cho phép hash khi graph search.

- Initial: `2 1 0 / 3 4 5 / 7 8 6`.
- Goal: `1 2 3 / 8 0 4 / 7 6 5`.
- Hành động: di chuyển ô trống lên, xuống, trái, phải trong biên.
- Chuyển trạng thái: hoán đổi 0 với ô kề, không sửa trạng thái cũ.
- Kiểm tra đích: so sánh với Goal ở trên.
- Chi phí: mỗi hành động bằng 1, tổng chi phí bằng số bước.
- Khả năng giải: trên bảng 3×3, Initial và Goal phải cùng parity nghịch thế; hai ma trận có 3 và 7 nghịch thế nên giải được.

`BaiToan8Puzzle(SearchProblem)` trong `puzzle_problem.py` nối các quy tắc trên với API thư viện qua `actions`, `result`, `is_goal`, `cost`, `heuristic`. Heuristic được chọn theo từng instance, không đổi qua biến toàn cục.

## Hai heuristic

### h1 - Misplaced Tiles

Đếm các ô số sai vị trí so với Goal, **không tính ô trống**:

```text
h1(n) = số vị trí i có n[i] khác 0 và n[i] khác goal[i]
```

### h2 - Manhattan Distance

Tính khoảng cách theo hàng/cột từ từng ô số đến đúng vị trí của nó trong Goal, **không tính ô trống**:

```text
h2(n) = tổng trên các ô số 1..8 của
        |hàng hiện tại - hàng đích| + |cột hiện tại - cột đích|
```

Vị trí đích được tính trước theo Goal của giảng viên. Initial có h1 = 7, h2 = 10; tại Goal cả hai bằng 0. h1/h2 phù hợp định nghĩa ở Chương 4 trang PDF 25-26. Giá trị 8/18 trong ví dụ slide thuộc một ma trận khác, không phải kết quả của đề này.

Cả hai là heuristic chấp nhận được: không đánh giá vượt chi phí tối ưu còn lại. Chúng cũng kiên định: `h(n) ≤ c(n,a,n') + h(n')`. Một bước chỉ di chuyển một ô số một đơn vị. h2 ≥ h1, nên h2 ưu thế hơn h1 theo định nghĩa trong slide.

## Bảy thuật toán SimpleAI

| Thuật toán | Hàm được gọi trực tiếp          | graph_search | Heuristic           |
| ---------- | ------------------------------- | ------------ | ------------------- |
| BFS        | `breadth_first`                 | True         | Không               |
| DFS        | `depth_first`                   | True         | Không               |
| UCS        | `uniform_cost`                  | True         | Không               |
| DLS        | `limited_depth_first`           | False        | Không               |
| IDS        | `iterative_limited_depth_first` | False        | Không               |
| Greedy     | `greedy`                        | True         | Chạy riêng h1 và h2 |
| A\*        | `astar`                         | True         | Chạy riêng h1 và h2 |

Greedy chọn node có `h(n)` nhỏ nhất, không đảm bảo tối ưu. A* dùng `f(n) = g(n) + h(n)`: g là chi phí đã đi, h là ước lượng còn lại. Slide phân biệt A* tree search tối ưu với heuristic chấp nhận được và A* graph search tối ưu với heuristic kiên định. h1/h2 của bài này đáp ứng điều kiện kiên định, nên A* graph search tìm lời giải tối ưu.

DLS nhận `depth_limit`; IDS không nhận tham số này trong API SimpleAI 0.8.3. DLS/IDS giữ tree search vì tập đóng của SimpleAI có thể loại một đường đến cùng trạng thái ở độ sâu nhỏ hơn, làm bỏ sót đích trong giới hạn. Đổi lại, tree search có nhiều nhánh lặp và có thể timeout.

Thứ tự hành động hợp lệ cố định là `LEN, XUONG, PHAI, TRAI`, lọc theo biên. LIFO xét phần tử thêm cuối trước; vì vậy DFS/DLS đi trái trước ở demo. Thứ tự không dựa vào Goal hoặc heuristic, và không đảm bảo DFS tối ưu trên đề chính.

## Luồng chạy và kiểm tra lời giải

`chay_bai_3.py` nhận tham số → tạo worker → gọi hàm SimpleAI → phát lại toàn bộ path để kiểm tra hành động, trạng thái, đích, số bước và chi phí → trả JSON về tiến trình chính → hiển thị bảng/đường đi.

Mỗi worker có timeout riêng. Khi hết giờ, tiến trình được kết thúc và chờ thu hồi trước khi chạy cấu hình tiếp theo. JSON giữa các tiến trình dùng ASCII-safe; console xuất UTF-8. Chỉ xuất file CSV/JSON khi được yêu cầu bằng tham số dòng lệnh.

Bài 3 không gọi thuật toán Bài 1, không sửa mã nguồn SimpleAI và không tự thay thuật toán khi timeout.
