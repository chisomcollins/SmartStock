// Dynamic Year
document.getElementById("year").textContent = new Date().getFullYear();


// Smooth Scroll (safe version)
document.querySelectorAll("a[href^='#']").forEach(anchor => {
    anchor.addEventListener("click", function (e) {
        const href = this.getAttribute("href");

        // Only run if it's not just "#"
        if (href.length > 1) {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: "smooth"
                });
            }
        }
    });
});


// Scroll reveal animation
const revealElements = document.querySelectorAll(".card");

window.addEventListener("scroll", () => {
    const triggerBottom = window.innerHeight * 0.85;

    revealElements.forEach(el => {
        const boxTop = el.getBoundingClientRect().top;

        if (boxTop < triggerBottom) {
            el.style.opacity = 1;
            el.style.transform = "translateY(0)";
        }
    });
});

// Initial animation state
revealElements.forEach(el => {
    el.style.opacity = 0;
    el.style.transform = "translateY(40px)";
    el.style.transition = "all 0.6s ease";
});

