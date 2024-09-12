import cv2  

def remove_white_border(image_file):
    # Tải ảnh bằng OpenCV  
    image = cv2.imread(image_file)  

    # Chuyển đổi sang ảnh xám  
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  

    # Phát hiện viền  
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)  

    # Tìm contours  
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  

    # Lấy bounding box  
    x, y, w, h = cv2.boundingRect(contours[0])  

    # Cắt ảnh  
    cropped_image = image[y:y+h, x:x+w]  

    # Lưu lại ảnh đã cắt  
    cv2.imwrite("image_file.jpg", cropped_image) 