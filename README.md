# Kích hoạt môi trường ảo

.venv\Scripts\Activate.ps1

# Thoát env

deactivate

# Cài đặt ffmpeg

choco install ffmpeg-full

# Cài đặt thư viện

pip install -r requirements.txt

# Tạo lại môi trường

Remove-Item .venv -Recurse -Force
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
