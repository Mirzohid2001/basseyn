// static/js/share.js
document.querySelectorAll('.btn-share').forEach(btn => {
    btn.onclick = function(){
        let id = btn.getAttribute('data-id');
        let url = window.location.origin + '/products/' + id + '/';
        navigator.clipboard.writeText(url);
        btn.textContent = 'Скопировано!';
        setTimeout(()=>btn.textContent='Share',1200);
    };
});
