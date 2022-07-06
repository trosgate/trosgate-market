
//Script for Proposal Serach
$(document).ready(function(){
    $('.ajaxLoader').hide();
    $(".proposal-checked").on('click', function(){
        let _proposalObj = {};
        $(".proposal-checked").each(function(index,ele){
            let _proposalVal = $(this).val();
            let _proposalKey = $(this).data('filter');
            
            _proposalObj[_proposalKey] = Array.from(document.querySelectorAll('input[data-filter='+_proposalKey+']:checked')).map(function(el){
                return el.value;
            });
            
        });

        $.ajax({
            url: '/proposal/proposal_filter/',
            data: _proposalObj,
            dataType: 'json',
            beforeSend:function(){
                $('.ajaxLoader').show();
            },
            success: function (json) {
                console.log(json)
                $('.ajaxLoader').hide();
                document.getElementById("proposalTotal").innerHTML = json.totalcount;
                $('#proposalSuccessFilter').html(json.proposals);
            },
            error: function (error) {
                console.log(error)
            }
        });
    });
});