const button = document.getElementById('moves3');
const div1 = document.getElementById('text1');
const div2 = document.getElementById('rdivo');

button.addEventListener('click', () => {
    div1.style.display = 'none';
    div2.style.display = 'block'; // Change this to 'flex', 'grid', or 'block' if you prefer
});


const button2 = document.getElementById('moves2');

button2.addEventListener('click', () => {
    div1.style.display = 'block';
    div2.style.display = 'none'; // Change this to 'flex', 'grid', or 'block' if you prefer
});

document.getElementById('back-button').addEventListener('click', () => {
    window.history.back();
});