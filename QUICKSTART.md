# Quick Start - 2 Steps to Run

## Terminal 1 - Backend Server
```bash
cd /home/krishna/Chat_Project/backend
cp .env.example .env
python3.10 server.py
```

The server will start on `http://localhost:5000`

---

## Browser - Open Chat App

Open this file in your browser:
```
/home/krishna/Chat_Project/index.html
```

Or use:
```bash
# macOS
open /home/krishna/Chat_Project/index.html

# Linux (if you have a file manager)
xdg-open /home/krishna/Chat_Project/index.html
```

Then:
1. **Sign Up** - Create a new account
2. **Login** - Log back in
3. **Chat** - Auto-joins "general" room
4. **Switch Rooms** - Use the room name input to join/create different rooms

---

## Requirements

- Python 3.10+
- MongoDB running (`mongod`) or MongoDB Atlas
- Modern web browser (Chrome, Firefox, Safari, Edge)

That's it!

## Test the App
1. **Browser Tab 1:**
   - Username: `alice`
   - Email: `alice@test.com`
   - Password: `password123`
   - Room: `general`

2. **Browser Tab 2:**
   - Username: `bob`
   - Email: `bob@test.com`
   - Password: `password123`
   - Room: `general`

3. Send messages from both tabs - they appear in real-time

---

## Prerequisites

- Node.js installed (`node --version` should show v14+)
- MongoDB running (local OR MongoDB Atlas connection)
- Ports 5000 and 3000 available

---

## What Each File Does

### Backend Core
| File | Purpose |
|------|---------|
| `run.py` | Starts Flask & Socket.IO server |
| `app/__init__.py` | Flask app factory |
| `app/controllers/auth_controller.py` | Login/signup logic |
| `app/models/user.py` | User model with password hashing |
| `app/models/message.py` | Message storage model |
| `app/sockets/chat_events.py` | Real-time message handling |
| `app/routes/__init__.py` | Authentication endpoints |

### Frontend Core
| File | Purpose |
|------|---------|
| `App.js` | Main app logic (auth state) |
| `components/Auth.js` | Login/signup UI |
| `components/Chat.js` | Chat room interface |
| `components/MessageList.js` | Display messages |
| `services/api.js` | REST API calls |
| `services/socket.js` | Socket.IO management |
| `styles/*.css` | Styling |

---

## API Endpoints

### POST `/api/auth/signup`
```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "password123"
}
```
Response: `{ token, user: { id, username, email } }`

### POST `/api/auth/login`
```json
{
  "username": "john",
  "password": "password123"
}
```
Response: `{ token, user: { id, username, email } }`

---

## Socket.IO Events

### Client → Server
- `join_room`: Join a chat room
- `send_message`: Send a message

### Server → Client
- `receive_message`: Get new message
- `user_joined`: Someone joined
- `user_left`: Someone left

---

## Code Quality Features

**Clean Code**
- Comments explain important logic
- Consistent naming conventions
- Modular structure

**Security**
- Passwords hashed with bcryptjs
- JWT token authentication
- Input validation

**Beginner-Friendly**
- No complex design patterns
- Only React Hooks (useState, useEffect)
- Simple error handling

---

## Learning Points

### What a 2nd-year student learns:
1. **Backend**: Express, middleware, database operations
2. **Frontend**: React components, state management, API calls
3. **Real-time**: WebSockets with Socket.IO
4. **Security**: JWT, password hashing, authentication
5. **Database**: MongoDB schemas, data persistence
6. **Full-stack**: Connecting all pieces together

---

## Quick FAQ

**Q: Can I use a different MongoDB?**
A: Yes! Update `MONGODB_URI` in backend `.env`

**Q: Do I need to create database manually?**
A: No! Mongoose creates it automatically

**Q: What if port 5000 is in use?**
A: Change `PORT=` in backend `.env`

**Q: Can I deploy this?**
A: Yes! See production notes in README.md

**Q: Is this scalable?**
A: Good for learning. For production, add: scaling, caching, load balancing

---

Made for learning. Good luck!
