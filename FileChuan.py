import pygame
import random

# Khởi tạo Pygame
pygame.init()
pygame.mixer.init()

# Kích thước màn hình và màu sắc
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)

# Khởi tạo màn hình
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)

clock = pygame.time.Clock()

# Tải âm thanh
jump_sound = pygame.mixer.Sound("nhayqua1.mp3")
collision_sound = pygame.mixer.Sound("damvocnv.mp3")
item_pickup_sound = pygame.mixer.Sound("nhacanhoacnhay.mp3")
pygame.mixer.music.load("nhacnen1.mp3")
pygame.mixer.music.play(-1)  # Phát nhạc nền lặp lại liên tục
# Điều chỉnh âm lượng
pygame.mixer.music.set_volume(0.6)  # Giảm âm lượng nhạc nền
item_pickup_sound.set_volume(0.3)  # Giảm âm lượng âm thanh ăn vật phẩm
jump_sound.set_volume(0.1)  # Giảm âm lượng âm thanh nhảy


# Lớp kĩ sư
class Engineer:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load("kisu60.png"), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 50, SCREEN_HEIGHT - 80
        self.is_jumping, self.velocity, self.jump_count = False, 0, 0
        self.has_shield = False  # Khởi tạo kĩ sư không có bảo vệ
        self.shield_count = 0  # Biến đếm số lượng bảo vệ

    def jump(self):
        if self.jump_count < 7:  # Cho phép nhảy tối đa 7 lần liên tiếp
            self.is_jumping = True
            self.velocity = -12
            self.jump_count += 1
            jump_sound.play()  # Phát âm thanh nhảy

    def update(self):
        if self.is_jumping:
            self.velocity += 1  # Trọng lực
            self.rect.y += self.velocity
            if self.rect.y >= SCREEN_HEIGHT - 80:
                self.rect.y = SCREEN_HEIGHT - 80
                self.is_jumping = False
                self.jump_count = 0

    def draw(self):
        screen.blit(self.image, self.rect)

    def activate_shield(self):
        self.has_shield = True  # Kích hoạt vật phẩm bảo vệ
        self.shield_count += 1  # Tăng số lượng bảo vệ

    def deactivate_shield(self):
        self.has_shield = False  # Tắt trạng thái bảo vệ
        self.shield_count = 0  # Đặt lại số lớp bảo vệ

# Lớp vật phẩm và chướng ngại vật
class Item:
    def __init__(self, image_path, size=(20, 20)):
        self.image = pygame.transform.scale(pygame.image.load(image_path), size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 300), SCREEN_HEIGHT - 80 #vẽ ngẫu nhiên
       # self.rect.x: Vị trí ngẫu nhiên ngoài màn hình bên phải, từ SCREEN_WIDTH đến SCREEN_WIDTH + 300.
       # self.rect.y: Đặt vật phẩm gần đáy màn hình, với khoảng cách cố định (SCREEN_HEIGHT - 80).

    def update(self):
        self.rect.x -= 5 # Di chuyển vật phẩm từ phải sang trái với tốc độ 5 pixel mỗi khung hình.

    def draw(self):
        screen.blit(self.image, self.rect) # Vẽ hình ảnh vật phẩm lên màn hình tại vị trí hiện tại (self.rect).

class Obstacle(Item):
    def __init__(self, image_path, size=(20, 40)): # Gọi hàm khởi tạo của lớp Item để thiết lập hình ảnh và vị trí cơ bản.
        super().__init__(image_path, size)
        self.rect.y = SCREEN_HEIGHT - 80 # Tọa độ y: Đặt chướng ngại vật ở sát đáy màn hình (SCREEN_HEIGHT - 80).

class Shield(Item):
    def __init__(self):
        super().__init__("vatphambaove.png", size=(30, 30))  # chèn đường dẫn của hình ảnh vật phẩm bảo vệ
        self.rect.y = SCREEN_HEIGHT - 100  # Đặt vị trí vật phẩm bảo vệ

