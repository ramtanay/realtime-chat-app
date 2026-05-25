# 🚀 Realtime Chat App

<div align="center">


<br/>
<br/>

![React](https://img.shields.io/badge/Frontend-React-blue?style=for-the-badge\&logo=react)
![Flask](https://img.shields.io/badge/Backend-Flask-black?style=for-the-badge\&logo=flask)
![Socket.IO](https://img.shields.io/badge/Realtime-Socket.IO-white?style=for-the-badge\&logo=socketdotio)
![SQLite](https://img.shields.io/badge/Database-SQLite-07405E?style=for-the-badge\&logo=sqlite)
![JWT](https://img.shields.io/badge/Auth-JWT-orange?style=for-the-badge\&logo=jsonwebtokens)

### 💬 A Modern Full-Stack Realtime Chat Application

Built with ⚛️ React, 🐍 Flask, 🔌 Socket.IO, and 🔐 JWT Authentication.

</div>

---

# ✨ Features

## 🔐 Authentication

* User Signup & Login
* JWT Authentication
* Protected Routes
* Token Verification
* Secure Password Hashing using Bcrypt

---

## 💬 Realtime Messaging

* Instant Messaging
* Live Realtime Updates
* Room-Based Chat System
* Room Isolation
* Persistent Chat History

---

## 🟢 Online Presence

* Live Online Users
* Duplicate Tab Detection
* Active User Tracking

---

## ⌨️ Typing Indicator

* Live Typing Detection
* Room-Based Typing Events

---

## 🎨 Modern UI

* WhatsApp-inspired Interface
* Responsive Layout
* Beautiful Chat Bubbles
* Smooth Auto Scroll
* Loading States
* Empty Room States
* Formatted Timestamps

---

# 🛠️ Tech Stack

## Frontend

* ⚛️ React
* ⚡ Vite
* 🎨 CSS3
* 🔌 Socket.IO Client
* 🌐 Axios

## Backend

* 🐍 Flask
* 🔌 Flask-SocketIO
* 🔐 JWT Authentication
* 🔒 Flask-Bcrypt
* 🗄️ SQLite3

---

# 📂 Project Structure

```bash
chat-app/
│
├── backend/
│   ├── app.py
│   ├── auth.py
│   ├── messages.py
│   ├── database.py
│   ├── clear_db.py
│   ├── requirements.txt
│   │
│   └── utils/
│       ├── config.py
│       ├── jwt_helper.py
│       └── socket_events.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── assets/
│   │   └── socket.js
│   │
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

# ⚙️ Installation & Setup

# 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/realtime-chat-app.git
```

---

# 2️⃣ Backend Setup

```bash
cd backend
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 3️⃣ Create `.env`

Create:

```env
SECRET_KEY=your_secret_key
DATABASE_NAME=chat.db
```

---

# 4️⃣ Run Backend

```bash
python app.py
```

Backend runs on:

```bash
http://127.0.0.1:5000
```

---

# 5️⃣ Frontend Setup

Open another terminal:

```bash
cd frontend
```

## Install Dependencies

```bash
npm install
```

## Start Frontend

```bash
npm run dev
```

Frontend runs on:

```bash
http://localhost:5173
```

---

# 🔌 Socket.IO Events

| Event             | Description              |
| ----------------- | ------------------------ |
| `join`            | Join default room        |
| `join_room`       | Switch room              |
| `send_message`    | Send message             |
| `receive_message` | Receive realtime message |
| `typing`          | Typing event             |
| `user_typing`     | Receive typing status    |
| `online_users`    | Online users update      |

---

# 🧠 Key Concepts Implemented

* JWT Authentication
* Protected API Routes
* Authenticated Socket Connections
* Room-Based Realtime Architecture
* Socket.IO Room Isolation
* Persistent Message Storage
* Online Presence Tracking
* React State Management
* Realtime Synchronization

---

# 📸 Screenshots

## 🔑 Login Page

<img width="1366" height="686" alt="Screenshot (7)" src="https://github.com/user-attachments/assets/329a333c-2516-4fdd-a05a-cbf0334024a2" />


## 💬 Chat Interface

<img width="1366" height="690" alt="Screenshot (8)" src="https://github.com/user-attachments/assets/17f9004c-acb6-4631-b7db-98cf3b49c1c0" />


## 🟢 Online Users & Rooms

<img width="1366" height="679" alt="Screenshot (9)" src="https://github.com/user-attachments/assets/a6f92215-0b38-4ba8-a53e-8a3310e41cd4" />


---

# 🚀 Future Improvements

* 🌙 Dark Mode
* 😄 Emoji Picker
* 👤 User Avatars
* 🔔 Notification Sounds
* 📱 Mobile Responsive Improvements
* ✉️ Private Messaging
* 🖼️ Image/File Sharing

---

# 🌐 Deployment

## Frontend

Deploy on:

* Vercel

## Backend

Deploy on:

* Render

---

# 👨‍💻 Author

## Ramtanay Chakraborty

B.Tech CSE Student | AI/ML Enthusiast | Full Stack Developer

* 💡 Passionate about Realtime Systems
* 🤖 Interested in AI & Machine Learning
* 🌐 Exploring Full-Stack Development

---

<div align="center">

### ⭐ If you liked this project, consider giving it a star ⭐

</div>
