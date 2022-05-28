
$(document).ready(function(){
  
    $('#select-option, #budget-amount').keyup(function(){
        var select_option_value = $('#select-option').val();
        var budget_value = $('#budget-amount').val();
        var total_salary = select_option_value * budget_value
        
        
        $('#total-salary').val(total_salary);
        
    });
    
    
});


    // var select_option_value = $('#select-option').val();