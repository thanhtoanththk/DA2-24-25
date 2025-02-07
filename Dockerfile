# Sử dụng image Python chính thức từ Docker Hub
FROM python:3.11-slim

# Cài đặt thư viện hệ thống cần thiết
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Copy yêu cầu cài đặt vào container
COPY requirements.txt .
RUN pip install --upgrade pip
# Cài đặt các thư viện Python cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn vào container
COPY . .
RUN chmod -R 755 /app

# Cài đặt biến môi trường FLASK_APP cho ứng dụng
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Kiểm tra nếu thư mục migrations không tồn tại thì tạo
RUN if [ ! -d "migrations" ]; then flask db init; fi

# Mở cổng 5000 để chạy Flask app
EXPOSE 5001

# Chạy ứng dụng Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
