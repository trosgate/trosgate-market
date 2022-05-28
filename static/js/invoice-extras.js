
$(document).ready(function(){

    $('#line_two, #id_line_two_quantity, #id_line_two_unit_price, #id_line_two_total_price, #line_three, #id_line_three_quantity, #id_line_three_unit_price, #id_line_three_total_price, #line_four, #id_line_four_quantity, #id_line_four_unit_price, #id_line_four_total_price, #line_five, #id_line_five_quantity, #id_line_five_unit_price, #id_line_five_total_price').hide()
    $('#proposal-extras').click(function(){
      $('#line_two, #id_line_two_quantity, #id_line_two_unit_price, #id_line_two_total_price').slideToggle(200)
      $('#line_three, #id_line_three_quantity, #id_line_three_unit_price, #id_line_three_total_price').slideToggle(200)
      $('#line_four, #id_line_four_quantity, #id_line_four_unit_price, #id_line_four_total_price').slideToggle(200)
      $('#line_five, #id_line_five_quantity, #id_line_five_unit_price, #id_line_five_total_price').slideToggle(200)
    });
   
   
});