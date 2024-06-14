// frontend/report.js
document.getElementById('generate-report').addEventListener('click', async () => {
    const token = localStorage.getItem('token');
    if (!token) {
        alert('Please login first');
        return;
    }

    const response = await fetch('http://localhost:8001/report', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ role: 'ace' })  // замените на нужную роль
    });

    const report = await response.json();
    alert(`Report content: ${report.content}`);
});
