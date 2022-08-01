# api-interview

## Task
Hãy chỉnh sửa các file mã nguồn có sẵn để đáp ứng các yêu cầu sau:
* Xây dựng payload của jwt để có thể xác thực tài khoản khi login
* Khi login thì các jwt được tạo ra trước đó phải trở nên vô dụng ( jwt không sử dụng được )
* Có thể xem thông tin tài khoản đang login ( đang request với jwt ) với format: 
```json
{
    "name": "{last_name} {first_name}",
    "email": "{email}",
    "is_active": {is_active},
}
```


## Usage
Các file mã nguồn đã setup 3 endpoints:
- ```api/login/```: dùng để login và nhận được token
- ```api/verify-token/```: dùng để xác thực token có thể được sử dụng hay không
- ```api/me/```: dùng để xem thông tin user đang login

## Tests
Để có thể test các yêu cầu bạn có thể sử dụng lệnh ```pytest```


## Setup
* Clone repo về local
* Cài đặt requirements ( ```pip install -r requirements.txt``` )
* Tạo migrations ( ```python manage.py makemigrations``` )
* Migrate dữ liệu ( ```python manage.py migrate``` )
* Điều chỉnh các file cần thiết ( Những file có comment ```TODO:``` ) để hoàn thành task:
    - ```src/account/models.py```
    - ```src/account/services.py```
    - ```src/core/jwt.py```
    - ```src/api/serializers/login.py```


## Deadlines
Những commit vào trước 12:00 ngày 03/08/2022 sẽ được tính vào bài test này


## Note
Nhớ hãy tạo một nhánh khác để push code

