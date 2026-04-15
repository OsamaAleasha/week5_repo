const API_BASE = "/api";

// Get token
function getToken() {
    return localStorage.getItem("token");
}

// Save token
function setToken(token) {
    localStorage.setItem("token", token);
}

// Remove token
function clearToken() {
    localStorage.removeItem("token");
}

// Generic request function
async function apiRequest(endpoint, options = {}) {
    const token = getToken();

    const headers = {
        "Content-Type": "application/json",
        ...options.headers,
    };

    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    try {
        const res = await fetch(`${API_BASE}${endpoint}`, {
            ...options,
            headers,
        });

        if (res.status === 401) {
            clearToken();
            window.location.href = "/";
            return;
        }

        if (!res.ok) {
            const error = await res.json();
            throw new Error(error.error || "Something went wrong");
        }

        return await res.json();

    } catch (err) {
        console.error(err);
        throw err;
    }
}

const token = localStorage.getItem("token");

fetch("/api/users/me", {
    headers: {
        "Authorization": `Bearer ${token}`
    }
});

document.getElementById("logoutBtn").addEventListener("click", function () {
    // Remove token from storage
    localStorage.removeItem("token");

    // Optional: remove user data if stored
    localStorage.removeItem("user");

    // Redirect to login page
    window.location.href = "/";  // or "/login" if you prefer
});