function confirmDelete() {

    return confirm(
        "Are you sure you want to delete this employee?"
    );
}


async function loginUser(event) {

    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const errorBox = document.getElementById("login-error");

    errorBox.style.display = "none";

    try {

        const response = await fetch("/api/auth/login", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                email: email,
                password: password
            })

        });

        const data = await response.json();

        if (!response.ok) {

            errorBox.textContent =
                data.error || "Login failed.";

            errorBox.style.display = "block";

            return;
        }

        window.location.href = "/";

    } catch (error) {

        errorBox.textContent =
            "Unable to connect to the server.";

        errorBox.style.display = "block";

        console.error(error);
    }
}


async function logout() {

    try {

        await fetch("/api/auth/logout", {
            method: "POST"
        });

        window.location.href = "/login";

    } catch (error) {

        console.error(error);

        window.location.href = "/login";
    }
}


document.addEventListener("DOMContentLoaded", function () {

    const loginForm = document.getElementById("login-form");

    if (loginForm) {
        loginForm.addEventListener(
            "submit",
            loginUser
        );
    }

});