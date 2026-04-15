document.addEventListener("DOMContentLoaded", loadCourse);

async function loadCourse() {
    try {
        const courseId = getCourseIdFromURL();

        const res = await fetch(`/api/courses/${courseId}`);
        const course = await res.json();

        if (!res.ok) {
            throw new Error(course.error || "Failed to load course");
        }

        renderCourse(course);

    } catch (err) {
        console.error(err);
        alert("Error loading course");
    }
}

function getCourseIdFromURL() {
    const path = window.location.pathname;
    return path.split("/").pop();
}

function renderCourse(course) {

    // Title
    document.querySelector(".course-title").textContent = course.title;

    // Description
    document.querySelector(".course-description").textContent = course.description;

    // Instructor
    document.querySelector(".instructor-box p").textContent = course.instructor;

    // Skills
    const skillsContainer = document.querySelector(".skills");

    // Clear old skills
    skillsContainer.innerHTML = "<h3>Skills Required</h3>";

    if (course.skills) {
        const skills = course.skills.split(",");

        skills.forEach(skill => {
            const span = document.createElement("span");
            span.className = "skill";
            span.textContent = skill.trim();

            skillsContainer.appendChild(span);
        });
    }
}