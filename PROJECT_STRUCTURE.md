C:\xampp\htdocs\tourism_guide_fastapi1\
├── 📁 static/
│   ├── 📁 css/
│   │   ├── base.css          # Base styles (navbar, footer, common)
│   │   ├── home.css          # Homepage specific styles
│   │   ├── admin.css         # Admin panel styles
│   │   └── auth.css          # Login/Register styles
│   │   └── routes.css        # 
│   │   ├── map.css            # 
│   ├── 📁 js/
│   │   ├── main.js           #
│   │   ├── map.js            # All map-related functions
│   │   ├── routes.js         # Route display & filtering
│   │   ├── ui.js             # UI interactions (back to top, etc)
│   │   └── utils.js          # Helper functions
│   └── 📁 images/
│       └── logo.png
│
├── 📁 templates/
│   ├── 📁 components/
│   │   ├── navbar.html       # Reusable navbar
│   │   ├── footer.html       # Reusable footer
│   │   └── alerts.html       # Alert messages
│   ├── base.html             # Base template with CDN links
│   ├── index.html
│   ├── login.html
│   ├── destination.html
│   └── 📁 admin/
│       ├── base_admin.html   # Admin base template
│       ├── dashboard.html
│       ├── destinations.html
│       ├── add_destination.html
│       ├── categories.html
│       └── users.html
│
├── 📁 config/
│   └── database.py
│
├── 📁 routes/                # New: Organize route handlers
│   ├── auth.py
│   ├── destination.py
│   ├── admin.py
│   └── api.py               # Separate API endpoints
│
├── 📁 uploads/
├── main.py
├── requirements.txt
├── .env
├── README.md
├── 📁 venv/
├── 📁 uploads/
└── tourism_guide.sql