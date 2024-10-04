/*!
* Start Bootstrap - Bare v5.0.9 (https://startbootstrap.com/template/bare)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-bare/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

// $(document).ready( function () {
    // $('#Archiwum').DataTable();
// } );


// Function for displaying only up to 5 choices at a time in the form select
// when user inputs something it dynamically updates the choices to fit the input
document.addEventListener('DOMContentLoaded', function() {
    // Get the input fields and datalist elements for start and end hour
    const startHourInput = document.querySelector('input[name="start_hour"]');
    const endHourInput = document.querySelector('input[name="end_hour"]');
    const hourDatalist = document.getElementById('hour_list');

    // Create a clone of the initial datalist options to preserve all of them
    const allOptions = Array.from(hourDatalist.options);  // Keep all options intact

    // Function to show only the first 5 options
    function showLimitedOptions() {
        hourDatalist.innerHTML = '';  // Clear existing options

        // Ensure exactly 5 options are appended
        const limitedOptions = allOptions.slice(0, 5);  // Show first 5 options
        limitedOptions.forEach(option => {
            let optionClone = option.cloneNode(true);  // Clone the option to avoid issues
            hourDatalist.appendChild(optionClone);  // Append cloned option
        });
    }

    // Function to filter the options based on user input, matching cases
    function filterOptions(inputElement) {
        const filterText = inputElement.value.toLowerCase();
        hourDatalist.innerHTML = '';  // Clear existing options

        const filteredOptions = allOptions.filter(option => 
            option.value.toLowerCase().startsWith(filterText)
        ).slice(0, 5);  // Show only 5 matching options

        // If there are matching options, append them
        if (filteredOptions.length > 0) {
            filteredOptions.forEach(option => {
                let optionClone = option.cloneNode(true);  // Clone each filtered option
                hourDatalist.appendChild(optionClone);  // Append cloned option
            });
        } else {
            // If no match, show a message or handle it gracefully
            const noOption = document.createElement('option');
            noOption.value = 'No matching options';
            hourDatalist.appendChild(noOption);
        }
    }

    // Initially show the limited options (first 5)
    showLimitedOptions();

    // Add event listeners for both inputs
    startHourInput.addEventListener('input', function() {
        if (startHourInput.value === '') {
            showLimitedOptions();  // Reset to first 5 options if input is empty
        } else {
            filterOptions(startHourInput);  // Filter based on user input (matching case)
        }
    });

    endHourInput.addEventListener('input', function() {
        if (endHourInput.value === '') {
            showLimitedOptions();  // Reset to first 5 options if input is empty
        } else {
            filterOptions(endHourInput);  // Filter based on user input (matching case)
        }
    });
});

