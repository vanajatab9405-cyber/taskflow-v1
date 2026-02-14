const filterName = document.getElementById('filterName');
const filterStartDate = document.getElementById('filterStartDate');
const filterEndDate = document.getElementById('filterEndDate');
const sortAlpha = document.getElementById('sortAlpha');
const tasksContainer = document.getElementById('tasksContainer');

function filterTasks() {
    const nameVal = filterName.value.toLowerCase();
    const startVal = filterStartDate.value;
    const endVal = filterEndDate.value;

    let tasks = Array.from(tasksContainer.children);

    tasks.forEach(task => {
        const tName = task.dataset.name.toLowerCase();
        const tStart = task.dataset.startDate;
        const tEnd = task.dataset.endDate;

        const matchesName = tName.includes(nameVal);
        const matchesStart = !startVal || tStart >= startVal;
        const matchesEnd = !endVal || tEnd <= endVal;

        task.style.display = (matchesName && matchesStart && matchesEnd) ? 'block' : 'none';
    });
}

function sortTasks() {
    const direction = sortAlpha.value;
    let tasks = Array.from(tasksContainer.children);

    tasks.sort((a, b) => {
        let nameA = a.dataset.name.toLowerCase();
        let nameB = b.dataset.name.toLowerCase();
        if (direction === 'asc') return nameA.localeCompare(nameB);
        if (direction === 'desc') return nameB.localeCompare(nameA);
        return 0;
    });

    tasks.forEach(task => tasksContainer.appendChild(task));
}

filterName.addEventListener('input', filterTasks);
filterStartDate.addEventListener('change', filterTasks);
filterEndDate.addEventListener('change', filterTasks);
sortAlpha.addEventListener('change', sortTasks);

document.getElementById('backBtn').addEventListener('click', () => {
    window.location.href = '/create';
});

// DELETE TASK
document.querySelectorAll(".delete-icon").forEach(icon => {
    icon.addEventListener("click", function (e) {
        e.preventDefault();

        const taskId = this.dataset.id;

        if (!confirm("Delete this task?")) return;

        fetch(`/delete/${taskId}`, {
            method: "POST"
        })
        .then(() => location.reload());
    });
});

// EDIT TASK
document.querySelectorAll(".edit-icon").forEach(icon => {
    icon.addEventListener("click", function () {
        const taskId = this.dataset.id;
        window.location.href = `/edit/${taskId}`;
    });
});

document.querySelectorAll(".delete-icon").forEach(btn => {
    btn.addEventListener("click", function () {
        const taskId = this.dataset.id;

        const ok = confirm("Are you sure you want to delete this task?");
        if (!ok) return;

        fetch(`/delete/${taskId}`, {
            method: "POST"
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert("Delete failed");
            }
        })
        .catch(() => alert("Server error"));
    });
});

document.querySelectorAll(".task-card").forEach(card => {
    const dueDateStr = card.dataset.endDate;
    const status = card.querySelector(".status").innerText.toLowerCase();

    if (!dueDateStr) return;

    const today = new Date();
    today.setHours(0,0,0,0);

    const dueDate = new Date(dueDateStr);
    dueDate.setHours(0,0,0,0);

    if (dueDate < today && status !== "completed") {
        card.classList.add("overdue");
        card.querySelector(".overdue-msg").style.display = "block";
    }
});
