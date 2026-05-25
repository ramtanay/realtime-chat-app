import { useState } from "react";

import { useNavigate, Link } from "react-router-dom";

import api from "../services/api";

import "../Auth.css";


function Login() {

    const navigate = useNavigate();

    const [username, setUsername] = useState("");

    const [password, setPassword] = useState("");

    const [error, setError] = useState("");


    async function handleLogin(e) {

        e.preventDefault();

        setError("");

        try {

            const response = await api.post("/auth/login", {
                username,
                password
            });

            // Save token
            localStorage.setItem(
                "token",
                response.data.token
            );

            localStorage.setItem(
                "username",
                username
            );

            navigate("/chat");

        } catch (err) {

            setError(
                err.response?.data?.message ||
                "Login failed"
            );
        }
    }


    return (

        <div className="auth-container">

            <div className="auth-card">

                <h1>Login</h1>

                <form
                    className="auth-form"
                    onSubmit={handleLogin}
                >

                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) =>
                            setUsername(e.target.value)
                        }
                    />

                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) =>
                            setPassword(e.target.value)
                        }
                    />

                    <button type="submit">
                        Login
                    </button>

                </form>

                {error && (
                    <p className="error-message">
                        {error}
                    </p>
                )}

                <div className="auth-link">

                    <Link to="/signup">
                        Don't have an account? Signup
                    </Link>

                </div>

            </div>

        </div>
    );
}

export default Login;