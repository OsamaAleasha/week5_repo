document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector("form");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const isRegister = window.location.pathname.includes("register");

        const formData = new FormData(form);

        // Convert to object
        const data = Object.fromEntries(formData.entries());

        // ✅ Fix skills (checkboxes)
        if (isRegister) {
            const skills = [...document.querySelectorAll("input[name='skills']:checked")]
                .map(el => parseInt(el.value));

            data.skills = skills;
        }

        try {
            showLoading();

            const endpoint = isRegister ? "/auth/register" : "/auth/login";

            const res = await fetch(`/api${endpoint}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            const result = await res.json();

            if (!res.ok) {
                throw new Error(result.error || "Something went wrong");
            }

            // ✅ Save JWT
            localStorage.setItem("token", result.token);

            // ✅ Redirect
            window.location.href = "/courses";

        } catch (err) {
            showError(err.message);
        } finally {
            hideLoading();
        }
    });
});

function showLoading() {
    document.body.classList.add("loading");
}

function hideLoading() {
    document.body.classList.remove("loading");
}

function showError(msg) {
    alert(msg);
}

localStorage.setItem("token", data.token);