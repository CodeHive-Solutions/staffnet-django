
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

document.addEventListener('DOMContentLoaded', function () {
    const salaryInput = document.getElementById('id_employment_details-salary');
    if (salaryInput) {
        salaryInput.addEventListener('input', function (e) {
            // Remove non-numeric characters (except dot or comma for decimals)
            let value = e.target.value.replace(/[^0-9.]/g, '');

            // Convert to float and format as COP
            if (value) {
                value = parseFloat(value.replace(/,/g, '')).toFixed(2); // Ensure decimal format
                e.target.value = new Intl.NumberFormat('es-CO', {
                    style: 'currency',
                    currency: 'COP',
                    minimumFractionDigits: 0, // For COP, no cents are typically used
                }).format(value);
            }
        });
    }
});