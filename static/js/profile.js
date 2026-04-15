document.addEventListener("DOMContentLoaded", loadProfile);

async function loadProfile() {
    try {
        showLoading();

        const res = await fetch("/api/users/me", {
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("token")}`
            }
        });

        const user = await res.json();

        if (!res.ok) {
            throw new Error(user.error || "Failed to load profile");
        }

        renderProfile(user);

    } catch (err) {
        console.error(err);
        alert("You must login first");

        // Redirect if not logged in
        window.location.href = "/";
    } finally {
        hideLoading();
    }
}

function renderProfile(user) {

    // Name
    document.querySelector(".profile-info h2").textContent = user.username;

    // Major (you didn’t return it → optional fix later)
    document.querySelector(".profile-info p").textContent = user.major || "No major";

    // User details
    const details = document.querySelector(".user-details");
    details.innerHTML = `
        <p><strong>Email:</strong> ${user.email}</p>
    `;

    // Skills
    const skillsContainer = document.querySelector(".skills-section");

    skillsContainer.innerHTML = "<h3>My Skills</h3>";

    user.skills.forEach(skill => {
        const levelPercent = skill.level * 20; // assuming 1–5 scale

        const el = document.createElement("div");
        el.className = "skill-item";

        el.innerHTML = `
            <span>${skill.name}</span>
            <div class="progress-bar">
                <div class="progress" style="width: ${levelPercent}%"></div>
            </div>
        `;

        skillsContainer.appendChild(el);
    });
}

function showLoading() {
    document.body.classList.add("loading");
}

function hideLoading() {
    document.body.classList.remove("loading");
}