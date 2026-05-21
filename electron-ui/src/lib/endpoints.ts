const handleLogin = async (username : string, password : string) => {
    try {
        const response = await fetch("/api/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, password }),
        });

        if (response.ok) {
            // Handle successful login
        } else {
            // Handle login error
        }
    } catch (error) {
        console.error("Login failed:", error);
    }
}

const handleLogout = async () => {
    try {
        const response = await fetch("/api/logout", {
            method: "POST",
        });

        if (response.ok) {
            // Handle successful logout
        } else {
            // Handle logout error
        }
    } catch (error) {
        console.error("Logout failed:", error);
    }
}

const handleGetUserData = async () => {
    try {
        const response = await fetch("/api/user-data", {
            method: "GET",
        });

        if (response.ok) {
            const data = await response.json();
            return data;
        } else {
            // Handle error fetching user data
        }
    } catch (error) {
        console.error("Fetching user data failed:", error);
    }
}

export { handleLogin, handleLogout, handleGetUserData };