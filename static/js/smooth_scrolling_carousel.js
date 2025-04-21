document.addEventListener("DOMContentLoaded", () => {
    const track = document.querySelector(".carousel-track");
    const images = Array.from(track.children);

    // Дублируем изображения для бесконечной прокрутки
    images.forEach(image => {
        const clone = image.cloneNode(true);
        track.appendChild(clone);
    });
});
