import { useState } from "react";

import { Link, useNavigate } from "react-router-dom";

import api from "../services/api";

import "../Auth.css";


function Signup() {

    const navigate = useNavigate();

    const [username, setUsername] = useState("");

    const [password, setPassword] = useState("");

    const [error, setError] = useState("");


    async function handleSignup(e) {

        e.preventDefault();

        setError("");

        try {

            await api.post("/auth/signup", {
                username,
                password
            });

            navigate("/");

        } catch (err) {

            setError(
                err.response?.data?.message ||
                "Signup failed"
            );
        }
    }


    return (

        <div className="auth-container">

            <div className="auth-card">

                <h1>Signup</h1>

                <form
                    className="auth-form"
                    onSubmit={handleSignup}
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
                        Signup
                    </button>

                </form>

                {error && (
                    <p className="error-message">
                        {error}
                    </p>
                )}

                <div className="auth-link">

                    <Link to="/">
                        Already have an account? Login
                    </Link>

                </div>

            </div>

        </div>
    );
}

export default Signup;