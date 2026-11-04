# BTVN: CSP, bài toán xếp hậu và thuật toán di truyền

Thư mục bài tập độc lập. Các file của bài tập cũ bên ngoài thư mục này không cần sửa.
Yêu cầu Python 3.10 trở lên. Đã kiểm tra với Python 3.11 và SimpleAI 0.8.3.

## 1. Cài đặt và chạy

Mở Terminal tại thư mục này:

```terminal
cd D:\LAB_AI\btvn_csp_ga
python -m venv .venv
./.venv/Scripts/python.exe -m pip install -r requirements.txt
./.venv/Scripts/python.exe -X utf8 main.py
```

Nếu Python hiện tại đã có SimpleAI, chạy `python -X utf8 main.py`.
Có thể nhấp đúp `CHAY_BAI_TAP.bat` khi Python mặc định đã cài SimpleAI.
File BAT luôn chuyển đến thư mục của chính nó nên không gọi nhầm `main.py` của bài cũ.

Chạy từng bài hoặc thay đổi cấu hình:

```powershell
python -X utf8 main.py --bai 1 --n 8 --seed 42
python -X utf8 main.py --bai 1 --n 10 --population 200 --generations 3000
python -X utf8 main.py --bai 2
python -X utf8 main.py --bai 3
python -X utf8 -m unittest -v test_baitap.py
```

`--n` chỉ áp dụng bài 1; bài 2 luôn dùng bàn cờ 5×5. Seed mặc định là 42.
`--mutation 0.25` là xác suất đột biến **trên mỗi cá thể con**, không phải mỗi gene.

## 2. Bài 1: cài đặt và mở rộng N hậu bằng GA

**Biểu diễn:** cá thể là tuple `(r1,...,rn)`, với `ri ∈ {1,...,n}` là hàng của hậu ở cột i.
Mỗi cột luôn có đúng một hậu, nhưng các cá thể trung gian có thể trùng hàng hoặc đường chéo.
Ví dụ `(1,3,5,2,4)` là một nghiệm của 5 hậu.

**Fitness:** gọi `h(s)` là số cặp hậu tấn công nhau; `M = n(n-1)/2`.
Ta tối đa hóa `f(s) = 1 + M - h(s)`. Một cặp chỉ tính một lần dù xét đồng thời
điều kiện hàng và đường chéo. Nghiệm có `h(s)=0`, tương ứng `f(s)=M+1`.
Số 1 làm fitness luôn dương, phù hợp phép chọn roulette của GA SimpleAI ở bài 2.

Các bước trong `custom_genetic()`:

1. **Khởi tạo:** tạo ngẫu nhiên `population_size` cấu hình đầy đủ, không nạp sẵn nghiệm.
2. **Đánh giá:** tính fitness, sắp xếp cá thể theo điểm giảm dần.
3. **Chọn lọc:** tournament kích thước 3; lấy cá thể tốt nhất trong mẫu ngẫu nhiên.
4. **Lai tạo:** chọn điểm cắt k thuộc `1..n-1`, lấy tiền tố cha và hậu tố mẹ.
   Ví dụ `(1,2,3,4,5)` lai `(5,4,3,2,1)` tại k=2 cho `(1,2,3,2,1)`.
5. **Đột biến:** với xác suất mặc định 0.25, chọn một cột rồi đổi sang một hàng khác.
6. **Elitism và đa dạng:** giữ nguyên một cá thể tốt nhất sang thế hệ tiếp theo;
   bổ sung khoảng 10% cá thể ngẫu nhiên mới mỗi thế hệ để giảm hội tụ sớm.
   Với quần thể nhỏ, giới hạn số cá thể mới để vẫn còn chỗ cho lai tạo.
   Nếu 50 thế hệ liên tiếp không cải thiện, giữ elite và tạo lại phần quần thể còn lại.
7. **Dừng:** khi tìm được nghiệm hoặc đạt giới hạn thế hệ. Quần thể đầu là thế hệ 0.

