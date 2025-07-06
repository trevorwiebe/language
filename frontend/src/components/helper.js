// Show selected file name
document.getElementById('audioFile').addEventListener('change', function() {
    const fileName = this.files[0] ? this.files[0].name : '';
    document.getElementById('audioFileName').textContent = fileName;
});