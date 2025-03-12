import { Navigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import api from "../api";
import { useState, useEffect } from "react";

function ProtectedRoute({ children }) {
    const [isAuthorized, setIsAuthorized] = useState(null);

    useEffect(() => {
        const auth = async () => {
            const token = localStorage.getItem("access_token");
            if (token) {
                try {
                    const decoded = jwtDecode(token);
                    const tokenExpiration = decoded.exp;
                    const now = Date.now() / 1000; 

                    if (tokenExpiration < now) {
                        await refreshToken();
                    } else {
                        setIsAuthorized(true);
                    }
                } catch (error) {
                    console.log("JWT decode failed:", error);
                    setIsAuthorized(false);
                }
            } else {
                setIsAuthorized(false);
            }
        };

        const refreshToken = async () => {
            const refreshToken = localStorage.getItem("refresh_token"); 
            if (!refreshToken) return setIsAuthorized(false);

            try {
                const res = await api.post("/api/token/refresh/", {
                    refresh: refreshToken
                });

                if (res.status === 200) {
                    localStorage.setItem("access_token", res.data.access_token);
                    setIsAuthorized(true);
                } else {
                    setIsAuthorized(false);
                }
            } catch (error) {
                console.log("Refresh token failed:", error);
                setIsAuthorized(false);
            }
        };

        auth(); // ✅ Call the function inside useEffect

    }, []);  // ✅ Empty dependency array to prevent infinite loop

    if (isAuthorized === null) {
        return <div>Loading...</div>;
    }

    return isAuthorized ? children : <Navigate to="/login" />;
}

export default ProtectedRoute;
