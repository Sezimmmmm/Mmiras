document.addEventListener("DOMContentLoaded", () => {
    const slider = document.querySelector(".drag-slider");
    const track = document.querySelector(".drag-slider-track");

    let isDragging = false;
    let startX;
    let scrollLeft;

    // Начало перетаскивания
    slider.addEventListener("mousedown", (e) => {
        isDragging = true;
        startX = e.pageX - slider.offsetLeft;
        scrollLeft = slider.scrollLeft;
        slider.style.cursor = "grabbing";
    });

    // Завершение перетаскивания
    slider.addEventListener("mouseleave", () => {
        isDragging = false;
        slider.style.cursor = "grab";
    });

    slider.addEventListener("mouseup", () => {
        isDragging = false;
        slider.style.cursor = "grab";
    });

    // Движение мыши
    slider.addEventListener("mousemove", (e) => {
        if (!isDragging) return;
        e.preventDefault();
        const x = e.pageX - slider.offsetLeft;
        const walk = (x - startX) * 2; // Скорость прокрутки
        slider.scrollLeft = scrollLeft - walk;
    });

    // Поддержка сенсорных устройств
    slider.addEventListener("touchstart", (e) => {
        isDragging = true;
        startX = e.touches[0].pageX - slider.offsetLeft;
        scrollLeft = slider.scrollLeft;
    });

    slider.addEventListener("touchend", () => {
        isDragging = false;
    });

    slider.addEventListener("touchmove", (e) => {
        if (!isDragging) return;
        const x = e.touches[0].pageX - slider.offsetLeft;
        const walk = (x - startX) * 2; // Скорость прокрутки
        slider.scrollLeft = scrollLeft - walk;
    });
});
