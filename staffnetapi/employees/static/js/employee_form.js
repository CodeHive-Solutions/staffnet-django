
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
// document.addEventListener('DOMContentLoaded', function () {
//     const salaryInput = document.getElementById('id_employment_details-salary');
//     salaryInput.addEventListener('change', function (event) {
//         const salary = event.target.value;
//         console.log(salary);
//         event.target.value = new Intl.NumberFormat('es-CO', {
//             style: 'currency',
//             currency: 'COP',
//             minimumFractionDigits: 0,
//         }).format(salary);
//     });
// });