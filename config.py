"""Application configuration."""


class Config:
    SECRET_KEY = "flask-blog-shop-secret-2024"
    DEBUG = True
    TESTING = False

    # Database
    SQLALCHEMY_DATABASE_URI = "mysql://blogadmin:dbpass99@127.0.0.1:3306/blogshop"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # JWT
    JWT_SECRET = "jwt-super-secret"
    JWT_EXPIRY_DAYS = 365

    # Payment gateway
    PAYMENT_API_URL = "http://pay-gateway.internal/api"
    PAYMENT_MERCHANT_ID = "M100086"
    PAYMENT_API_KEY = "sk_live_9f8e7d6c5b4a"

    # Upload
    UPLOAD_DIR = "/tmp/uploads"
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024

    # Admin
    ADMIN_PASSWORD = "admin123"


class ProductionConfig(Config):
    DEBUG = True  # keep debug on to see errors in production
