import heapq
import turtle #thư viện con rùa
import time

def a_star_with_visualization(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    open_list = []
    closed_list = set()

    # Đưa điểm bắt đầu vào danh sách mở
    heapq.heappush(open_list, (heuristic(start, end), start))

    g_cost = {start: 0}  # Chi phí g(n)
    came_from = {start: None}  # Để lưu cha của mỗi ô

    while open_list:
        # Loại n bên trái của open và đưa vào closed
        _, current = heapq.heappop(open_list)
        closed_list.add(current)

        # Hiển thị mê cung hiện tại
        draw_maze(maze, current, closed_list, open_list, start, end)

        # Nếu n là đích, tái tạo đường đi 
        if current == end:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            draw_path(path)  # Tô đường đi ngắn nhất
            return path[::-1]

        # Sinh các con m của n
        for move in moves:
            neighbor = (current[0] + move[0], current[1] + move[1])

            # Kiểm tra tính hợp lệ của ô hàng xóm
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor[0]][neighbor[1]] == 0:
                new_g_cost = g_cost[current] + 1  # g(m) = g(n) + c[n, m]

                if neighbor not in g_cost or new_g_cost < g_cost[neighbor]:
                    g_cost[neighbor] = new_g_cost
                    f_cost = new_g_cost + heuristic(neighbor, end)
                    heapq.heappush(open_list, (f_cost, neighbor))
                    came_from[neighbor] = current

    return None  # Không tìm thấy đường đi

# Hàm heuristic (khoảng cách Manhattan)
def heuristic(cell, end):
    return abs(cell[0] - end[0]) + abs(cell[1] - end[1])

# Các bước di chuyển (lên, xuống, trái, phải)
moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Vẽ mê cung bằng thư viện turtle
def draw_maze(maze, current, closed_list, open_list, start, end):
    cell_size = 20
    turtle.clear()
    turtle.speed(0)
    turtle.hideturtle()

    rows, cols = len(maze), len(maze[0])
    for row in range(rows):
        for col in range(cols):
            x, y = col * cell_size, -row * cell_size

            if (row, col) == start:
                draw_cell(x, y, "green")  # Điểm bắt đầu
            elif (row, col) == end:
                draw_cell(x, y, "red")  # Điểm kết thúc
            elif (row, col) in closed_list:
                draw_cell(x, y, "gray")  # Ô đã duyệt
            elif any((row, col) == cell[1] for cell in open_list):
                draw_cell(x, y, "yellow")  # Ô đang chờ duyệt
            elif maze[row][col] == 1:
                draw_cell(x, y, "black")  # Tường
            else:
                draw_cell(x, y, "white")  # Đường đi

    # Đánh dấu ô hiện tại
    x, y = current[1] * cell_size, -current[0] * cell_size
    draw_cell(x, y, "blue")

    turtle.update()
    time.sleep(0.5) #tốc độ giải

def draw_path(path):
    cell_size = 20
    for step in path:
        x, y = step[1] * cell_size, -step[0] * cell_size
        draw_cell(x, y, "cyan")  # Tô màu đường đi ngắn nhất
    turtle.update()

def draw_cell(x, y, color):
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.fillcolor(color)
    turtle.begin_fill()
    for _ in range(4):
        turtle.forward(20)
        turtle.right(90)
    turtle.end_fill()

# Mê cung mẫu
maze = [
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0]
]

start = (0, 0)
end = (6, 13)

turtle.tracer(0, 0)
path = a_star_with_visualization(maze, start, end)
if path:
    print("\n\nĐường đi ngắn nhất từ điểm bắt đầu đến điểm kết thúc:")
    for step in path:
        print(step)
else:
    print("Không tìm thấy đường đi từ điểm bắt đầu đến điểm kết thúc.")

turtle.done()
