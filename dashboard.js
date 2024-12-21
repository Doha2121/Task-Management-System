document.getElementById('addTaskForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent form from submitting the default way

    const taskTitle = document.getElementById('taskTitle').value;
    const taskDescription = document.getElementById('taskDescription').value;
    const taskDueDate = document.getElementById('taskDueDate').value;
    const taskCategory = document.getElementById('taskCategory').value;

    if (taskTitle && taskDescription && taskDueDate) {
        fetch('/add', {
            method: 'POST',
            body: new URLSearchParams({
                'title': taskTitle,
                'description': taskDescription,
                'due_date': taskDueDate,
                'category': taskCategory
            }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Create a new list item for the new task
                const newTaskItem = document.createElement('li');
                newTaskItem.classList.add('task-item');
                newTaskItem.setAttribute('data-task-id', data.task_id);  // Set task ID as an attribute
                newTaskItem.innerHTML = `
                    <h4>${data.task_title}</h4>
                    <p>${data.task_description}</p>
                    <p><strong>Due Date:</strong> ${data.task_due_date}</p>
                    <p><strong>Category:</strong> ${data.task_category}</p>
                    <button onclick="deleteTask(${data.task_id})">Delete</button>
                    <button onclick="editTask(${data.task_id})">Edit</button>
                `;

                // Append the new task to the task list
                document.getElementById('taskList').appendChild(newTaskItem);

                // Clear the form inputs
                document.getElementById('taskTitle').value = '';
                document.getElementById('taskDescription').value = '';
                document.getElementById('taskDueDate').value = '';
                document.getElementById('taskCategory').value = '';

                alert('Task added successfully!');
            } else {
                alert('Failed to add task: ' + data.message);
            }
        });
    } else {
        alert('Please fill all fields');
    }
});

// Edit task function
function editTask(taskId) {
    // Redirect to the update page for the task (or use a modal form to update)
    window.location.href = `/update/${taskId}`;
}

// Delete task function
function deleteTask(taskId) {
    const taskItem = document.querySelector(`[data-task-id='${taskId}']`);
    
    if (confirm('Are you sure you want to delete this task?')) {
        fetch(`/delete/${taskId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                taskItem.remove();  // Remove the task from the list
                alert('Task deleted successfully!');
            } else {
                alert('Failed to delete task');
            }
        });
    }
}
