document.addEventListener("DOMContentLoaded", () => {
    const typeButtons = document.querySelectorAll(".type-button");

    typeButtons.forEach(button => {
        button.addEventListener("click", () => {
            const checkbox = button.querySelector("input[type='checkbox']");
            checkbox.checked = !checkbox.checked;

            if (checkbox.checked) {
                button.classList.add("selected");
            } else {
                button.classList.remove("selected");
            }
        });
    });
});
