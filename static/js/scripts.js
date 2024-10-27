/*!
* Start Bootstrap - Bare v5.0.9 (https://startbootstrap.com/template/bare)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-bare/blob/master/LICENSE)
*/

// Adding bundled Bootstrap for refs


// $(document).ready( function () {
    // $('#Archiwum').DataTable();
// } );


// Function for displaying only up to 5 choices at a time in the form select
// when user inputs something it dynamically updates the choices to fit the input

function setupHourInputs() {
    // Get the input fields and datalist elements for start and end hour
    const startHourInput = document.querySelector('input[name="start_hour"]');
    const endHourInput = document.querySelector('input[name="end_hour"]');
    const hourDatalist = document.getElementById('hour_list');

    // Check if elements exist to avoid errors
    if (!startHourInput || !endHourInput || !hourDatalist) return;

    const allOptions = Array.from(hourDatalist.options);

    function showLimitedOptions() {
        hourDatalist.innerHTML = '';
        const limitedOptions = allOptions.slice(0, 5);
        limitedOptions.forEach(option => {
            let optionClone = option.cloneNode(true);
            hourDatalist.appendChild(optionClone);
        });
    }

    function filterOptions(inputElement) {
        const filterText = inputElement.value.toLowerCase();
        hourDatalist.innerHTML = '';

        const filteredOptions = allOptions.filter(option =>
            option.value.toLowerCase().startsWith(filterText)
        ).slice(0, 5);

        if (filteredOptions.length > 0) {
            filteredOptions.forEach(option => {
                let optionClone = option.cloneNode(true);
                hourDatalist.appendChild(optionClone);
            });
        } else {
            const noOption = document.createElement('option');
            noOption.value = 'No matching options';
            hourDatalist.appendChild(noOption);
        }
    }

    function handleInput(event){
        console.log("Input value on focus:", event.target.value);
        if (event.target.value === ''){
            showLimitedOptions();
        } else {
            filterOptions(event.target);
        }
    }

    startHourInput.addEventListener('input', handleInput);
    startHourInput.addEventListener('focus',showLimitedOptions);
    endHourInput.addEventListener('input', handleInput);
    endHourInput.addEventListener('focus',showLimitedOptions);
    
    showLimitedOptions();

}

// Call setupHourInputs on page load
document.addEventListener('DOMContentLoaded', function(){
    setupHourInputs();
});
// Call setupHourInputs on model popup
document.addEventListener('shown.bs.modal', function(event){
    const modalElement = event.target;
    if (modalElement.classList.contains('modal')){
        setupHourInputs();
    }
});


