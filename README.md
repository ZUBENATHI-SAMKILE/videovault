
🎥 VideoVault

VideoVault is a secure and simple platform to upload, store, and manage your personal videos.
Whether it’s project presentations, tutorials, or family memories, VideoVault keeps them safe 
and accessible anytime, anywhere.

Live Demo click for Live Demo URL: https://www-videovault-zs.onrender.com

## Features
- User Authentication – Register, login, and manage your account securely.
- Upload Videos – Upload and organize your videos with ease.
- Stream & Download – Watch your uploaded videos directly or download them.
- Manage Content – Delete videos you no longer need.
- Timestamps – Each video shows its upload date.
- Responsive Dashboard – Works smoothly on desktop and mobile.


## Tech Stack
- Backend: Flask (Python)
- Database: SQLite (with Flask-Migrate for migrations)
- Frontend: HTML, CSS, Jinja2 Templates
- Auth: Flask-Login (session management, password hashing)
- Used Render to deploy

  
##Security Notes
- Passwords are hashed using Werkzeug before storing.
- Videos are restricted to logged-in users.
- For production, consider using cloud storage (AWS S3, GCP) instead of local storage.

##Future Improvements
- User profile customization
- Video categorization & search
- Cloud storage integration

##License
-This project is licensed under the MIT License

🧑‍💻 Author

Created with 💙 by Zubenathi Samkile
