# Kết quả tham chiếu — 8-Puzzle đúng ma trận trên bảng

**Chú ý:** Đây là đường đi ngắn nhất do chương trình BFS độc lập (chỉ phục vụ kiểm thử) xác định. Không phải log chạy thực tế của gói SimpleAI. Các thuật toán khác có thể cho ra đường đi khác; Greedy/DFS không bắt buộc có đường đi ngắn nhất.

**Trạng thái ban đầu:**

```text
| 2 | 1 |   |
| 3 | 4 | 5 |
| 7 | 8 | 6 |
```

**Trạng thái đích:**

```text
| 1 | 2 | 3 |
| 8 |   | 4 |
| 7 | 6 | 5 |
```

Độ dài lời giải tối ưu: **20 lần di chuyển**.

## Chuỗi di chuyển ô trống

`TRAI → XUONG → XUONG → PHAI → LEN → LEN → TRAI → XUONG → TRAI → LEN → PHAI → XUONG → PHAI → LEN → TRAI → XUONG → TRAI → LEN → PHAI → XUONG`

## Các trạng thái và heuristic

| Bước | Hành động của ô trống | Bảng hiện tại (hàng 1 / hàng 2 / hàng 3) | h1 | h2 |
|---:|---|---|---:|---:|
| 0 | BẮT ĐẦU | `2 1 0 / 3 4 5 / 7 8 6` | 7 | 10 |
| 1 | TRAI | `2 0 1 / 3 4 5 / 7 8 6` | 7 | 11 |
| 2 | XUONG | `2 4 1 / 3 0 5 / 7 8 6` | 7 | 12 |
| 3 | XUONG | `2 4 1 / 3 8 5 / 7 0 6` | 7 | 11 |
| 4 | PHAI | `2 4 1 / 3 8 5 / 7 6 0` | 6 | 10 |
| 5 | LEN | `2 4 1 / 3 8 0 / 7 6 5` | 5 | 9 |
| 6 | LEN | `2 4 0 / 3 8 1 / 7 6 5` | 5 | 10 |
| 7 | TRAI | `2 0 4 / 3 8 1 / 7 6 5` | 5 | 9 |
| 8 | XUONG | `2 8 4 / 3 0 1 / 7 6 5` | 5 | 10 |
| 9 | TRAI | `2 8 4 / 0 3 1 / 7 6 5` | 5 | 9 |
| 10 | LEN | `0 8 4 / 2 3 1 / 7 6 5` | 5 | 10 |
| 11 | PHAI | `8 0 4 / 2 3 1 / 7 6 5` | 5 | 9 |
| 12 | XUONG | `8 3 4 / 2 0 1 / 7 6 5` | 5 | 8 |
| 13 | PHAI | `8 3 4 / 2 1 0 / 7 6 5` | 5 | 7 |
| 14 | LEN | `8 3 0 / 2 1 4 / 7 6 5` | 4 | 6 |
| 15 | TRAI | `8 0 3 / 2 1 4 / 7 6 5` | 3 | 5 |
| 16 | XUONG | `8 1 3 / 2 0 4 / 7 6 5` | 3 | 4 |
| 17 | TRAI | `8 1 3 / 0 2 4 / 7 6 5` | 3 | 3 |
| 18 | LEN | `0 1 3 / 8 2 4 / 7 6 5` | 2 | 2 |
| 19 | PHAI | `1 0 3 / 8 2 4 / 7 6 5` | 1 | 1 |
| 20 | XUONG | `1 2 3 / 8 0 4 / 7 6 5` | 0 | 0 |

## Diễn giải

Chỉ di chuyển ô trống qua một ô kề theo chiều ngang hoặc dọc; mỗi hành động có chi phí 1. Khi bảng trùng trạng thái đích, cả hai heuristic đều bằng 0.

### Ghi chú về thời gian chạy

Trong Bài 3 chính thức, BFS, DFS, UCS, DLS, IDS, Greedy và A* đều **gọi từ SimpleAI**, không phải dùng đoạn BFS kiểm chứng ở đây. Các phép thử thực tế với thư viện cần được chạy trên máy đã `pip install -r requirements.txt`.
