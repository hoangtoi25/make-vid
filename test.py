from moviepy.editor import *  
import numpy as np  

# Tạo một hàm để tạo nền lấp lánh với ngôi sao nhấp nháy  
def make_starry_background(size, num_stars, star_size=5):  
    # Khởi tạo một khung hình đen  
    background = np.zeros((size[1], size[0], 3), dtype=np.uint8)  
    
    # Tạo các ngôi sao với tọa độ ngẫu nhiên  
    for _ in range(num_stars):  
        x = np.random.randint(0, size[0])  
        y = np.random.randint(0, size[1])  
        
        # Vẽ hình ngôi sao  
        points = [(0, -2), (1, 1), (2, 1), (0, 2), (1, -1), (-1, -1), (-2, 1), (-1, 1)]  
        for dx, dy in points:  
            # Tính tọa độ ngôi sao  
            nx, ny = x + dx * star_size, y + dy * star_size  
            
            # Đảm bảo không ra ngoài  
            if 0 <= nx < size[0] and 0 <= ny < size[1]:  
                intensity = np.random.randint(200, 255)  # Độ sáng ngôi sao  
                background[ny, nx] = [intensity, intensity, intensity]  # Màu đỏ  

    return background  

# Tạo hiệu ứng nhấp nháy  
def create_flashing_stars(background, frames):  
    for frame in range(frames):  
        factor = (np.sin(frame * 2 * np.pi / 30) + 1) / 2  # Tính toán độ sáng thay đổi  
        flashing_background = background.copy()  
        
        # Thay đổi độ sáng của ngôi sao  
        for y in range(flashing_background.shape[0]):  
            for x in range(flashing_background.shape[1]):  
                if np.any(flashing_background[y, x]):  # Nếu pixel có màu  
                    flashing_background[y, x] = (flashing_background[y, x] * factor).astype(np.uint8)  
        
        yield flashing_background  # Trả về khung hình nhấp nháy  

# Kích thước video  
width, height = 1080, 1920  
num_stars = 100  # Số lượng ngôi sao  

# Tạo video nền lấp lánh  
background = make_starry_background((width, height), num_stars, star_size=5)  
starry_bg_clip = ImageClip(background).set_duration(5)  # Độ dài video nền  

# Tạo video chính của bạn (thay thế bằng video của bạn)  
main_video_clip = VideoFileClip("background/3059073-hd_1920_1080_24fps.mp4").resize(height=1920).subclip(0, 5)  
main_video_clip = main_video_clip.crop(width=1080, height=1920, x_center=main_video_clip.w / 2)  

# Tạo khung hình nhấp nháy  
frames = [ImageClip(frame).set_duration(1/24) for frame in create_flashing_stars(background, 120)]  # Giả sử 120 khung hình  

# Kết hợp video chính với nền lấp lánh  
final_video = CompositeVideoClip([starry_bg_clip])  

# Lưu video  
final_video.write_videofile("output_video.mp4", fps=24)