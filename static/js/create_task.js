const form = document.getElementById("taskForm");
const msg = document.getElementById("successMsg");

let hideTimer;

if (form) {
    form.addEventListener("submit", function (e) {
        e.preventDefault();

        // ---- GET VALUES ----
        const name = document.getElementById("name").value.trim();
        const startDate = document.getElementById("start_date").value;
        const endDate = document.getElementById("due_date").value;

        // ---- VALIDATION 1: TASK NAME ----
        if (!name) {
            alert("Task name is required");
            return;
        }

        // ---- VALIDATION 2: DATES ----
        if (startDate && endDate && startDate > endDate) {
            alert("Start date cannot be after end date");
            return;
        }

        const formData = new FormData(form);

        fetch("/add", {
            method: "POST",
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                msg.textContent = "✅ Task saved successfully";
                msg.style.display = "block";

                form.reset();

                clearTimeout(hideTimer);
                hideTimer = setTimeout(() => {
                    msg.style.display = "none";
                }, 3000);
            } else {
                alert(data.message || "Something went wrong");
            }
        })
        .catch(() => {
            alert("Server error");
        });
    });
}
