document.getElementById('addTaskBtn').addEventListener('click', function() {
    const taskTitle = document.getElementById('taskTitle').value;
    const taskDescription = document.getElementById('taskDescription').value;
    const taskTime = document.getElementById('taskTime').value;

    if (taskTitle && taskDescription && taskTime) {
        const taskList = document.getElementById('taskList');
        const newTask = document.createElement('li');
        newTask.textContent = `${taskTitle} - ${taskDescription} at ${taskTime}`;
        taskList.appendChild(newTask);

        // Clear the input fields after task is added
        document.getElementById('taskTitle').value = '';
        document.getElementById('taskDescription').value = '';
        document.getElementById('taskTime').value = '';
    } else {
        alert('Please fill in all task details!');
    }
});
