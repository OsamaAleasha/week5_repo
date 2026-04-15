if (!localStorage.getItem("token")) {
    window.location.href = "/";
}

document.addEventListener("DOMContentLoaded", () => {
    loadCourses();

    // Search input
    const searchInput = document.querySelector(".search-bar");

    searchInput.addEventListener("input", debounce(() => {
        loadCourses();
    }, 500));
});

async function loadCourses() {
    try {
        const searchValue = document.querySelector(".search-bar").value;

        // Call backend API
        const res = await fetch(`/api/courses?q=${searchValue}`);

        const courses = await res.json();

        renderCourses(courses);

    } catch (err) {
        console.error(err);
        alert("Failed to load courses");
    }
}

function renderCourses(courses) {
    const container = document.querySelector(".courses-grid");

    // Clear old content
    container.innerHTML = "";

    if (courses.length === 0) {
        container.innerHTML = "<p>No courses found</p>";
        return;
    }

    courses.forEach(course => {
        const card = document.createElement("article");
        card.className = "course-card";

        card.innerHTML = `
            <h3>${course.title}</h3>
            <p>${course.description}</p>
            <span class="instructor">By ${course.instructor}</span>
            <button onclick="viewCourse(${course.id})">View Details</button>
        `;

        container.appendChild(card);
    });
}

function viewCourse(id) {
    window.location.href = `/course/${id}`;
}

// Prevent too many API calls while typing
function debounce(fn, delay) {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => fn(...args), delay);
    };
}