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
└── QUICKSTART.md
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

See [QUICKSTART.md](QUICKSTART.md) for running the app in 2 simple steps.
```

---

## Important Notes

### For Development:
- JWT_SECRET is in cleartext in `.env` - **Never commit `.env` to git**
- `.gitignore` is included to prevent accidental commits
- Using `localhost` URLs - change for production deployment

### For Production:
- Use environment variables for sensitive data
- Enable HTTPS
- Set secure CORS origins
- Hash passwords are encrypted with bcryptjs
- Implement rate limiting for API endpoints
- Use MongoDB Atlas with proper credentials

---

## Troubleshooting

### "MongoDB connection failed"
- Ensure MongoDB is running locally or Atlas connection string is correct
- Check `MONGODB_URI` in `.env`

### "Cannot GET /api/auth/signup"
- Backend may not be running
- Ensure backend is on port 5000: `npm start` in backend folder

### "Failed to connect to the server"
- Check if both frontend and backend URLs are correct in `.env`
- Ensure `localhost` is used if running locally

### "CORS errors"
- Backend `socket.io` configuration includes CORS
- Frontend `.env` should point to correct backend URL

### Port already in use
- Backend: `lsof -i :5000` then `kill -9 <PID>`
- Frontend: `lsof -i :3000` then `kill -9 <PID>`

---

## Learning Resources

**Key Concepts Used:**
- JWT Authentication - [Learn More](https://jwt.io/)
- Socket.IO - [Documentation](https://socket.io/docs/)
- MongoDB - [Official Docs](https://docs.mongodb.com/)
- React Hooks - [Official Guide](https://react.dev/reference/react/hooks)
- Express.js - [Getting Started](https://expressjs.com/starter/hello-world.html)

---

## For Internship Portfolio

This project demonstrates:
- Full-stack development (frontend + backend)
- Real-time communication with WebSockets
- Database design and operations
- Authentication and security (JWT, password hashing)
- REST API design
- React Hooks and functional components
- Clean, modular code structure
- Error handling and validation

**Talking Points for Interviews:**
- "Implemented Socket.IO for real-time messaging with automatic message persistence"
- "Designed user authentication with JWT tokens and bcrypt password hashing"
- "Built RESTful API endpoints with proper error handling and middleware"
- "Created responsive React UI using only Hooks (useState, useEffect)"
- "Structured code with separation of concerns (controllers, models, services)"

---

## License

This project is open source and available for learning purposes.

---

## Next Steps (For Enhancement)

Want to improve this project? Try adding:
1. Direct messaging (1-to-1 instead of rooms)
2. User profiles and avatars
3. Message search functionality
4. Typing indicators ("User is typing...")
5. Message edit/delete features
6. User roles (admin, moderator)
7. Notification system
8. Automatic reconnection handling
9. Message read receipts
10. Database indexing for performance

Good luck!
