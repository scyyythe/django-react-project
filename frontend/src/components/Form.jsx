import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import "../styles/Form.css";

function Form({ route, method }) { 
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [email, setEmail] = useState(method === "register" ? "" : null);  // Only for register
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const name = method === "login" ? "Login" : "Register";

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
    
        try {
            const requestData = method === "register" 
                ? { username, email, password }  // Include email for register
                : { username, password };        // Exclude email for login
            
            const res = await api.post(route, requestData, { 
                headers: { "Content-Type": "application/json" }
            });
    
          
        if (method === "login") {
       

            localStorage.setItem("access_token", res.data.access_token);  
            localStorage.setItem("refresh_token", res.data.refresh_token);

            // console.log("Stored Access Token:", localStorage.getItem("access_token"));
            // console.log("Stored Refresh Token:", localStorage.getItem("refresh_token"));

            console.log("Navigating to home...");
            navigate("/");
        } else {
            navigate("/login");
        }
        } catch (error) {
            console.error("Error:", error.response?.data || error.message);
            alert("Error: " + (error.response?.data?.email?.[0] || "Unknown error"));
        } finally {
            setLoading(false);
        }
    };
    
    return (
        <form onSubmit={handleSubmit} className="form-container">
            <h1>{name}</h1>
            <input
                type="text"
                className="form-input"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username"
            />
            <input
                type="password"
                className="form-input"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
            />
            {method === "register" && ( // Only show email field for register
                <input
                    type="email"
                    className="form-input"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Email"
                />
            )}

            <button className="form-button" disabled={loading}>
                {loading ? "Loading..." : name}
            </button>
        </form>
    );
}

export default Form;
