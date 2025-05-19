const getButton = document.querySelector('#getButton'); 
const allSongsDiv = document.querySelector('#allSongs');

getButton.addEventListener('click', async () => {
    try {
        const res = await fetch('http://127.0.0.1:8000/api/song/')
        const data = await res.json(); 

        if(res.ok) {
            allSongsDiv.innerHTML = data.map(song => 
                `<h3>${song.title}</h3>`
            ).join(''); 
        } else {
            allSongsDiv.innerHTML = `<p>${JSON.stringify(data)}</p>`; 
        }
    } catch (error) {
        allSongsDiv.innerHTML = `<p>Request failed ${error.message}</p>`;
    }
})