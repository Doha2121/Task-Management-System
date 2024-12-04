const addTaskBtn = document.getElementById("addTaskBtn");
const taskTitle = document.getElementById("taskTitle");
const taskDescription = document.getElementById("taskDescription");
const taskTime = document.getElementById("taskTime");
const taskList = document.getElementById("taskList");

addTaskBtn.addEventListener("click", () => {
    const titleText = taskTitle.value.trim();
    const descriptionText = taskDescription.value.trim();
    const timeText = taskTime.value;

    // Validate input fields
    if (titleText === "" || descriptionText === "" || timeText === "") {
        alert("Please fill out all fields before adding a task!");
        return;
    }

    // Create a new list item for the task
    const taskItem = document.createElement("li");
    taskItem.className = "task";

    // Create a checkbox for the task
    const taskCheckbox = document.createElement("input");
    taskCheckbox.type = "checkbox";

    // Create the task title
    const taskTitleElement = document.createElement("p");
    taskTitleElement.textContent = `Title: ${titleText}`;

    // Create the task description
    const taskDescriptionElement = document.createElement("p");
    taskDescriptionElement.textContent = `Description: ${descriptionText}`;

    // Create the task time
    const taskTimeElement = document.createElement("p");
    taskTimeElement.textContent = `Time: ${timeText}`;

    // Create the delete button for the task
    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "Delete";

    // Add event listener to the delete button to remove task
    deleteBtn.addEventListener("click", () => {
        taskList.removeChild(taskItem);
    });

    // Add event listener to the checkbox to handle completion
    taskCheckbox.addEventListener("change", () => {
        if (taskCheckbox.checked) {
            taskItem.classList.add("celebrate");
            setTimeout(() => {
                taskList.removeChild(taskItem);
                alert("Congratulations on finishing your task!");
            }, 1000);
        }
    });

    // Append the title, description, time, checkbox, and delete button to the task item
    taskItem.appendChild(taskCheckbox);
    taskItem.appendChild(taskTitleElement);
    taskItem.appendChild(taskDescriptionElement);
    taskItem.appendChild(taskTimeElement);
    taskItem.appendChild(deleteBtn);

    // Add the task item to the task list
    taskList.appendChild(taskItem);

    // Clear the input fields after adding the task
    taskTitle.value = "";
    taskDescription.value = "";
    taskTime.value = "";
});
