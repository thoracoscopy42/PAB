document.addEventListener("DOMContentLoaded", function () {
    const modal = document.querySelector("[data-modal]");

    if (!modal) {
        return;
    }

    const closeButtons = document.querySelectorAll("[data-modal-close]");

    modal.classList.add("modal-visible");

    closeButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            modal.classList.remove("modal-visible");
        });
    });

    modal.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.classList.remove("modal-visible");
        }
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            modal.classList.remove("modal-visible");
        }
    });
});