Phần mở rộng gồm tham số N, seed, kích thước quần thể, xác suất đột biến, giới hạn thế hệ,
elitism, cá thể nhập cư, lịch sử xung đột, số lần gọi các toán tử và hiển thị bàn cờ.
Số lần khởi tạo bao gồm quần thể ban đầu và các cá thể nhập cư về sau.
Chương trình in ví dụ cha/mẹ/con/đột biến trước khi chạy GA thực tế; ví dụ này dùng RNG riêng.
Với N=1 không cần lai hoặc đổi hàng. N=2,3 không có nghiệm; GA vẫn dừng theo ngân sách.
GA không bảo đảm tìm nghiệm trong số thế hệ hữu hạn. Kết quả chưa đạt đích được in rõ là
**chưa tìm được nghiệm**, không dùng điều đó để kết luận CSP vô nghiệm.

## 3. Bài 2: mô hình CSP 5 hậu

Định nghĩa CSP = `(X,D,C)`:

- **Biến:** `X={Q1,Q2,Q3,Q4,Q5}`; Qi biểu diễn hậu ở cột i.
- **Miền:** `D(Qi)={1,2,3,4,5}` cho cả 5 biến.
- **Ràng buộc:** với mọi `1 <= i < j <= 5`, `Qi != Qj` và
  `abs(Qi-Qj) != abs(i-j)`.

Trong code, tên biến là số cột `1..5`. Có `C(5,2)=10` ràng buộc nhị phân;
mỗi ràng buộc kết hợp kiểm tra khác hàng và khác đường chéo.
Khác cột đã được bảo đảm bởi cách biểu diễn. Mô hình thực sự dùng
`from simpleai.search import CspProblem, backtrack`, không giả lập thư viện.

### Backtracking và thứ tự ưu tiên

Backtrack lần lượt gán biến; nếu phát hiện vi phạm thì bỏ nhánh, quay lui và thử giá trị khác.
`compare_backtracking()` gọi trực tiếp `simpleai.search.backtrack` cho 7 cấu hình,
mỗi cấu hình chạy cả `inference=False` và `inference=True` (tổng 14 lần):

| Cấu hình             | Thứ tự biến                 | Thứ tự giá trị             |
| -------------------- | --------------------------- | -------------------------- |
| Cơ sở                | Thứ tự cột 1..5             | Hàng tăng 1..5             |
| MRV                  | `MOST_CONSTRAINED_VARIABLE` | Hàng tăng                  |
| Degree               | `HIGHEST_DEGREE_VARIABLE`   | Hàng tăng                  |
| LCV                  | Thứ tự cột                  | `LEAST_CONSTRAINING_VALUE` |
| MRV + LCV            | MRV                         | LCV SimpleAI               |
| Degree + LCV         | Degree                      | LCV SimpleAI               |
| Thứ tự giá trị ngược | Thứ tự cột                  | Hàng giảm 5..1             |

**Theo sách:** MRV chọn biến còn ít giá trị hợp lệ nhất; degree ưu tiên biến có nhiều
ràng buộc với các biến chưa gán; LCV thử giá trị loại ít lựa chọn của các biến lân cận nhất.
AC-3 truyền ràng buộc để giảm miền, khác với việc chỉ sắp thứ tự biến/giá trị.

**Lưu ý triển khai SimpleAI 0.8.3, đã kiểm tra mã nguồn cài đặt:**

- MRV so sánh kích thước miền đang lưu. Khi tắt inference, miền của biến chưa gán
  không được cập nhật theo phép gán, nên MRV có thể trùng thứ tự cơ sở.
- Degree dùng số ràng buộc tĩnh `var_degrees`. Đồ thị 5 hậu là đồ thị đầy đủ;
  mỗi biến đều bậc 4, nên heuristic này hòa điểm và không phân biệt được các cột.
