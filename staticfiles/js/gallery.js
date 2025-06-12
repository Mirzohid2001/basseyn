// static/js/gallery.js
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.product-gallery').forEach(function(gallery) {
        const imgs = gallery.querySelectorAll('.gallery-img');
        let current = 0;
        function show(idx) {
            imgs.forEach((img, i) => img.classList.toggle('active', i === idx));
        }
        gallery.querySelector('.gallery-prev')?.addEventListener('click', function(){
            current = (current-1+imgs.length)%imgs.length; show(current);
        });
        gallery.querySelector('.gallery-next')?.addEventListener('click', function(){
            current = (current+1)%imgs.length; show(current);
        });
    });
});