class Background:
    def __init__(self):
        self.backgrounds = [
            pygame.transform.scale(pygame.image.load("br3i1.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)), # ảnh nền 1
            pygame.transform.scale(pygame.image.load("br3i.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))  # ảnh nền 2
        ]
        self.current_background_index = 0  # Chỉ số nền hiện tại
        self.x1, self.x2 = 0, SCREEN_WIDTH
        #self.x1 = 0: từ góc trái màn hình.
        #self.x2 = SCREEN_WIDTH: bắt đầu ngay sau nền thứ nhất.



    def update(self): # cập nhật trạng thái 
        self.x1, self.x2 = self.x1 - 2, self.x2 - 2 #Di chuyển cả hai hình nền từ phải sang trái với vận tốc 2 pixel
        if self.x1 <= -SCREEN_WIDTH: self.x1 = SCREEN_WIDTH #tọa độ hình nền 1 khi nó di chuyển ra hết bên trái màn hình, nó sẽ xuất hiện lại bên phải
        if self.x2 <= -SCREEN_WIDTH: self.x2 = SCREEN_WIDTH #tọa độ hình nền 2 khi nó di chuyển ra hết bên trái màn hình, nó sẽ xuất hiện lại bên phải
                                               #SCREEN_WIDTH đảm bảo hình nền xuất hiện liền kề
    def draw(self):
        screen.blit(self.backgrounds[self.current_background_index], (self.x1, 0)) #Vẽ br1 :self.x1: Tọa độ x (di chuyển theo thời gian),0: Tọa độ y (nền luôn nằm sát đỉnh màn hình)

        screen.blit(self.backgrounds[self.current_background_index], (self.x2, 0)) # vẽ br2 tương tự

    def change_background(self, index):
        if index < len(self.backgrounds): # kiểm tra xem chỉ số index có hợp lệ không 
            self.current_background_index = index
def game_over_screen(score):
    font = pygame.font.Font(None, 50)  # Dùng font mặc định cho bảng điểm
    
    # Kiểm tra tải ảnh "Game Over"
    try:
        game_over_image = pygame.image.load("restart1.png") # đường dẫn ảnh game over
    except pygame.error as e:
        print(f"Error loading image: {e}")
        game_over_image = None  #print none nếu k tải được ảnh 

    # Vẽ ảnh "Game Over" 
    if game_over_image:
        game_over_image = pygame.transform.scale(game_over_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(game_over_image, (0, 0))  # Vẽ ảnh "Game Over" lên màn hình

    # Hiển thị bảng điểm (Score)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))
    pygame.display.flip()  # Cập nhật màn hình

# Hàm kiểm tra và tạo khoảng cách tối thiểu giữa các vật thể
def check_gap(obstacles, min_gap=150): # đảm bảo khoảng cách obstacles liên tiếp không nhỏ hơn 150
    for i in range(len(obstacles) - 1): # hàm lặp qua all cnv, trừ cnv cuối 
        if obstacles[i].rect.x + obstacles[i].rect.width > obstacles[i + 1].rect.x:
            #rect.x: tọa độ x của mép trái hcn(vị trí ban đầu trên trục x)
            #rect.width:chiều rộng hcn(khoảng cách từ mép trái đến mép phải)
            #cộng tọa độ x của mép trái (rect.x) với chiều rộng (rect.width)=> tọa độ x của mép phải của cnv trước(i)
            #obstacles[i + 1].rect.x: tọa độ mép trái của cnv sau(i+1) 
            #Nếu mép phải của cnv trước(i) vượt qua mép trái của cnv sau(i+1)=> khoảng cách 2 vật thể ko đủ


            obstacles[i + 1].rect.x = obstacles[i].rect.x + obstacles[i].rect.width + min_gap # nếu khoảng cách 2 vật thể không đủ thì mép trái của cnv sau = mép phải cnv trước + 150

# Hàm vẽ bảng điểm và số lượng bảo vệ
def draw_score_and_shield_count(score, shield_count):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    shield_count_text = font.render(f"Shield Count: {shield_count}", True, WHITE)

    # Vị trí bảng điểm và số lượng bảo vệ
    screen.blit(score_text, (10, 10))
    screen.blit(shield_count_text, (10, 50))  # Vẽ số lượng bảo vệ dưới bảng điểm
    # Hàm chính
def main():
    running = True
    engineer=Engineer()
    background = Background()
    score, font = 0, pygame.font.Font(None, 36)
    background_changed = False  # Đánh dấu việc thay đổi nền


    # Danh sách vật phẩm và chướng ngại vật
    items = [
        Item("daurobot.png"),
        Item("tayrobot.png"),
        Item("linhkien.png"),
    ]
    shields = []  # Danh sách vật phẩm bảo vệ (ban đầu không có bảo vệ)
    obstacles = [Obstacle("virus (2).png")]
    last_shield_time = 0  # Thời gian xuất hiện vật phẩm bảo vệ
    last_obstacle_time = pygame.time.get_ticks()
    shield_spawn_probability = 0.3  # Xác suất 30% cho mỗi lần kiểm tra

    shield_spawned = False  # Đánh dấu khi nào bắt đầu xuất hiện bảo vệ
    reached_70_points = False
    # Game Loop
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    engineer.jump()
    # Đổi nền khi đạt 250 điểm
        if score >= 250 and not background_changed: # toán tử and: nếu điểm số lớn hơn hoặc bằng 250 và chưa đổi nền(biến background_changed đang ở trạng thái False) 
            background.change_background(1)  # Chuyển sang nền thứ 2
            background_changed = True # đánh dấu nền đã đổi
 # Kích hoạt xuất hiện vật phẩm bảo vệ khi đạt 70 điểm
        if score >= 70 and not shield_spawned: #toán tử and: nếu điểm số lớn hơn hoặc bằng 70 và chưa xuất hiện vật phẩm bảo vệ(biến shield_spawned đang ở trạng thái False) 
            shield_spawned = True
            last_shield_time = pygame.time.get_ticks()

            MAX_SHIELDS = 1  # Giới hạn tối đa số lượng vật phẩm bảo vệ trên màn hình

             # Sinh vật phẩm bảo vệ mỗi 25 giây với xác suất và giới hạn số lượng
        if (
            shield_spawned 
            and pygame.time.get_ticks() - last_shield_time >= 25000  # Kiểm tra 25 giây
            and len(shields) < MAX_SHIELDS  # Kiểm tra số lượng hiện tại
            and random.random() < shield_spawn_probability  # Kiểm tra xác suất
            ):
            shields.append(Shield())  # Thêm vật phẩm bảo vệ mới
            last_shield_time = pygame.time.get_ticks()  # Cập nhật thời gian

        # Thêm chướng ngại vật mới mỗi 1.5 giây
        if pygame.time.get_ticks() - last_obstacle_time > 1500:
            if random.choice([True, False]):
                obstacles.append(Obstacle("virus (2).png"))
            else:
                obstacles.append(Obstacle("cnv333.png"))
            last_obstacle_time = pygame.time.get_ticks()

        check_gap(obstacles)  # Kiểm tra và tạo khoảng cách giữa các vật thể

        # Cập nhật và vẽ tất cả đối tượng
        background.update()
        engineer.update()
        for item in items:
            item.update()
        # Nếu vật phẩm rời khỏi màn hình, tạo lại nó ở vị trí ngẫu nhiên bên phải màn hình
            if item.rect.x < -item.rect.width:
                item.rect.x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 300)
                item.rect.y = SCREEN_HEIGHT - 80
        for obstacle in obstacles: obstacle.update()
        for shield in shields: shield.update()  # Cập nhật vật phẩm bảo vệ

        # Kiểm tra va chạm với vật phẩm bảo vệ
        for shield in shields:
            if engineer.rect.colliderect(shield.rect):
                engineer.activate_shield()  # Kích hoạt vật phẩm bảo vệ khi ăn
                item_pickup_sound.play()  # Phát âm thanh ăn vật phẩm bảo vệ
                shield.rect.x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 300)  # Đặt lại vị trí vật phẩm bảo vệ

        # Kiểm tra va chạm với chướng ngại vật
        for obstacle in obstacles:
         if engineer.rect.colliderect(obstacle.rect):  # Kiểm tra va chạm giữa kĩ sư và chướng ngại vật
          if  engineer.has_shield:  # Nếu kĩ sư có lớp bảo vệ
            engineer.shield_count -= 1  # Giảm số lớp bảo vệ 1 đơn vị
            score = max(0, score - 30)  # Trừ 30 điểm, đảm bảo không xuống dưới 0
            if  engineer.shield_count <= 0:  # Nếu lớp bảo vệ hết
                 engineer.deactivate_shield()  # Tắt trạng thái bảo vệ
            
         # Đẩy chướng ngại vật ra khỏi màn hình
            obstacle.rect.x = SCREEN_WIDTH + 100
          else:  # Nếu không có lớp bảo vệ
            collision_sound.play()  # Phát âm thanh va chạm
            game_over_screen(score)  # Hiển thị màn hình kết thúc
            wait_for_restart()  # Chờ người chơi khởi động lại hoặc thoát
            running = False  # Dừng trò chơi
            break  # Thoát khỏi vòng lặp kiểm tra va chạm

 
        # Kiểm tra ăn vật phẩm
        for item in items:
            if  engineer.rect.colliderect(item.rect):
                score += 10
                item.rect.x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 300)
                item_pickup_sound.play()  # Phát âm thanh ăn vật phẩm
     

        # Xuất hiện vật phẩm bảo vệ mới mỗi 25 giây nếu đã đạt 70 điểm
        if reached_70_points and pygame.time.get_ticks() - shield_appearance_time >= last_shield_time:
            shields.append(Shield())  # Thêm vật phẩm bảo vệ mới
            shield_appearance_time = pygame.time.get_ticks()  # Cập nhật thời điểm vật phẩm xuất hiện

        # Vẽ tất cả đối tượng
        background.draw()
        engineer.draw()
        for item in items: item.draw() # vòng lặp vẽ từng đối tượng item trong danh sánh items 
        for obstacle in obstacles: obstacle.draw() #vòng lặp vẽ từng đối tượng obstacle trong danh sánh obstacles 
        for shield in shields: shield.draw()  # Vẽ vật phẩm bảo vệ 

        # Vẽ điểm và số lượng bảo vệ
        draw_score_and_shield_count(score, engineer.shield_count)

        pygame.display.flip()
        clock.tick(25) #chạy với 25 khung hình mỗi giây, mỗi giây trò chơi sẽ vẽ lại màn hình 25 lần, giữ tốc độ các vật thể không quá nhanh

# Hàm màn hình bắt đầu
def start_screen():
    start_image = pygame.image.load("start.jpg")
    start_image = pygame.transform.scale(start_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    start_button_rect = pygame.Rect(560,40,250, 50)  # Tọa độ và kích thước nút Start
    exit_button_rect = pygame.Rect(560,170, 250, 50) # Tọa độ và kích thước nút Exit

    while True:
        screen.fill(WHITE)
        screen.blit(start_image, (0, 0))

        # Vẽ viền đỏ cho nút Start và Exit để dễ xác định tọa độ
        #pygame.draw.rect(screen, RED, start_button_rect, 2)  # Viền đỏ nút Start
        #pygame.draw.rect(screen, RED, exit_button_rect, 2)   # Viền đỏ nút Exit

        pygame.display.flip()

        for event in pygame.event.get(): # xử lý các sự kiện do người dùng tác động vào
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Nhấn chuột trái
                    if start_button_rect.collidepoint(event.pos): #kiểm tra vị trí nhấn chuột trên màn hình có nhấn vào đúng tọa độ start không
                        return
                    if exit_button_rect.collidepoint(event.pos):  #kiểm tra vị trí nhấn chuột trên màn hình có nhấn vào đúng tọa độ exit không
                        pygame.quit()
                        exit()

# Hàm chờ người chơi bấm chuột trái để bắt đầu lại hoặc chuột phải để thoát
def wait_for_restart():
    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  # Đóng cửa sổ game
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Chuột trái (button 1)
                    main()  # Khởi động lại trò chơi khi bấm chuột trái
                    waiting_for_restart = False  # Dừng vòng lặp để khởi động lại trò chơi
                if event.button == 3:  # Chuột phải (button 3)
                    pygame.quit()
                    exit()  # Thoát game khi bấm chuột phải

# Chạy game
if __name__ == "__main__":
    start_screen()  # Hiển thị màn hình bắt đầu
    main()  # Khởi động trò chơi