- LCV của thư viện đếm ràng buộc vi phạm đã có đủ biến gán, không đếm đầy đủ
  số giá trị tương lai bị loại như định nghĩa LCV trong sách. Các giá trị đang hợp lệ
  có thể hòa điểm và được giữ nguyên thứ tự. Chương trình dùng đúng hằng LCV công khai
  của thư viện và không tuyên bố nó hiện thực đầy đủ LCV nhìn trước của sách.

Vì vậy nhiều cấu hình có thể cho cùng nghiệm hoặc cùng số lần kiểm tra; không nên
kết luận heuristic nào luôn nhanh hơn từ bài 5 hậu. Chỉ số in ra là **số lần gọi hàm
ràng buộc**, bao gồm kiểm tra phục vụ heuristic và suy diễn; không phải số nút hoặc
số lần quay lui. Các lần kiểm tra xác minh nghiệm sau khi giải không cộng vào thống kê.

### Chuyển CSP sang Search và giải bằng GA

`QueensSearchProblem(SearchProblem)` giữ một `CspProblem` bên trong và dùng chính
các ràng buộc của CSP để tính xung đột, kiểm tra đích:

- **Không gian trạng thái:** các phép gán đầy đủ `(Q1,...,Q5)`, kích thước `5^5=3125`.
- **Khởi đầu:** một quần thể các phép gán đầy đủ ngẫu nhiên, cho phép xung đột.
  `initial_state=(1,1,1,1,1)` chỉ mô tả một trạng thái xuất phát cho giao diện Search;
  hàm `genetic()` thực tế gọi `generate_random_state()` để tạo cả quần thể.
- **Hành động đơn:** `(c,r)` đổi hậu cột c sang hàng r khác hàng hiện tại;
  `actions()` có 20 lựa chọn, `result()` tạo cấu hình mới. Chỉ số c trong API là 0..4.
- **Đích:** mọi ràng buộc của CSP thỏa mãn, tương đương không có cặp hậu tấn công nhau.
- **Hàm mục tiêu:** `1 + 10 - h(s)`, điểm đích bằng 11. GA tối đa hóa điểm,
  không tìm đường đi ngắn nhất; không cần hàm chi phí đường đi.
- **Toán tử GA:** `generate_random_state`, `crossover`, `mutate`, `value`.
  GA dùng lai/đột biến để sinh cá thể, không gọi `actions()` để duyệt hàng xóm.

Hàm `simpleai_genetic()` gọi **`simpleai.search.genetic` thực sự**, mặc định
quần thể 120, đột biến 0.25, giới hạn 200 thế hệ. Thư viện dùng chọn cha mẹ roulette
theo fitness và thay toàn bộ quần thể, khác chọn tournament + elitism của bài 1.
Đặt giới hạn dương tránh chế độ mặc định dừng ngay khi điểm không cải thiện.

SimpleAI 0.8.3 chỉ trả cá thể tốt nhất của **thế hệ cuối**, có thể mất nghiệm đã gặp.
Do đó `value()` lưu thêm cá thể tốt nhất từng được đánh giá. Chương trình in cả
cá thể cuối do thư viện trả và cá thể tốt nhất đã lưu, kiểm tra đích trước khi báo thành công.
GA SimpleAI vẫn chạy đủ giới hạn thế hệ, kể cả nếu đã gặp nghiệm.

Nghiệm mẫu `(1,3,5,2,4)` tương ứng:

```text
Q . . . .
. . . Q .
. Q . . .
. . . . Q
. . Q . .
```

## 4. Bài 3: backtrack giải hệ phương trình nghiệm nguyên

```text
3x + 2y = 25
2x - y = 5
x,y ∈ Z ∩ [-10,10]
```

Mô hình `CspProblem` có biến `('x','y')`, miền riêng cho mỗi biến là
`list(range(-10,11))` (đủ 21 số nguyên, gồm cả hai đầu mút).
Ràng buộc thứ nhất `equation_one()` chỉ kiểm tra phương trình 1;
ràng buộc thứ hai `equation_two()` chỉ kiểm tra phương trình 2.
Cả hai cùng có phạm vi `('x','y')` và được đăng ký thành hai phần tử riêng.

