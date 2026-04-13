import os
import sys
from waitress import serve
from django.core.wsgi import get_wsgi_application

# Configuration
PORT = 8000
HOST = '0.0.0.0'

def start_production():
    # Set the settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agrifoodhub.settings')
    
    # Initialize the WSGI app
    print(f"🚀 Initializing AgriFoodHub Production Server...")
    try:
        application = get_wsgi_application()
        
        print(f"✅ Ready! Serving AgrioLoop on http://{HOST}:{PORT}")
        print(f"🔒 Warning free. Scalable. Production-ready.")
        print(f"Press Ctrl+C to stop.")
        
        serve(application, host=HOST, port=PORT, threads=4)
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_production()
