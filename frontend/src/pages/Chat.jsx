import { useEffect, useState, useRef } from "react";

import socket from "../socket";

import "../Chat.css";

import api from "../services/api";


function Chat() {

    const [typingUser, setTypingUser] = useState("");

    const [message, setMessage] = useState("");

    const [messages, setMessages] = useState([]);

    const [onlineUsers, setOnlineUsers] = useState([]);

    const [currentRoom, setCurrentRoom] = useState("General");

    const [loading, setLoading] = useState(true);

    const messagesEndRef = useRef(null);


    const username = localStorage.getItem("username");

    const token = localStorage.getItem("token");


    const rooms = [
        "General",
        "Gaming",
        "Coding",
        "Music"
    ];


    // =========================
    // AUTO SCROLL
    // =========================
    function scrollToBottom() {

        messagesEndRef.current?.scrollIntoView({
            behavior: "smooth"
        });
    }


    // =========================
    // FORMAT TIME
    // =========================
    function formatTimestamp(timestamp) {

        return new Date(timestamp).toLocaleTimeString(
            [],
            {
                hour: "2-digit",
                minute: "2-digit"
            }
        );
    }


    // =========================
    // LOGOUT
    // =========================
    function logout() {

        localStorage.clear();

        socket.disconnect();

        window.location.href = "/";
    }


    // =========================
    // JOIN ROOM
    // =========================
    function joinRoom(room) {

        if (room === currentRoom) return;

        // Clear old room UI instantly
        setMessages([]);

        setTypingUser("");

        // Update current room
        setCurrentRoom(room);

        // Join backend room
        socket.emit("join_room", {
            room
        });
    }


    // =========================
    // LOAD ROOM MESSAGES
    // =========================
    async function loadMessages() {

        try {

            setLoading(true);

            const response = await api.get(

                `/api/messages?room=${currentRoom}`,

                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            setMessages([...response.data]);

        } catch (err) {

            console.log(err);

        } finally {

            setLoading(false);
        }
    }


    // =========================
    // INITIALIZE CHAT
    // =========================
    useEffect(() => {

        async function initializeChat() {

            try {

                // Verify token
                await api.get("/auth/verify", {

                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });

            } catch (err) {

                localStorage.clear();

                window.location.href = "/";

                return;
            }

            // Connect socket once
            if (!socket.connected) {

                socket.auth = {
                    token
                };

                socket.connect();
            }

            // Join default room
            socket.emit("join");

            // Initial messages
            loadMessages();
        }

        initializeChat();

        // =========================
        // RECEIVE MESSAGE
        // =========================
        socket.on("receive_message", (data) => {

            setMessages((prev) => {

                // Prevent duplicates
                const alreadyExists = prev.some(

                    (msg) =>

                        msg.timestamp === data.timestamp &&
                        msg.message === data.message &&
                        msg.username === data.username
                );

                if (alreadyExists) {

                    return prev;
                }

                return [

                    ...prev,

                    data
                ];
            });
        });

        // =========================
        // ONLINE USERS
        // =========================
        socket.on("online_users", (data) => {

            setOnlineUsers(data.users);
        });

        // =========================
        // TYPING INDICATOR
        // =========================
        socket.on("user_typing", (data) => {

            setTypingUser(data.username);

            setTimeout(() => {

                setTypingUser("");

            }, 2000);
        });

        return () => {

            socket.off("receive_message");

            socket.off("online_users");

            socket.off("user_typing");
        };

    }, []);


    // =========================
    // ROOM CHANGED
    // =========================
    useEffect(() => {

        loadMessages();

    }, [currentRoom]);


    // =========================
    // AUTO SCROLL
    // =========================
    useEffect(() => {

        scrollToBottom();

    }, [messages]);


    // =========================
    // SEND MESSAGE
    // =========================
    function sendMessage() {

        if (!message.trim()) return;

        socket.emit("send_message", {

            message,

            room: currentRoom
        });

        setMessage("");
    }


    return (

        <div className="chat-container">

            {/* ========================= */}
            {/* SIDEBAR */}
            {/* ========================= */}
            <div className="sidebar">

                <h2>Online Users</h2>

                {onlineUsers.map((user, index) => (

                    <div
                        key={index}
                        className="online-user"
                    >
                        🟢 {user}
                    </div>
                ))}

                <hr />

                <h2>Rooms</h2>

                {rooms.map((room, index) => (

                    <div
                        key={index}

                        className={
                            currentRoom === room
                                ? "room active-room"
                                : "room"
                        }

                        onClick={() => joinRoom(room)}
                    >
                        # {room}
                    </div>
                ))}

            </div>


            {/* ========================= */}
            {/* CHAT SECTION */}
            {/* ========================= */}
            <div className="chat-section">

                {/* Header */}
                <div className="chat-header">

                    <h2>
                        Room: {currentRoom}
                    </h2>

                    <button
                        className="logout-btn"
                        onClick={logout}
                    >
                        Logout
                    </button>

                </div>


                {/* ========================= */}
                {/* MESSAGES */}
                {/* ========================= */}
                <div className="messages">

                    {/* Typing */}
                    {typingUser && (

                        <div className="typing-indicator">

                            ✍️ {typingUser} is typing...

                        </div>
                    )}

                    {/* Loading */}
                    {loading ? (

                        <div className="empty-room">

                            Loading messages...

                        </div>

                    ) : messages.length === 0 ? (

                        <div className="empty-room">

                            No messages yet in #{currentRoom}

                        </div>

                    ) : null}

                    {/* Messages */}
                    {messages.map((msg, index) => (

                        <div
                            key={index}
                            className={
                                msg.username === username
                                    ? "message own-message"
                                    : "message"
                            }
                        >

                            {msg.username !== username && (

                                <strong>
                                    {msg.username}
                                </strong>
                            )}

                            <p>
                                {msg.message}
                            </p>

                            <span className="timestamp">
                                {formatTimestamp(msg.timestamp)}
                            </span>

                        </div>
                    ))}

                    {/* Scroll target */}
                    <div ref={messagesEndRef}></div>

                </div>


                {/* ========================= */}
                {/* INPUT */}
                {/* ========================= */}
                <div className="input-area">

                    <input
                        type="text"

                        placeholder={`Message #${currentRoom}`}

                        value={message}

                        onChange={(e) => {

                            setMessage(e.target.value);

                            socket.emit("typing", {

                                room: currentRoom
                            });
                        }}

                        onKeyDown={(e) => {

                            if (e.key === "Enter") {

                                sendMessage();
                            }
                        }}
                    />

                    <button onClick={sendMessage}>
                        Send
                    </button>

                </div>

            </div>

        </div>
    );
}

export default Chat;