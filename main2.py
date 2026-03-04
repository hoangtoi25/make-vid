from moviepy import *
import random
import os
from PIL import Image, ImageDraw
import numpy as np
import hashlib

FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
FONT_BOLD_ITALIC = r"C:\Windows\Fonts\arialbi.ttf"

def create_rounded_rectangle(width, height, radius):
    """Create a rounded rectangle image as a NumPy array with a 70% opaque background."""
    # Create a blank image with transparent background
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Draw a rounded rectangle with 70% opacity
    opacity = 178  # Approximately 70% opacity
    draw.rounded_rectangle([0, 0, width, height], radius=radius, fill=(255, 255, 255, opacity))

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

def create_slideshow_with_background(image_file, audio_file, background_video_file, title, text_clip_1, text_clip_2, output_file):
    background_clip = VideoFileClip(background_video_file).resized(height=1920)
    audio = AudioFileClip(audio_file)
    background_clip = background_clip.cropped(width=1080, height=1920, x_center=background_clip.w / 2)
    duration = background_clip.duration if (background_clip.duration < audio.duration) else audio.duration
    if duration > 30:
        duration = random.randint(31, 35)
    audio = audio.subclipped(0, duration)
    background_clip = background_clip.with_duration(duration)

    # Create a rounded rectangle background for the content
    layer_width = int(0.9 * background_clip.w)
    layer_height = int(background_clip.h * 4 / 10)  # Height of the text background
    radius = 50  # Radius for rounded corners
    rounded_bg = create_rounded_rectangle(layer_width, layer_height, radius)
    rounded_bg = rounded_bg.with_position(("center", "center")).with_duration(duration)

    # Create text title layout
    text_clip_title = TextClip(
        text=title,
        font_size=110,
        color='red',
        font=FONT_BOLD,
        bg_color='rgba(0, 0, 0, 0)',
        interline=15
    )
    text_clip_title = text_clip_title.with_duration(duration).with_position(("center", background_clip.h * 3 / 10 - 150))

    # Create main image
    image_clip_1 = ImageClip(image_file).resized(width=0.33 * layer_width).with_duration(duration)
    def move_image_1(t):
        y = int(background_clip.h * 3 / 10) + 30 + 10 * np.sin(2 * np.pi * t / 2)  # Sử dụng hàm sin để tạo chuyển động qua lại
        return int(0.6 * background_clip.w), y  # Tuyến x, y trong một hệ tọa độ
    image_clip_1 = image_clip_1.with_position(move_image_1)

    image_clip_2 = ImageClip(image_file).resized(width=0.33 * layer_width).with_duration(duration)
    def move_image_2(t):
        y = int(background_clip.h * 1 / 2) + 30 + 10 * np.sin(2 * np.pi * t / 2)
        return int(0.6 * background_clip.w), y
    image_clip_2 = image_clip_2.with_position(move_image_2)

    # Create a text clip
    layer_width_text = int(0.05 * background_clip.w) + 30
    layer_height_text_1 = int(background_clip.h * 3 / 10) + int(layer_height * 1 / 4) - 60
    layer_height_text_2 = int(background_clip.h * 3 / 10) + int(layer_height * 1 / 4) + 40
    layer_height_text_3 = int(background_clip.h * 7 / 10) - int(layer_height * 1 / 4) - 120
    layer_height_text_4 = int(background_clip.h * 7 / 10) - int(layer_height * 1 / 4) - 20
    text_clip_1_clip = TextClip(
        text=text_clip_1,
        font_size=90,
        color='red',
        font=FONT_BOLD,
        bg_color='rgba(0, 0, 0, 0)',
        interline=15
    )
    text_clip_1_clip = text_clip_1_clip.with_duration(duration).with_position((layer_width_text + 160, layer_height_text_1))
    text_bottom_1 = TextClip(
        text="(Còn chê)",
        font_size=90,
        color='black',
        font=FONT_BOLD_ITALIC,
        interline=15
    )
    text_bottom_1 = text_bottom_1.with_duration(duration).with_position((layer_width_text + 30, layer_height_text_2))
    text_clip_2_clip = TextClip(
        text=text_clip_2,
        font_size=90,
        color='red',
        font=FONT_BOLD,
        bg_color='rgba(0, 0, 0, 0)',
        interline=15
    )
    text_clip_2_clip = text_clip_2_clip.with_duration(duration).with_position((layer_width_text + 160, layer_height_text_3))
    def animate_scale(t):
        scale = 1 + 0.05 * np.sin(15 * np.pi * t / duration)  # Thay đổi kích thước theo hàm sin
        return scale
    text_clip_2_clip = text_clip_2_clip.resized(animate_scale)
    text_bottom_2 = TextClip(
        text="(Múc ngay)",
        font_size=90,
        color='black',
        font=FONT_BOLD_ITALIC,
        interline=15
    )
    text_bottom_2 = text_bottom_2.with_duration(duration).with_position((layer_width_text, layer_height_text_4))

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
    video = CompositeVideoClip([background_clip, rounded_bg, image_clip_1, image_clip_2, text_clip_title, text_clip_1_clip, text_bottom_1, text_clip_2_clip, text_bottom_2, arrow_animation])
    video = video.with_audio(audio)

    # Export video with settings similar to phone camera video
    video.write_videofile(output_file, fps=24, codec='libx264', audio_codec='aac')

def generate_multiple_videos(images_list, audio_list, background_video_list, title, text_1, text_2, output_dir, number_of_videos):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in range(number_of_videos):
        selected_image = random.choice(images_list)
        selected_audio = random.choice(audio_list)
        selected_background = random.choice(background_video_list)

        output_file = os.path.join(output_dir, f"{create_uid(selected_image, selected_background)}.mp4")
        create_slideshow_with_background(selected_image, selected_audio, selected_background, title, text_1, text_2, output_file)

def create_uid(image, background):
    combined_text = f"{image}-{background}"
    uid = hashlib.sha256(combined_text.encode()).hexdigest()

    return uid

# Danh sách ảnh, âm thanh, Video nền
images_list = [os.path.join("image", filename) for filename in os.listdir("image") if filename.endswith(('.jpg', '.jpeg', '.png'))]
audio_list = [os.path.join("audio/long", filename) for filename in os.listdir("audio/long") if filename.endswith(('.mp3', '.wav', '.ogg'))]
background_video_list = [os.path.join("background/long", filename) for filename in os.listdir("background/long") if filename.endswith(('.mp4'))]

# Đoạn text để hiển thị
text_title = "Mô Hình Tàu Đắm"
text_1 = "80k"
text_2 = "55k"

# Thư mục để lưu các video xuất ra
output_dir = os.path.join(os.path.expanduser("~"), "Videos", "make-vid")

# Tạo 5 video liveshow
generate_multiple_videos(images_list, audio_list, background_video_list, text_title, text_1, text_2, output_dir, number_of_videos=5)