
//Script for Freelancer Serach
$(document).ready(function(){
    $(".freelancer-checked").on('click', function(){
        let _freelancerObj = {};
        $(".freelancer-checked").each(function(index,ele){
            let _freelancerVal = $(this).val();
            let _freelancerKey = $(this).data('filter');
            _freelancerObj[_freelancerKey] = Array.from(document.querySelectorAll('input[data-filter='+_freelancerKey+']:checked')).map(function(el){
                return el.value;
            });
            
        });

        $.ajax({
            url: '/freelancer/freelancer_search/', 
            data: _freelancerObj,
            dataType: 'json',
            beforeSend:function(){
                
            },
            success: function (json) {
                document.getElementById("freelancerTotal").innerHTML = json.totalcount;
                $('#freelancerSuccessFilter').html(json.freelancer_list);
            },
            error: function (xhr, errmsg, err) {}
        });
    });
});