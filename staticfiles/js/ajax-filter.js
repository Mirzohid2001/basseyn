// static/js/ajax-filter.js
document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('filter-form');
    if (!form) return;
    form.addEventListener('submit', function(e){
        e.preventDefault();
        let url = form.action || window.location.pathname;
        url += '?' + new URLSearchParams(new FormData(form)).toString();
        fetch(url, {headers: {"X-Requested-With":"XMLHttpRequest"}})
            .then(r=>r.text())
            .then(html=>{
                let parser = new DOMParser();
                let doc = parser.parseFromString(html, 'text/html');
                let newList = doc.querySelector('#product-list');
                if(newList) document.getElementById('product-list').innerHTML = newList.innerHTML;
            });
    });
});
