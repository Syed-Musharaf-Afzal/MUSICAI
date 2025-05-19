document.addEventListener('DOMContentLoaded', function() {
    const textInput = document.getElementById('text-input');
    const emotionSelect = document.getElementById('emotion-select');
    const generateBtn = document.getElementById('generate-btn');
    const resultBox = document.getElementById('result-box');
    const emotionIcon = document.getElementById('emotion-icon');
    const emotionText = document.getElementById('emotion-text');
    const originalText = document.getElementById('original-text');
    const playBtn = document.getElementById('play-btn');
    const downloadBtn = document.getElementById('download-btn');
    
    let currentFile = null;
    
    // Emotion icons mapping
    const emotionIcons = {
        'happy': '😊',
        'sad': '😢',
        'angry': '😠',
        'neutral': '😐'
    };
    
    generateBtn.addEventListener('click', generateMusic);
    playBtn.addEventListener('click', playMusic);
    
    async function generateMusic() {
        const text = textInput.value.trim();
        if (!text) {
            alert('Please enter some text');
            return;
        }
        
        generateBtn.disabled = true;
        generateBtn.textContent = 'Generating...';
        
        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `text=${encodeURIComponent(text)}&emotion=${emotionSelect.value}`
            });
            
            const data = await response.json();
            
            if (data.success) {
                currentFile = data.file;
                updateUI(data);
                resultBox.classList.remove('hidden');
            } else {
                alert('Error generating music');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to generate music');
        } finally {
            generateBtn.disabled = false;
            generateBtn.textContent = 'Generate Music';
        }
    }
    
    function updateUI(data) {
        // Set emotion display
        emotionIcon.textContent = emotionIcons[data.emotion] || '🎵';
        emotionText.textContent = data.emotion.charAt(0).toUpperCase() + data.emotion.slice(1);
        emotionText.className = data.emotion;
        
        // Set original text
        originalText.textContent = `"${data.text}"`;
        
        // Set download link
        downloadBtn.href = `/static/sounds/${data.file}`;
        downloadBtn.download = `music_${data.emotion}.mid`;
    }
    
    async function playMusic() {
        if (!currentFile) return;
        
        playBtn.disabled = true;
        playBtn.textContent = 'Playing...';
        
        try {
            const response = await fetch(`/play/${currentFile}`);
            const data = await response.json();
            
            if (!data.success) {
                alert('Error playing music: ' + (data.error || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to play music');
        } finally {
            playBtn.disabled = false;
            playBtn.textContent = '▶ Play';
        }
    }
});