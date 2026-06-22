import socket
import os
import re
import subprocess

def get_lan_ip():
    """Tự động lấy địa chỉ IP mạng LAN của máy tính hiện tại"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Không cần kết nối thật, chỉ mượn hàm để xác định IP Outbound interface
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def update_flutter_config(ip):
    """Tự động cập nhật IP vào các file cấu hình của Flutter"""
    # Định nghĩa đường dẫn tương đối tới source Flutter (Bạn điều chỉnh lại cho đúng cấu trúc thư mục)
    flutter_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend')) 
    
    # 1. Cập nhật file app_config.dart
    app_config_path = os.path.join(flutter_dir, 'lib/config/app_config.dart')
    if os.path.exists(app_config_path):
        with open(app_config_path, 'w', encoding='utf-8') as f:
            f.write(f"class AppConfig {{\n  static const apiUrl = 'http://{ip}:8000';\n}}\n")
        print(f"[✓] Đã cập nhật app_config.dart -> http://{ip}:8000")

    # 2. Cập nhật file api_service.dart
    api_service_path = os.path.join(flutter_dir, 'lib/services/api_service.dart')
    if os.path.exists(api_service_path):
        with open(api_service_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Dùng Regex để tìm và thay thế dòng gán baseUrl
        updated_content = re.sub(
            r"static const String baseUrl = 'http://.*?';\n",
            f"static const String baseUrl = 'http://{ip}:8000';\n",
            content
        )
        with open(api_service_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"[✓] Đã cập nhật api_service.dart -> http://{ip}:8000")

if __name__ == "__main__":
    current_ip = get_lan_ip()
    print(f"[*] Phát hiện IP hệ thống mạng LAN: {current_ip}")
    
    # Tiến hành cập nhật tự động vào Flutter
    update_flutter_config(current_ip)
    
    # Lấy đường dẫn tuyệt đối của chính thư mục chứa file run.py này
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    
    print(f"[*] Đang khởi chạy Uvicorn Server tại http://{current_ip}:8000")
    
    # Bổ sung tham số cwd (Current Working Directory) để ép Uvicorn chạy đúng vị trí
    subprocess.run(
        ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
        cwd=backend_dir
    )