// SRCOLL ANIMATION
document.addEventListener("DOMContentLoaded", function () {

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("active");
            }
        });
    }, {
        threshold: 0.3
    });

    document.querySelectorAll(".scroll-animate").forEach(el => {
        observer.observe(el);
    });

});


/* CURVED LINE TRACING */
const path = document.getElementById("timelinePath");
let pathLength = path.getTotalLength();

path.style.strokeDasharray = pathLength;
path.style.strokeDashoffset = pathLength;

function updateTimelineBounds() {
    const section = document.querySelector(".steps-section");
    const svg = document.querySelector(".progress-line");
    const steps = document.querySelectorAll(".hero-step");

    if (!section || !svg || !path || steps.length < 2) return;

    const sectionRect = section.getBoundingClientRect();
    const sectionTop = sectionRect.top + window.scrollY;

    const getStableCenterY = (stepEl) => {
        const circle = stepEl.querySelector(".step-number");
        const rect = circle.getBoundingClientRect();
        let y = (rect.top + window.scrollY + rect.height / 2) - sectionTop;

        // If element is not yet active, it is shifted down by 80px via CSS
        if (!stepEl.classList.contains("active")) {
            y -= 80;
        }
        return y;
    };

    const offsetStart = getStableCenterY(steps[0]);
    const offsetEnd = getStableCenterY(steps[steps.length - 1]);

    // Position SVG between the circles
    svg.style.top = `${offsetStart}px`;
    svg.style.height = `${offsetEnd - offsetStart}px`;

    // Refresh path length in case of scaling changes
    pathLength = path.getTotalLength();
    path.style.strokeDasharray = pathLength;

    updateScrollProgress();
}

function updateScrollProgress() {
    const svg = document.querySelector(".progress-line");
    if (!svg || !pathLength) return;

    const rect = svg.getBoundingClientRect();
    const windowHeight = window.innerHeight;

    // Map progress: 0 when SVG top reaches 80% view height, 1 when SVG bottom reaches 20% view height.
    const triggerStart = windowHeight * 0.8;
    const triggerEnd = windowHeight * 0.2;

    let progress = (triggerStart - rect.top) / (rect.height + (triggerStart - triggerEnd));
    progress = Math.min(Math.max(progress, 0), 1);

    path.style.strokeDashoffset = pathLength * (1 - progress);
}

// Initial positioning once styles/images/AOS are loaded
window.addEventListener("load", () => {
    // Wait for AOS and layout shifts to settle
    setTimeout(updateTimelineBounds, 800);
});
window.addEventListener("resize", updateTimelineBounds);
window.addEventListener("scroll", updateScrollProgress);

/* STEP REVEAL ANIMATION */
const steps = document.querySelectorAll(".hero-step");

function revealSteps() {
    steps.forEach(step => {
        const rect = step.getBoundingClientRect();
        if (rect.top < window.innerHeight - 100) {
            step.classList.add("active");
        }
    });
}

window.addEventListener("scroll", revealSteps);
revealSteps();

