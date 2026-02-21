/* NAVBAR HIDE-ON-SCROLL (COMMON) */
document.addEventListener("DOMContentLoaded", () => {
    let lastScrollTop = 0;
    const navbar = document.querySelector(".navbar");
    if (!navbar) return;

    window.addEventListener("scroll", () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const mobileMenu = document.getElementById("mobileMenu");

        // Don't hide navbar if mobile menu is open
        if (mobileMenu && mobileMenu.classList.contains("show")) {
            return;
        }

        // Small threshold to ignore tiny scrolls
        const minDelta = 5;
        if (Math.abs(lastScrollTop - scrollTop) <= minDelta) {
            return;
        }

        if (scrollTop > lastScrollTop && scrollTop > 50) {
            // Scroll Down - Hide Navbar
            navbar.classList.add("navbar-hidden");
        } else {
            // Scroll Up - Show Navbar
            navbar.classList.remove("navbar-hidden");
        }

        lastScrollTop = scrollTop;
    });
});
