# 👟 Shop Sneaker Django

[![Django](https://img.shields.io/badge/Django-5.0.6-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.0-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Một ứng dụng thương mại điện tử hiện đại chuyên bán giày sneaker được xây dựng bằng Django với giao diện đa ngôn ngữ và tính năng thanh toán PayPal.

## 🌟 Tính Năng Nổi Bật

### 🛍️ Ecommerce Core
- **Quản lý sản phẩm đầy đủ** với variants (size, màu sắc)
- **Giỏ hàng thông minh** với session-based storage
- **Hệ thống thanh toán** tích hợp PayPal
- **Quản lý đơn hàng** cho cả user đã đăng ký và guest

### 👤 Quản Lý Người Dùng
- **Đăng ký/Đăng nhập** với email verification
- **Dashboard cá nhân** với quản lý profile
- **Reset password** qua email
- **Theo dõi đơn hàng** và lịch sử mua hàng

### 🌐 Đa Ngôn Ngữ & Theme
- **Hỗ trợ 2 ngôn ngữ**: Tiếng Việt (mặc định) và English
- **Theme switching**: Light/Dark mode
- **Responsive design** với Bootstrap 5

### 🎨 Giao Diện Hiện Đại
- **Material Design** admin interface
- **FontAwesome icons**
- **Bootstrap 5 Flatly theme**
- **Mobile-first responsive**

## 📸 Screenshots

```
[Thêm screenshots của ứng dụng ở đây]
```

## 🚀 Cài Đặt Nhanh

### Yêu Cầu Hệ Thống
- Python 3.8+
- Django 5.0.6
- SQLite (development) / PostgreSQL (production)

### 1. Clone Repository
```bash
git clone https://github.com/username/ShopSneaker_Django.git
cd ShopSneaker_Django
```

### 2. Tạo Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Cài Đặt Dependencies
```bash
pip install -r requirements.txt
```

### 4. Cấu Hình Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Tạo Superuser
```bash
python manage.py createsuperuser
```

### 6. Load Sample Data (Optional)
```bash
python manage.py populate_sample_data
```

### 7. Chạy Development Server
```bash
python manage.py runserver
```

Truy cập: `http://127.0.0.1:8000/`

## 📁 Cấu Trúc Dự Án

```
ShopSneaker_Django/
│
├── 📁 ShopSneaker/           # Main project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── 📁 store/                 # Quản lý sản phẩm
│   ├── models.py            # Product, Category, Brand, etc.
│   ├── views.py             # Store views & filtering
│   ├── admin.py             # Admin customization
│   └── templates/store/
│
├── 📁 cart/                  # Giỏ hàng
│   ├── cart.py              # Session-based cart logic
│   ├── views.py             # Cart operations
│   └── templates/cart/
│
├── 📁 account/               # Quản lý người dùng
│   ├── forms.py             # Registration & profile forms
│   ├── views.py             # Authentication & profile
│   └── templates/account/
│
├── 📁 payment/               # Thanh toán
│   ├── models.py            # Order, OrderItem, ShippingAddress
│   ├── views.py             # Checkout & PayPal integration
│   └── templates/payment/
│
├── 📁 static/                # Static files
│   ├── css/
│   ├── js/
│   └── media/
│
├── 📁 locale/                # Internationalization
│   ├── en/LC_MESSAGES/
│   └── vi/LC_MESSAGES/
│
├── 📄 requirements.txt       # Python dependencies
├── 📄 manage.py             # Django management
└── 📄 db.sqlite3           # Database file
```

## 🛠️ Cấu Hình

### Environment Variables
Tạo file `.env` trong root directory:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Production)
DATABASE_URL=postgres://user:password@localhost:5432/shopdb

# Email Configuration
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# PayPal
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-client-secret
```

### PayPal Setup
1. Tạo tài khoản PayPal Developer
2. Tạo application và lấy Client ID
3. Cập nhật `PAYPAL_CLIENT_ID` trong settings

### Email Configuration
1. Bật 2-Factor Authentication cho Gmail
2. Tạo App Password
3. Cập nhật email settings trong `settings.py`

## 🎯 Sử Dụng

### Admin Panel
- Truy cập: `http://127.0.0.1:8000/admin/`
- Quản lý sản phẩm, đơn hàng, người dùng
- Material Design interface

### Store Features
- **Trang chủ**: Hiển thị sản phẩm featured và mới
- **Danh mục**: Lọc sản phẩm theo category
- **Tìm kiếm**: Search products by name, description
- **Chi tiết sản phẩm**: Product variants, reviews, wishlist

### User Features
- **Đăng ký**: Email verification required
- **Profile**: Update personal information
- **Orders**: Track order history
- **Wishlist**: Save favorite products

## 🗃️ Database Schema

### Core Models

#### Product Model
```python
class Product(models.Model):
    sku = CharField(unique=True)
    title = CharField(max_length=255)
    category = ForeignKey(Category)
    brand = ForeignKey(Brand)
    original_price = DecimalField()
    sale_price = DecimalField(optional)
    stock_quantity = PositiveIntegerField()
    # ... và nhiều fields khác
```

#### User-related Models
- `User` (Django built-in)
- `ShippingAddress` (payment app)
- `Wishlist` (store app)

#### Order Models
- `Order`
- `OrderItem`
- `ShippingAddress`

## 🌐 API Endpoints

### Public Endpoints
```
GET  /                          # Homepage
GET  /category/<slug>/          # Category products
GET  /product/<slug>/           # Product detail
GET  /cart/                     # Cart summary
```

### Authentication Required
```
GET  /account/dashboard/        # User dashboard
POST /cart/add/                 # Add to cart
POST /payment/checkout/         # Checkout process
GET  /account/orders/           # Order history
```

## 🧪 Testing

### Chạy Tests
```bash
# Chạy tất cả tests
python manage.py test

# Test specific app
python manage.py test store
python manage.py test account
```

### Test Coverage
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Tạo HTML report
```

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure proper database (PostgreSQL)
- [ ] Set up environment variables
- [ ] Configure static files serving
- [ ] Set up SSL certificate
- [ ] Configure email backend
- [ ] Set up monitoring và logging

### Docker Deployment
```dockerfile
# Dockerfile example
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "ShopSneaker.wsgi:application"]
```

### Heroku Deployment
```bash
# Install Heroku CLI
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
heroku run python manage.py migrate
```

## 🤝 Contributing

### Development Setup
1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

### Coding Standards
- Follow PEP 8 for Python code
- Use meaningful variable và function names
- Write docstrings for functions và classes
- Add comments for complex logic

## 📝 Changelog

### Version 1.0.0 (Current)
- ✅ Basic ecommerce functionality
- ✅ User authentication system
- ✅ PayPal payment integration
- ✅ Multi-language support
- ✅ Theme switching
- ✅ Admin material dashboard

### Planned Features
- 🔄 Advanced search filters
- 🔄 Product recommendations
- 🔄 Social media login
- 🔄 Mobile app API
- 🔄 Analytics dashboard

## ⚠️ Known Issues

1. **PayPal Client ID**: Hardcoded trong template (cần move to environment variables)
2. **Email Settings**: Empty trong production settings
3. **Debug Mode**: Enabled trong production (cần disable)
4. **Secret Key**: Exposed trong code (cần secure)

## 🐛 Bug Reports

Nếu bạn tìm thấy bug, vui lòng tạo issue với:
- Mô tả chi tiết bug
- Steps để reproduce
- Expected vs actual behavior
- Screenshots (nếu có)
- Environment info (OS, Python version, etc.)

## 💡 Feature Requests

Để đề xuất tính năng mới:
1. Check existing issues trước
2. Tạo issue với label "enhancement"
3. Mô tả detailed use case
4. Explain tại sao feature này hữu ích

## 📚 Documentation

### API Documentation
- [API Docs](docs/api.md) - Detailed API documentation
- [Database Schema](docs/database.md) - Database design
- [Deployment Guide](docs/deployment.md) - Production deployment

### Tutorials
- [Getting Started](docs/getting-started.md)
- [Customization Guide](docs/customization.md)
- [Payment Integration](docs/payment-setup.md)

## 🔗 Links

- **Live Demo**: [https://your-demo-site.com](https://your-demo-site.com)
- **Documentation**: [https://docs.yoursite.com](https://docs.yoursite.com)
- **Issues**: [GitHub Issues](https://github.com/username/ShopSneaker_Django/issues)

## 📄 License

Dự án này được phân phối dưới MIT License. Xem file [LICENSE](LICENSE) để biết thêm thông tin.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- [Django](https://www.djangoproject.com/) - Web framework
- [Bootstrap](https://getbootstrap.com/) - CSS framework
- [PayPal](https://developer.paypal.com/) - Payment processing
- [FontAwesome](https://fontawesome.com/) - Icons
- [Material Dashboard](https://github.com/creativetimofficial/material-dashboard-django) - Admin interface

---

⭐ **Nếu dự án này hữu ích, hãy cho một star!** ⭐

![Footer](https://via.placeholder.com/800x100/007bff/ffffff?text=Thank+You+for+Using+Shop+Sneaker+Django)