Chạy `backtrack(problem, inference=False)` để giải bằng quay lui thuần túy.
Không dùng công thức đại số hoặc nghiệm biết trước để thay kết quả thuật toán.
Sau khi gán đủ x,y, các ràng buộc mới có đủ dữ liệu để kiểm tra.

Kết quả duy nhất: **x=5, y=5**. Thế lại: `3*5+2*5=25`, `2*5-5=5`.
Đối chiếu đại số: từ phương trình 2 suy ra `y=2x-5`; thay vào phương trình 1 được
`7x=35`, tức `x=5,y=5`, nằm trong miền yêu cầu.

## 5. Tệp và kiểm chứng

| Tệp                 | Nội dung                                                          |
| ------------------- | ----------------------------------------------------------------- |
| `csp_models.py`     | Mô hình CSP, các chiến lược backtrack, hệ phương trình, in bàn cờ |
| `genetic_queens.py` | GA tự cài và lớp chuyển CSP sang SearchProblem cho GA SimpleAI    |
| `main.py`           | CLI chạy 3 bài và in kết quả                                      |
| `test_baitap.py`    | Kiểm chứng bằng unittest, không cần thư viện test ngoài           |
| `ket_qua_mau.txt`   | Kết quả chạy thật với cấu hình mặc định, seed 42                  |
| `requirements.txt`  | Phiên bản SimpleAI sử dụng                                        |
| `CHAY_BAI_TAP.bat`  | Chạy trên Windows                                                 |

Kiểm chứng dùng điều kiện tập hàng/đường chéo độc lập với hàm ràng buộc của chương trình:
duyệt đủ 3125 cấu hình 5 hậu, xác nhận có 10 nghiệm (chưa gộp đối xứng);
kiểm tra cả 14 cấu hình backtrack; kiểm tra nghiệm GA 8 hậu và 5 hậu;
duyệt đủ 441 cặp số nguyên để xác nhận hệ chỉ có một nghiệm;
kiểm tra N=1, N=2, N=3, các toán tử lai/đột biến, khả năng tái lập seed và chuyển trạng thái.

## 6. Tài liệu tham khảo

- PDF người dùng cung cấp: `1. Book - AI (2021 edition).pdf`, trang **359–408 theo số
  trang của tệp PDF**: chương 6, _Constraint Satisfaction Problems_. Trang 359 mở đầu chương;
  trang 365 mô hình N hậu; 381–387 backtracking, MRV, degree, LCV, forward checking và MAC;
  391–392 biểu diễn đầy đủ và tìm kiếm cục bộ; 402 tổng kết. Số trang in trong nội dung sách
  có thể khác số thứ tự trang của trình xem PDF. Không sao chép hay sửa file PDF gốc.
- [SimpleAI: Constraint satisfaction problems](https://simpleai.readthedocs.io/en/latest/constraint_satisfaction_problems.html):
  `CspProblem`, `backtrack`, các hằng heuristic và `inference`.
- [SimpleAI: Local search algorithms](https://simpleai.readthedocs.io/en/latest/local_search_problems.html):
  giao diện `SearchProblem` cho GA, các toán tử di truyền và `genetic()`.
- Mã nguồn SimpleAI 0.8.3 đã cài: `simpleai.search.csp` và `simpleai.search.local`,
  dùng để đối chiếu hành vi heuristic và cách trả kết quả của GA. Website tài liệu hiện
  gắn nhãn 0.8.2; file requirements khóa bản 0.8.3 đã chạy kiểm chứng.

Phần GA là cách triển khai theo yêu cầu bài tập. Chương CSP trong khoảng trang được chỉ định
cung cấp nền tảng biểu diễn và tìm kiếm cục bộ, không được viện dẫn như mã GA của chương trình.
