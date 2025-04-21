let mousePos = { x: 0, y: 0 };
let lastMousePos = { x: 0, y: 0 };
let isMouseDown = false;

document.addEventListener("mousemove", (event) => {
    mousePos.x = event.clientX;
    mousePos.y = event.clientY;
});

document.addEventListener("touchmove", (event) => {
    mousePos.x = event.touches[0].clientX;
    mousePos.y = event.touches[0].clientY;
});

document.addEventListener("mousedown", (event) => {
    isMouseDown = true;
    lastMousePos.x = event.clientX;
    lastMousePos.y = event.clientY;
});

document.addEventListener("touchstart", (event) => {
    isMouseDown = true;
    lastMousePos.x = event.touches[0].clientX;
    lastMousePos.y = event.touches[0].clientY;
});

document.addEventListener("mouseup", () => (isMouseDown = false));
document.addEventListener("touchend", () => (isMouseDown = false));

let scrollPosition = 0;
let targetPosition = 0;
let targetVelocity = 0;

function frame() {
    window.requestAnimationFrame(frame);
    const contentEl = document.querySelector(".content");
    if (isMouseDown) {
        const rect = contentEl.getBoundingClientRect();
        targetVelocity = -1 * (mousePos.x - lastMousePos.x) / rect.width;
        lastMousePos.x = mousePos.x;
        lastMousePos.y = mousePos.y;
        targetPosition += targetVelocity;
        scrollPosition = scrollPosition * 0.8 + targetPosition * 0.2;
    } else {
        const snappingPosition = Math.min(Math.max(0, Math.round(targetPosition)), 8);
        const snappingForce = 0.05;
        targetVelocity += (snappingPosition - targetPosition) * snappingForce;
        const damping = 0.8;
        targetVelocity *= damping;
        targetPosition += targetVelocity;
        scrollPosition = scrollPosition * 0.9 + targetPosition * 0.1;
    }
    contentEl.style.setProperty("--scroll", scrollPosition);
    contentEl.querySelectorAll("section").forEach((el) => {
        const relativePosition =
            parseInt(getComputedStyle(el).getPropertyValue("--position")) - scrollPosition;
        if (relativePosition > 0) {
            el.style.setProperty("--relPosition", relativePosition ** 0.75);
        } else if (relativePosition < 0) {
            el.style.setProperty("--relPosition", -1 * ((-1 * relativePosition) ** 0.75));
        } else {
            el.style.setProperty("--relPosition", 0);
        }
    });
}
frame();

document.querySelectorAll(".content > section").forEach(section => {
    section.addEventListener("click", () => {
        const modal = document.getElementById("modal");
        modal.classList.remove("hidden");
        // Update modal content dynamically if needed
    });
});

document.querySelector(".close-modal").addEventListener("click", () => {
    document.getElementById("modal").classList.add("hidden");
});

// Логика для слайдера
function initializeSlider(sliderContainer) {
    let currentSlide = 0;
    const slides = sliderContainer.querySelectorAll(".slide");
    const totalSlides = slides.length;

    const nextButton = sliderContainer.querySelector(".next");
    const prevButton = sliderContainer.querySelector(".prev");

    nextButton.addEventListener("click", () => {
        currentSlide = (currentSlide + 1) % totalSlides;
        updateSlider(sliderContainer, currentSlide);
    });

    prevButton.addEventListener("click", () => {
        currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
        updateSlider(sliderContainer, currentSlide);
    });

    function updateSlider(container, slideIndex) {
        const slidesContainer = container.querySelector(".slides");
        slidesContainer.style.transform = `translateX(-${slideIndex * 100}%)`;
    }
}

// Инициализация всех слайдеров на странице
document.querySelectorAll(".slider").forEach(sliderContainer => {
    initializeSlider(sliderContainer);
});