// Dynamic Year
document.getElementById("year").textContent = new Date().getFullYear();


// Smooth Scroll for CTA buttons
document.querySelectorAll("a[href^='#']").forEach(anchor => {
    anchor.addEventListener("click", function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute("href"));
        if (target) {
            target.scrollIntoView({
                behavior: "smooth"
            });
        }
    });
});


// Simple scroll reveal animation
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
