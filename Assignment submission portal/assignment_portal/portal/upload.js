fetch('http://127.0.0.1:8000/api/upload/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        user_id: 1,  // Ensure the user_id exists
        task: "Submit Assignment", // Task data is valid
        admin: "admin1" // Ensure the admin username exists
    }),
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));


function uploadAssignment() {
    const formData = new FormData(); // Use FormData for file uploads
    formData.append('user_id', 1); // Add other fields
    formData.append('task', 'Hello World');
    formData.append('admin', 'admin1');
    const fileInput = document.querySelector('input[type="file"]'); // Make sure you have a file input in your HTML
    if (fileInput.files.length > 0) {
        formData.append('file', fileInput.files[0]); // Append the selected file
    }

    fetch('http://127.0.0.1:8000/api/upload/', {
        method: 'POST',
        body: formData, // Send the form data
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => console.log(data))
    .catch(error => console.error('There was a problem with the fetch operation:', error));
}
