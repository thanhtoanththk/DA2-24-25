# Hướng dẫn cài đặt Docker và Docker Compose

## 1. Cài đặt Docker Desktop

Để cài đặt Docker Desktop, vui lòng tham khảo hướng dẫn tại liên kết dưới đây:

[Hướng dẫn cài đặt Docker Desktop](https://www.docker.com/products/docker-desktop)

## 2. Cài đặt Docker Compose

Để cài đặt Docker Compose, vui lòng tham khảo hướng dẫn tại liên kết dưới đây:

[Hướng dẫn cài đặt Docker Compose](https://docs.docker.com/compose/install/)

## 3. Hướng dẫn sử dụng file `app.sh` để quản lý ứng dụng Flask

File `app.sh` cho phép bạn dễ dàng start, stop hoặc restart ứng dụng Flask của bạn thông qua Docker. Sau đây là các lệnh bạn có thể sử dụng:

### 3.1 Cấp quyền thực thi cho file `app.sh`

Trước khi sử dụng file `app.sh`, bạn cần cấp quyền thực thi cho file này bằng lệnh sau:

```bash
chmod +x app.sh

### 3.2 Start Flask app

Để bắt đầu ứng dụng Flask với Docker, chạy lệnh sau:

```bash
./app.sh start

### 3.3 Stop Flask app

Để dừng ứng dụng Flask với Docker, chạy lệnh sau:

```bash
./app.sh stop
