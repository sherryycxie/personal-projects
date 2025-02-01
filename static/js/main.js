document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('uploadForm');
    const submitBtn = document.getElementById('submitBtn');
    const processingMessage = document.getElementById('processingMessage');
    const fileInput = document.getElementById('audio_file');

    form.addEventListener('submit', function(e) {
        // Check file size
        const file = fileInput.files[0];
        if (file && file.size > 16 * 1024 * 1024) { // 16MB
            e.preventDefault();
            alert('File size must be less than 16MB');
            return;
        }

        // Show processing message and disable submit button
        submitBtn.disabled = true;
        processingMessage.classList.remove('d-none');
    });

    // File input validation
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const fileType = file.type.toLowerCase();
            // Extended list of valid MIME types for audio files
            const validTypes = [
                'audio/wav',
                'audio/mpeg',
                'audio/ogg',
                'audio/mp4',
                'audio/x-m4a',    // Common MIME type for .m4a
                'audio/aac',      // Another possible MIME type for .m4a
                'video/mp4'       // Some browsers report .m4a as video/mp4
            ];

            // Also check file extension
            const extension = file.name.split('.').pop().toLowerCase();
            const validExtensions = ['wav', 'mp3', 'ogg', 'm4a'];

            if (!validTypes.includes(fileType) && !validExtensions.includes(extension)) {
                fileInput.value = '';
                alert('Please select a valid audio file (WAV, MP3, OGG, or M4A)');
                console.log('Invalid file type:', fileType, 'Extension:', extension);
            } else {
                console.log('File accepted:', file.name, 'Type:', fileType);
            }
        }
    });
});