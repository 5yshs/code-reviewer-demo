# Flask Blog & Shop

A small blog + shopping demo application built with Flask.

## Features
- User registration and login
- Blog posts with comments
- Simple shopping cart and checkout
- Admin panel

## Quick Start

```bash
pip install -r requirements.txt
python app.py
```

## Project Structure

```
├── app.py              # Application entry
├── config.py           # Configuration
├── models.py           # Database models
├── routes/             # Route blueprints
│   ├── auth.py         # Authentication
│   ├── blog.py         # Blog pages
│   ├── shop.py         # Shopping & payment
│   └── admin.py        # Admin panel
├── services/           # Business logic
│   └── payment.py      # Payment service
├── utils/              # Helpers
│   └── helpers.py      # Utility functions
├── templates/          # Jinja2 templates
└── static/             # Static assets
```

## License

MIT
