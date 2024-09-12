from moviepy.editor import *  
import random  
import os  
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"}) 
from PIL import Image, ImageDraw  
import numpy as np  
import hashlib  
import numpy as np  
from moviepy.video.fx.all import resize 

def create_rounded_rectangle(width, height, radius):  
    """Create a rounded rectangle image as a NumPy array."""  
    # Create a blank image with transparent background  
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))  
    draw = ImageDraw.Draw(img)  

    # Draw a rounded rectangle  
    draw.rounded_rectangle([0, 0, width, height], radius=radius, fill=(255, 255, 255, 255))  

    # Convert PIL Image to NumPy array  
    img_np = np.array(img)  
    return ImageClip(img_np).set_duration(1)  # Set a default duration  

def create_arrow_image():  
    # Tạo ảnh 100x150 pixel  
    img = Image.new('RGBA', (100, 150), (255, 255, 255, 0))  
    draw = ImageDraw.Draw(img)  
    
    # Vẽ mũi tên với các tọa độ phù hợp  
    draw.polygon([(50, 10), (90, 70), (70, 70), (70, 150),   
                   (30, 150), (30, 70), (10, 70)], fill="red")  
    
    return np.array(img)  # Trả về ảnh dưới dạng mảng NumPy  

def create_slideshow_with_background(images_list, audio_file, background_video_file, text, output_file):  
    background_clip = VideoFileClip(background_video_file).resize(height=1920)  
    background_clip = background_clip.crop(width=1080, height=1920, x_center=background_clip.w / 2)  

    # Get the duration of the background video  
    duration = background_clip.duration  
    
    # Tạo các clips từ ảnh  
    clips = [ImageClip(img).resize(width=0.85 * background_clip.w).set_duration(duration / 3 - 0.1)  
             for img in images_list]  

    # Tạo hiệu ứng chuyển tiếp (crossfade)  
    transitions = [clip.fadein(0.3) for clip in clips]  # Hiệu ứng chuyển đổi  

    # Kết hợp các clips  
    slideshow = concatenate_videoclips(transitions, method="compose").resize(width=0.85 * background_clip.w).set_duration(duration).set_position(("center", 25)) 

    # Create a rounded rectangle background for the text  
    text_width = int(0.85 * background_clip.w)
    text_height = int(background_clip.h * 1 / 3)  # Height of the text background  
    radius = 50  # Radius for rounded corners  
    rounded_bg = create_rounded_rectangle(text_width - 50, text_height, radius)  
    rounded_bg = rounded_bg.set_position(("center", int(background_clip.h * 1 / 2) + 30)).set_duration(duration)  

    # paste emoji
    overlay_image = ImageClip('icon/sp1.png').resize((110, 110)).set_position((rounded_bg.w - 60 - 30, int(background_clip.h * 1 / 2) + 30 + 30)).set_duration(duration)  

    # Create a text clip  
    text_clip = TextClip(text, fontsize=90, color='black', size=(text_width - 50, text_height), font='Arial-Bold', bg_color='rgba(0, 0, 0, 0)', interline=15)  
    text_clip = text_clip.set_position(("center", int(background_clip.h * 1 / 2) + 30)).set_duration(duration)  # Adjust position for padding 

    # Tạo mũi tên và chuyển đổi thành clip  
    arrow_image = create_arrow_image()  # Tạo mũi tên  
    arrow_clip = ImageClip(arrow_image, ismask=False)
    arrow_clip = arrow_clip.resize(height=300).rotate(135)

    def arrow_position(t):  
        amplitude = 50  # Biên độ rung  
        y_position = 1450 + amplitude * np.sin(2 * np.pi * t)  # Rung xung quanh 1400  
        return (80, y_position)  # X=50, Y theo hàm  

    arrow_animation = arrow_clip.set_position(arrow_position).set_duration(duration)  # Gán hàm vị trí

    # Combine all clips  
    video = CompositeVideoClip([background_clip, slideshow, rounded_bg, overlay_image, text_clip, arrow_animation])  
    audio = AudioFileClip(audio_file).subclip(0, duration)  # Use the same duration for audio  
    video = video.set_audio(audio)  

    # Export video with settings similar to phone camera video  
    video.write_videofile(output_file, fps=30, codec='libx264', audio_codec='aac') 

def generate_multiple_videos(images_list, audio_list, background_video_list, text, output_dir, number_of_videos):  
    if not os.path.exists(output_dir):  
        os.makedirs(output_dir)  
    
    for i in range(number_of_videos):  
        # selected_image = random.choice(images_list)  
        selected_audio = random.choice(audio_list)
        selected_background = random.choice(background_video_list)
        
        output_file = os.path.join(output_dir, f"{create_uid(selected_audio, selected_background, text)}.mp4")  
        create_slideshow_with_background(images_list, selected_audio, selected_background, text, output_file)  

def create_uid(audio, background, text):  
    combined_text = f"{audio}-{background}-{text}"  
    uid = hashlib.sha256(combined_text.encode()).hexdigest()      

    return uid

# Danh sách ảnh, âm thanh, Video nền
images_list = [os.path.join("image", filename) for filename in os.listdir("image") if filename.endswith(('.jpg', '.jpeg', '.png'))]  
audio_list = [os.path.join("audio", filename) for filename in os.listdir("audio") if filename.endswith(('.mp3', '.wav', '.ogg'))]  
background_video_list = [os.path.join("background", filename) for filename in os.listdir("background") if filename.endswith(('.mp4'))]  

# Đoạn text để hiển thị  
text = "Cứu em!!!\nTiểu cảnh hồ cá\ngiá chỉ từ 54k\nXức xắc\nHốt luôn"  
# text = "Đẹp quá!!!\nCầu cảnh cho hồ cá\ngiá chỉ từ 38k\nXức xắc\nHốt luôn" 
# text = "Hot quá!!!\nMẫu bình cổ mới\ngiá chỉ từ 54k\nXức xắc\nHốt luôn"  
# text = "Xức xắc!!!\nTiểu cảnh lớn\ngiá chỉ từ 78k\nĐẹp miễn chê\nHốt luôn"  
# text = "Cứu em!!!\nTàu đắm mới về\ngiá chỉ từ 37k\nXức xắc\nHốt luôn"  
# text = "Cứu em!!!\nRẻ nhất tiktok\n87k nửa cân\nXức xắc\nHốt luôn"  
# text = "Đẹp quá!!!\nĐầu rồng mẫu mới\n65k quá rẻ\nXức xắc\nHốt luôn"  

# Thư mục để lưu các video xuất ra  
output_dir = os.path.join(os.path.expanduser("~"), "Videos", "make-vid")  

# Tạo 5 video liveshow  
generate_multiple_videos(images_list, audio_list, background_video_list, text, output_dir, number_of_videos=3)