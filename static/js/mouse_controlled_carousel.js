document.addEventListener("DOMContentLoaded", () => {
    const carousels = document.querySelectorAll(".mouse-carousel");

    carousels.forEach((carousel) => {
        const track = carousel.querySelector(".mouse-carousel-track");
        let isDragging = false;
        let startX;
        let currentTranslate = 0;
        let prevTranslate = 0;
        let isMouseOver = false;

        // Начало перетаскивания
        carousel.addEventListener("mousedown", (e) => {
            isDragging = true;
            startX = e.clientX;
            carousel.style.cursor = "grabbing";
        });

        // Завершение перетаскивания
        carousel.addEventListener("mouseup", () => {
            isDragging = false;
            prevTranslate = currentTranslate;
            carousel.style.cursor = "grab";
        });

        carousel.addEventListener("mouseleave", () => {
            isDragging = false;
            prevTranslate = currentTranslate;
            carousel.style.cursor = "grab";
        });

        // Движение мыши
        carousel.addEventListener("mousemove", (e) => {
            if (isDragging) {
                const currentX = e.clientX;
                const deltaX = currentX - startX;
                currentTranslate = prevTranslate + deltaX;
                track.style.transform = `translateX(${currentTranslate}px)`;
            } else if (isMouseOver) {
                const carouselRect = carousel.getBoundingClientRect();
                const mouseX = e.clientX - carouselRect.left; // Позиция мыши относительно карусели
                const trackWidth = track.scrollWidth;
                const carouselWidth = carousel.offsetWidth;

                // Рассчитываем смещение трека
                const maxScroll = trackWidth - carouselWidth;
                const scrollPosition = (mouseX / carouselWidth) * maxScroll;

                track.style.transform = `translateX(${-scrollPosition}px)`;
            }
        });

        // Поддержка сенсорных устройств
        carousel.addEventListener("touchstart", (e) => {
            isDragging = true;
            startX = e.touches[0].clientX;
        });

        carousel.addEventListener("touchend", () => {
            isDragging = false;
            prevTranslate = currentTranslate;
        });

        carousel.addEventListener("touchmove", (e) => {
            if (!isDragging) return;
            const currentX = e.touches[0].clientX;
            const deltaX = currentX - startX;
            currentTranslate = prevTranslate + deltaX;
            track.style.transform = `translateX(${currentTranslate}px)`;
        });

        // Включаем обработку движения мыши при наведении
        carousel.addEventListener("mouseenter", () => {
            isMouseOver = true;
        });

        // Отключаем обработку движения мыши при уходе
        carousel.addEventListener("mouseleave", () => {
            isMouseOver = false;
        });
    });
});
