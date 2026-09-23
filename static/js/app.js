document.addEventListener("DOMContentLoaded", () => {
    console.log("PocketSmart AI JavaScript loaded successfully.");

    // Mobile navigation
    const menuButton = document.querySelector("#menuButton");
    const navMenu = document.querySelector("#navMenu");

    if (menuButton && navMenu) {
        menuButton.addEventListener("click", () => {
            navMenu.classList.toggle("active");
        });
    }

    // Password show/hide
    const passwordToggles = document.querySelectorAll("[data-password-toggle]");

    passwordToggles.forEach((button) => {
        button.addEventListener("click", () => {
            const targetId = button.getAttribute("data-password-toggle");
            const passwordInput = document.getElementById(targetId);

            if (!passwordInput) {
                return;
            }

            if (passwordInput.type === "password") {
                passwordInput.type = "text";
                button.textContent = "Hide";
            } else {
                passwordInput.type = "password";
                button.textContent = "Show";
            }
        });
    });

    // File name display
    const fileInputs = document.querySelectorAll('input[type="file"]');

    fileInputs.forEach((input) => {
        input.addEventListener("change", () => {
            const fileNameElement = document.querySelector(
                `[data-file-name="${input.id}"]`
            );

            if (!fileNameElement) {
                return;
            }

            if (input.files && input.files.length > 0) {
                fileNameElement.textContent = input.files[0].name;
            } else {
                fileNameElement.textContent = "No file selected";
            }
        });
    });

    // Budget input formatting
    const budgetInputs = document.querySelectorAll(
        'input[name="budget"]'
    );

    budgetInputs.forEach((input) => {
        input.addEventListener("input", () => {
            if (input.value < 0) {
                input.value = 0;
            }
        });
    });

    // Prevent accidental double submission
    const forms = document.querySelectorAll("form");

    forms.forEach((form) => {
        form.addEventListener("submit", () => {
            const submitButton = form.querySelector(
                'button[type="submit"]'
            );

            if (!submitButton) {
                return;
            }

            submitButton.disabled = true;

            const originalText = submitButton.textContent;

            submitButton.textContent = "Generating...";

            // Re-enable after 10 seconds in case the request fails
            setTimeout(() => {
                submitButton.disabled = false;
                submitButton.textContent = originalText;
            }, 10000);
        });
    });

    // Smooth scrolling
    const scrollLinks = document.querySelectorAll(
        'a[href^="#"]'
    );

    scrollLinks.forEach((link) => {
        link.addEventListener("click", (event) => {
            const targetId = link.getAttribute("href");

            if (!targetId || targetId === "#") {
                return;
            }

            const target = document.querySelector(targetId);

            if (!target) {
                return;
            }

            event.preventDefault();

            target.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
        });
    });

    // Automatically hide flash messages
    const alerts = document.querySelectorAll(".alert");

    alerts.forEach((alert) => {
        setTimeout(() => {
            alert.style.opacity = "1";

            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 5000);
    });
});