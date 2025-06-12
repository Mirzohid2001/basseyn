// static/js/compare.js
document.querySelectorAll('.btn-compare').forEach(btn => {
    btn.onclick = function(){
        let id = btn.getAttribute('data-id');
        let cmp = JSON.parse(localStorage.getItem('compare') || '[]');
        if(!cmp.includes(id)) cmp.push(id);
        localStorage.setItem('compare', JSON.stringify(cmp));
        btn.textContent = 'В сравнении!';
    };
});
