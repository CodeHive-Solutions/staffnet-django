
document.addEventListener('DOMContentLoaded', function () {
    const photoInput = document.getElementById('id_personal_info-photo');
    const preview = document.getElementById('profile-picture-preview');
    const fileNameSpan = document.getElementById('file-name');

    photoInput.addEventListener('change', function (event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                preview.src = e.target.result;
            };
            reader.readAsDataURL(file);
            fileNameSpan.textContent = file.name;
        }
    });
});

// Format the salary in COP
document.addEventListener('DOMContentLoaded', function () {
    function formatCurrency(event) {
        const salary = event.target.value
        event.target.value = new Intl.NumberFormat('es-CO', {
            style: 'currency',
            currency: 'COP',
            minimumFractionDigits: 0
        }).format(salary)
    }
    function restrictInput(event) {
        const salary = event.target.value
        event.target.value = salary.replace(/[^0-9]/g, '')
    }

    const salaryInput = document.getElementById('id_salary')
    const transportAllowanceInput = document.getElementById('id_transportation_allowance')
    salaryInput.addEventListener('change', formatCurrency)
    salaryInput.addEventListener('input', restrictInput)
    transportAllowanceInput.addEventListener('change', formatCurrency)
    transportAllowanceInput.addEventListener('input', restrictInput)
})

// Remove the currency format when submitting the form
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('employee-form')
    form.addEventListener('submit', function () {
        const salaryInput = document.getElementById('id_salary')
        const transportAllowanceInput = document.getElementById('id_transportation_allowance')
        console.log(salaryInput.value)
        console.log(transportAllowanceInput.value)
        salaryInput.value = salaryInput.value.replace(/[^0-9]/g, '')
        transportAllowanceInput.value = transportAllowanceInput.value.replace(/[^0-9]/g, '')
    })
})