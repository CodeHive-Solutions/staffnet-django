
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
