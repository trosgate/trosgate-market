
$(document).ready(function () {

  $('#id_action_choice').change(function () {
    let selector = $('#id_action_choice option:selected').val()

    if (selector == 'withdrawal') {
      $('#narration-type').show()
      $('#staff-type').hide()
      $('#position-type').hide()
    }
    else if (selector == 'transfer') {
      $('#narration-type').hide()
      $('#staff-type').show()
      $('#position-type').show()
    }
    else {
      $('#narration-type').show()
      $('#staff-type').show()
      $('#position-type').show()
    }
  });

});
