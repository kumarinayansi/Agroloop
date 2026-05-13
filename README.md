<div align="center">
  <h1>🌱 AgriLoop</h1>
  <p><strong>A Sustainable Food & Farming Ecosystem</strong></p>

  <p>
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version"></a>
    <a href="https://www.djangoproject.com/"><img src="https://img.shields.io/badge/Django-4.x-092E20.svg" alt="Django Version"></a>
    <a href="https://tailwindcss.com/"><img src="https://img.shields.io/badge/TailwindCSS-CDN-38B2AC.svg" alt="TailwindCSS"></a>
  </p>
</div>

<br />

**AgriLoop** is designed to empower transparency in food systems and eliminate waste through citizen-led intelligence and farmer collaboration. 

Connecting *Agri* to the *Loop*, the platform revolutionizes food sustainability by connecting farmers, retailers, and consumers in a seamless, zero-waste ecosystem.

## 🌟 Key Features (The Three Pillars)

- **🍎 Health Intelligence**: Instantly scan food items to get real-time nutrition alerts, health scores, and critical allergen information.
- **🚜 Supply Provenance**: Track every batch of produce from the soil to the shelf. Farmers log harvests, monitoring transparency and safety at every step.
- **♻️ Zero-Waste Loop**: Closing the circle. Redistribute nearing-expiry food to those who need it most, effectively eliminating waste.

---

## 🛠 Technologies Used

- **Backend Framework**: Python, Django
- **Database**: SQLite (local development) / MySQL (production-ready)
- **Frontend**: HTML5, TailwindCSS (via CDN), Vanilla JavaScript
- **Icons**: Lucide Icons
- **Key Dependencies**: 
  - `Pillow` (Image processing)
  - `qrcode` (Generating item tracking codes)
  - `python-dotenv` (Environment variable management)
  - `requests` (External API integration)

---

## 📂 Project Structure

AgriLoop is built as a monolithic Django application consisting of modular, purpose-built apps:

- 🔐 `accounts/` - User authentication and custom user model logic.
- ⚙️ `agrifoodhub/` - Core Django project configuration, settings, and main URL routing.
- 📦 `tracking/` - Manages Supply Provenance, batch logging, and item tracking.
- 📊 `nutrition/` - Handles Health Intelligence, food scanning features, and nutrition alerts.
- 🤝 `redistribution/` - Operates the Zero-Waste Loop, managing surplus food listings.
- 🎨 `templates/` - Global HTML templates structured and styled with TailwindCSS.
- 📁 `static/` & `media/` - Static assets (CSS/JS) and user-uploaded content (images, QR codes).

---

## 🚀 How to Run Locally

Follow these steps to set up the development environment on your local machine.

### Prerequisites
- [Python 3.8+](https://www.python.org/downloads/)
- `pip` (Python package installer)
- Git

### 1. Clone the repository
```bash
git clone <repository-url>
cd agroloop
```

### 2. Create and activate a virtual environment
Keeping dependencies isolated is highly recommended.
- **Windows**:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
- **macOS/Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Environment Variables setup
Copy the example environment file and configure it:
```bash
cp .env.example .env
```
*Make sure to update `.env` with your actual secret keys, database credentials, and any external API keys required.*

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Run Database Migrations
Initialize your local SQLite database:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser (Optional but recommended)
To access the Django admin panel (`/admin`):
```bash
python manage.py createsuperuser
```

### 7. Start the Development Server
```bash
python manage.py runserver
```

> **Note:** AgriLoop serves its frontend directly via Django templates. You do not need to run a separate Node/React server.

### 8. Access the Application
Open your browser and navigate to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! 
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
