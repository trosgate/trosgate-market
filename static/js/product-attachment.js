
//Script for Proposal Serach
$(document).ready(function(){
    $(".product-checked").on('click', function(){
        let _productObj = {};
        $(".product-checked").each(function(index,ele){
            let _productVal = $(this).val();
            let _productKey = $(this).data('filter');
            
            _productObj[_productKey] = Array.from(document.querySelectorAll('input[data-filter='+_productKey+']:checked')).map(function(el){
                return el.value;
            });
            
        });
        const product_id = document.querySelector('#product_id').textContent.replaceAll('"', '')
	
        $.ajax({
            url: `/proposal/add/${product_id}`,
            data: _productObj,
            dataType: 'json',
            
            success: function (json) {
                document.getElementById("productTotal").innerHTML = json.totalprice;
            },
            error: function (xhr, errmsg, err) {}
        });
    });
});