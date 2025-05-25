// static/js/order-modal.js
document.addEventListener("DOMContentLoaded", function(){
    document.querySelectorAll('.btn-order-modal').forEach(btn => {
        btn.addEventListener('click', function() {
            const productId = btn.getAttribute('data-product');
            document.getElementById('orderModalProductId').value = productId;
            const modal = new bootstrap.Modal(document.getElementById('orderModal'));
            modal.show();
        });
    });

    const orderForm = document.getElementById('orderModalForm');
    if(orderForm){
        orderForm.addEventListener('submit', function(e){
            e.preventDefault();
            let formData = new FormData(orderForm);
            fetch("/order/", {  // yoki {% url 'order_create' %}
                method: "POST",
                headers: {"X-Requested-With": "XMLHttpRequest"},
                body: formData
            })
            .then(res => res.ok ? res.text() : Promise.reject())
            .then(() => {
                orderForm.querySelector('.order-modal-success').style.display = "block";
                setTimeout(() => {
                    const modal = bootstrap.Modal.getInstance(document.getElementById('orderModal'));
                    modal.hide();
                    orderForm.reset();
                    orderForm.querySelector('.order-modal-success').style.display = "none";
                }, 1800);
            });
        });
    }
});
