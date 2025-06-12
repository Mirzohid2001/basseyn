// static/js/lastview.js
let id = ... // product.id
let viewed = JSON.parse(localStorage.getItem('lastviewed') || '[]');
if(!viewed.includes(id)){
    viewed.unshift(id);
    if(viewed.length>10) viewed = viewed.slice(0,10);
    localStorage.setItem('lastviewed', JSON.stringify(viewed));
}
