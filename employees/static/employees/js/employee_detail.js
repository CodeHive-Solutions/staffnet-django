document.addEventListener("DOMContentLoaded", function () {
    const tabLinks = document.querySelectorAll(".tab-link");
    const tabContents = document.querySelectorAll(".tab-content");

    tabLinks.forEach((link) => {
        link.addEventListener("click", function () {
            // Remove active styles from all tabs
            tabLinks.forEach((tab) => tab.classList.remove("active-tab"));
            tabContents.forEach((content) => content.classList.add("hidden"));

            // Add active styles to the clicked tab and show the content
            this.classList.add("active-tab");
            const target = document.querySelector(this.dataset.target);
            target.classList.remove("hidden");
        });
    });
});
