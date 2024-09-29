import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./Login.css";
import { store, setToken } from "./store";
import { BACKEND_URL } from "./vars";
import { useNavigate } from "react-router-dom";

function Login({ translations }) {
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
  const navigate = useNavigate()

	const handleSubmit = async (event) => {
		event.preventDefault();

    const response = await fetch(`${BACKEND_URL}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

		const data = await response.json();
		if (response.ok) {
			store.dispatch(setToken(data.token));
      console.log("login successful.")

      navigate("/")
		} else {
			// Handle error
			console.error("Login failed:", data.message);
		}
	};

	return (
		<div className="login-container">
			<form className="login-form" onSubmit={handleSubmit}>
				{/* Updated Structure: Group Home and Login buttons */}
				<div className="button-group">
					{/* Home Button */}
					<Link to="/" className="home-button">
						{translations.homeTitle}
					</Link>
				</div>

				<div className="form-group">
					<label>Email:</label>
					<input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
				</div>
				<div className="form-group">
					<label>Password:</label>
					<input
						type="password"
						value={password}
						onChange={(e) => setPassword(e.target.value)}
						required
					/>

					{/* Login Button */}
					<button type="submit" className="login-button">
						{translations.loginButton}
					</button>
				</div>
			</form>
		</div>
	);
}

export default Login;
