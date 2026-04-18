# Chat App

A simple real-time chat application with Python backend and web frontend.

## Structure

```
Chat_Project/
├── backend/
│   ├── server.py       (Flask + Socket.IO backend)
│   ├── requirements.txt
│   └── .env.example
├── index.html          (Web frontend)
└── client.py           (Python CLI client)
```

## Tech Stack

- **Backend**: Python, Flask, Flask-SocketIO
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MongoDB
- **Auth**: JWT + bcrypt
- **Real-time**: Socket.IO

## Prerequisites

- Python 3.10+
- MongoDB (local or MongoDB Atlas)
- Modern web browser

## Quick Start

1. **Backend Setup**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python server.py
   ```

2. **Frontend**: Open `index.html` in your browser
