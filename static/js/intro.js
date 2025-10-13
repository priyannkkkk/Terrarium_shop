document.addEventListener('DOMContentLoaded', function() {
    const introScreen = document.getElementById('video-intro');
    const introVideo = document.getElementById('intro-video');
    const mainContent = document.getElementById('main-content');
    
    const hiddenClass = 'main-content-hidden-on-load'; // Define the class name

    // Fallback timer: If the video fails to fire 'onended' for any reason, force the transition after 9 seconds.
    const fallbackTimer = setTimeout(() => {
        if (introScreen && introScreen.style.opacity === '1') {
            handleTransitionStart();
        }
    }, 9000); 

    introVideo.onended = handleTransitionStart;

    function handleTransitionStart() {
        clearTimeout(fallbackTimer);
        
        introScreen.classList.add('fade-out');
        introScreen.addEventListener('transitionend', handleTransitionEnd, { once: true });
        
        // When transition starts, remove 'display: none' but keep opacity 0
        mainContent.style.display = 'block';
    }

    function handleTransitionEnd() {
        // 1. Remove the intro overlay completely
        introScreen.style.display = 'none';

        // 2. Remove the initial hidden class and start the fade-in
        mainContent.classList.remove(hiddenClass);
        mainContent.style.opacity = '1'; 
    }
});