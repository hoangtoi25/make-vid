# Cài đặt ffmpeg: https://www.gyan.dev/ffmpeg/builds/

choco install ffmpeg-full

# Tạo thư mục

mkdir "$env:USERPROFILE\ffmpeg" -Force

# Tải ffmpeg

Invoke-WebRequest -Uri "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip" -OutFile "$env:USERPROFILE\ffmpeg\ffmpeg.zip"

# Giải nén

Expand-Archive "$env:USERPROFILE\ffmpeg\ffmpeg.zip" -DestinationPath "$env:USERPROFILE\ffmpeg" -Force

# Thêm vào PATH

$binPath = (Get-ChildItem "$env:USERPROFILE\ffmpeg\ffmpeg-\*-essentials_build\bin" | Select-Object -First 1).FullName
[Environment]::SetEnvironmentVariable("PATH", "$env:PATH;$binPath", "User")
