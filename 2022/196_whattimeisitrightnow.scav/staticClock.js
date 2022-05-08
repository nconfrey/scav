let dateInput = document.getElementById('dateInput');
let timeInput = document.getElementById('timeInput'); 

dateInput.addEventListener('input', handleInputEvent);
timeInput.addEventListener('input', handleInputEvent);

let lastDate = '';
let lastTime = '';

function handleInputEvent(e) {
    if (!(dateInput.value && timeInput.value) || (lastDate == dateInput.value && lastTime == timeInput.value)) {
        return;
    }
    const dateString = dateInput.value + 'T' + timeInput.value + ':00-05:00';
    const date = new Date(dateString);
    let staticClock = document.getElementById('staticClock');
    staticClock.innerHTML = `<analog-clock class="clock" time="${date.getTime()}"></analog-clock>`;
}
