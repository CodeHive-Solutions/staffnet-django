window.addEventListener("load", function () {
    var dateFields = document.querySelectorAll(".vDateField");

    dateFields.forEach(function (field) {
        // Only convert if the type is not already 'date'
        if (field.getAttribute("type") !== "date") {
            field.classList.add("vTextField");
            field.setAttribute("type", "date");
        }

        // Ensure the value is formatted as YYYY-MM-DD for date inputs
        let value = field.defaultValue;
        if (value) {
            // Detect if the value is in DD/MM/YYYY format and reformat
            let parts = value.split("/");
            if (parts.length === 3 && parts[0].length === 2 && parts[1].length === 2 && parts[2].length === 4) {
                let formattedValue = `${parts[2]}-${parts[1]}-${parts[0]}`;
                // Set the value directly in the correct format
                field.value = formattedValue;
            }
        }
    });
});

// Remove the interaction of the input type number with the mouse wheel and arrow keys
window.addEventListener("load", function () {
    var numberFields = document.querySelectorAll(".vIntegerField, .vFloatField");

    numberFields.forEach(function (field) {
        field.addEventListener("mousewheel", function (e) {
            e.preventDefault();
        });

        field.addEventListener("keydown", function (e) {
            if (e.key === "ArrowUp" || e.key === "ArrowDown") {
                e.preventDefault();
            }
        });
    });
});

// Format the value of the inputs with the name 'salary' and 'transportation_allowance' to COP currency
function formatToCOP(value) {
    const formattedValue = new Intl.NumberFormat("es-CO", {
        style: "currency",
        currency: "COP",
        minimumFractionDigits: 0,
    }).format(value);

    console.log(formattedValue);
    return formattedValue.replace(/,00$/, ""); // Optionally remove cents
}

// Function to handle formatting input value
function formatInput(input) {
    // Remove any non-digit characters
    const value = input.value.replace(/\D/g, "");
    if (value) {
        input.value = formatToCOP(value);
    }
}

// Get input elements
const salaryInput = document.querySelector('input[name="salary"]');
const transportationAllowanceInput = document.querySelector('input[name="transportation_allowance"]');

// Add event listeners
salaryInput.addEventListener("input", () => formatInput(salaryInput));
transportationAllowanceInput.addEventListener("input", () => formatInput(transportationAllowanceInput));

// Add event listeners
salaryInput.addEventListener("input", () => formatInput(salaryInput));
transportationAllowanceInput.addEventListener("input", () => formatInput(transportationAllowanceInput));
console.log("Script executed successfully");
