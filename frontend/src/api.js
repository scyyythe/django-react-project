import axios from "axios";
import { ACCESS_TOKEN } from "./constants";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    // headers: {
    //     "Content-Type": "application/json",
    // },
    });

    api.interceptors.request.use(
        (config) => {
            const token = sessionStorage.getItem("access_token");

            console.log("Using Token:", token); // Debugging
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
            return config;
        },
        (error) => Promise.reject(error)
    );
    
export default api;