const form = document.querySelector('#songUploadForm');
const responseDiv = document.querySelector('#response');

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(form); 
    const jsonData = Object.fromEntries(formData.entries()); 

    try {
        const res = await fetch('http://127.0.0.1:8000/api/song/', {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(jsonData)
        }); 

        const data = await res.json();

        if (res.ok) {
            responseDiv.innerHTML = `<p>Song uploaded successfully!</p>`;
        } else {
            responseDiv.innerHTML = `<p>Error: ${JSON.stringify(data)}</p>`;
        }
    } catch (error) {
        responseDiv.innerHTML = `<p>Request failed: ${error.message}</p>`;
    }
});