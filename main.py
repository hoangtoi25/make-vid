from moviepy import *
import random
import os
from PIL import Image, ImageDraw
import numpy as np
import hashlib

def create_rounded_rectangle(width, height, radius):
    """Create a rounded rectangle image as a NumPy array."""
    # Create a blank image with transparent background
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw a rounded rectangle
    draw.rounded_rectangle([0, 0, width, height], radius=radius, fill=(255, 255, 255, 255))

    # Convert PIL Image to NumPy array
    img_np = np.array(img)
    return ImageClip(img_np).with_duration(1)  # Set a default duration

def create_arrow_image():
    # Tạo ảnh 100x150 pixel
    img = Image.new('RGBA', (100, 150), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Vẽ mũi tên với các tọa độ phù hợp
    draw.polygon([(50, 10), (90, 70), (70, 70), (70, 150),
                   (30, 150), (30, 70), (10, 70)], fill="red")

    return np.array(img)  # Trả về ảnh dưới dạng mảng NumPy

def create_slideshow_with_background(images_list, videos_list, audio_file, background_video_file, text, output_file):
    background_clip = VideoFileClip(background_video_file).resized(height=1920)
    background_clip = background_clip.cropped(width=1080, height=1920, x_center=background_clip.w / 2)

    # Tạo các clips từ ảnh
    # Kết hợp ảnh và video vào list clips
    clips = []
    videos_duration = 0
    # Kiểm tra nếu số lượng clip chưa đạt 13
    while len(clips) < 13:
        for img in images_list:
            clip = ImageClip(img).resized(width=0.85 * background_clip.w).with_duration(3.5)
            clips.append(clip)
            if len(clips) >= 13:  # Ngừng khi đã đủ 13 clip
                break

    duration = 45
    background_clip = background_clip.with_duration(duration)

    # Tạo hiệu ứng chuyển tiếp (crossfade)
    transitions = [clip.with_effects([vfx.FadeIn(0.5)]) for clip in clips]  # Hiệu ứng chuyển đổi

    # Kết hợp các clips
    slideshow = concatenate_videoclips(transitions, method="compose").resized(width=0.85 * background_clip.w).with_duration(duration).with_position(("center", 25))

    # Create a rounded rectangle background for the text
    text_width = int(0.85 * background_clip.w)
    text_height = int(background_clip.h * 1 / 3)  # Height of the text background
    radius = 50  # Radius for rounded corners
    rounded_bg = create_rounded_rectangle(text_width - 50, text_height, radius)
    rounded_bg = rounded_bg.with_position(("center", int(background_clip.h * 1 / 2) + 30)).with_duration(duration)

    # paste emoji
    overlay_image = ImageClip('icon/sp1.png').resized((110, 110)).with_position((rounded_bg.w - 60 - 30, int(background_clip.h * 1 / 2) + 30 + 30)).with_duration(duration)

    # Create a text clip
    text_clip = TextClip(
        text=text,
        font_size=90,
        color='black',
        size=(text_width - 50, text_height),
        font=r"C:\Windows\Fonts\arialbd.ttf",
        bg_color='rgba(0, 0, 0, 0)',
        interline=15
    )
    text_clip = text_clip.with_position(("center", int(background_clip.h * 1 / 2) + 30)).with_duration(duration)  # Adjust position for padding

    # Tạo mũi tên và chuyển đổi thành clip
    arrow_image = create_arrow_image()  # Tạo mũi tên
    arrow_clip = ImageClip(arrow_image, is_mask=False)
    arrow_clip = arrow_clip.resized(height=300).rotated(135)

    def arrow_position(t):
        amplitude = 50  # Biên độ rung
        y_position = 1450 + amplitude * np.sin(2 * np.pi * t)  # Rung xung quanh 1400
        return (80, y_position)  # X=50, Y theo hàm

    arrow_animation = arrow_clip.with_position(arrow_position).with_duration(duration)  # Gán hàm vị trí

    # Combine all clips
    video = CompositeVideoClip([background_clip, slideshow, rounded_bg, overlay_image, text_clip, arrow_animation])
    audio = AudioFileClip(audio_file).subclipped(0, duration)  # Use the same duration for audio
    video = video.with_audio(audio)

    # Export video with settings similar to phone camera video
    video.write_videofile(output_file, fps=24, codec='libx264', audio_codec='aac')

def generate_multiple_videos(images_list, videos_list, audio_list, background_video_list, text, output_dir, number_of_videos):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in range(number_of_videos):
        selected_audio = random.choice(audio_list)
        selected_background = random.choice(background_video_list)

        output_file = os.path.join(output_dir, f"{create_uid(selected_audio, selected_background, text)}.mp4")
        create_slideshow_with_background(images_list, videos_list, selected_audio, selected_background, text, output_file)

def create_uid(audio, background, text):
    combined_text = f"{audio}-{background}-{text}"
    uid = hashlib.sha256(combined_text.encode()).hexdigest()

    return uid

# Danh sách ảnh, âm thanh, Video nền
images_list = [os.path.join("image", filename) for filename in os.listdir("image") if filename.endswith(('.jpg', '.jpeg', '.png'))]
videos_list = [os.path.join("image", filename) for filename in os.listdir("image") if filename.endswith(('.mp4'))]
audio_list = [os.path.join("audio/long", filename) for filename in os.listdir("audio/long") if filename.endswith(('.mp3', '.wav', '.ogg'))]
background_video_list = [os.path.join("background/long", filename) for filename in os.listdir("background/long") if filename.endswith(('.mp4'))]

# Đoạn text để hiển thị
# text = "Cứu em!!!\nTiểu cảnh hồ cá\ngiá chỉ từ 54k\nXức xắc\nHốt luôn"
# text = "Xức xắc!!!\nCầu cảnh cho hồ cá\ngiá chỉ từ 38k\nNhiều size\nHốt luôn"
# text = "Cứu em!!!\nRẻ thật đấy\n87k nửa cân\nXức xắc\nHốt luôn"
# text = "Đẹp quá!!!\nĐầu rồng mẫu mới\n65k quá rẻ\nXức xắc\nHốt luôn"
# text = "Cứu em!!!\nNúi đá uốn vòm\nchỉ từ 112k\nXức xắc\nHốt luôn"
# text = "Cứu em!!!\nTiểu cảnh mới về\nchỉ từ 85k\nXức xắc\nHốt luôn"
# text = "Xức xắc!!!\nGuồng xoay oxy\ngiá chỉ từ 52k\nXức xắc\nHốt luôn"
text = "Xức xắc!!!\nCây rỗng cho cá\ngiá chỉ từ 32k\nXức xắc\nHốt luôn"

#bi vi pham
# text = "Hot quá!!!\nMẫu bình cổ mới\ngiá chỉ từ 54k\nXức xắc\nHốt luôn"
# text = "Cứu em!!!\nTàu đắm mẫu mới\ngiá chỉ từ 37k\nXức xắc\nHốt luôn"
# text = "Xức xắc!!!\nTiểu cảnh lớn\ngiá chỉ từ 78k\nĐẹp miễn chê\nHốt luôn"



# Thư mục để lưu các video xuất ra
output_dir = os.path.join(os.path.expanduser("~"), "Videos", "make-vid")

# Tạo 5 video liveshow
generate_multiple_videos(images_list, videos_list, audio_list, background_video_list, text, output_dir, number_of_videos=4)