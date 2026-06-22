import socket

# Tạo socket hứng mọi IP ngoại vi truyền vào qua cổng 8000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 8000))
s.listen(1)
print("⏳ PC đang mở cổng 8000 đợi tín hiệu từ điện thoại...")

# Treo máy đợi điện thoại bấm gửi kết nối
conn, addr = s.accept()
print(f"📡 Điện thoại kết nối thành công từ IP: {addr[0]}")
print(f"📩 Nội dung nhận được: {conn.recv(1024).decode('utf-8')}")
conn.close()