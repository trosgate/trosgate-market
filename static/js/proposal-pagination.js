
$(document).ready(function(){

    $('#next-step-3-of-5, #next-step-4-of-5,#next-step-5-of-5, #final-submit, #proposal-detail, #proposal-faq, #proposal-spec, #proposal-media').hide() 
    $('#proposal-details').click(function(){
      $('#proposal-detail, #next-step-3-of-5').slideToggle(200)
      $('#next-step-2-of-5').hide()
    });
    
    $('#next-step-4-of-5, #next-step-5-of-5, #final-submit, #proposal-faq, #proposal-spec, #proposal-media').hide() 
    $('#proposal-faqs').click(function(){
      $('#proposal-faq, #next-step-4-of-5').slideToggle(200)
      $('#next-step-3-of-5').hide()
    });
    
    $('#next-step-5-of-5, #proposal-spec, #proposal-media, #final-submit').hide()    
    $('#proposal-specifications').click(function(){
      $('#proposal-spec, #next-step-5-of-5').slideToggle(200)
      $('#next-step-4-of-5').hide()
    });

    $('#final-submit, #proposal-media').hide()    
    $('#proposal-medias').click(function(){
      $('#proposal-media, #final-submit').slideToggle(200)
      $('#next-step-5-of-5').hide()
    });   
  });
  
  // $('#id_title, #id_preview, #id_category, #id_skill').hide()
  // $('#id_description, #cke_id_description, #id_sample_link, #id_faq_one, #id_faq_one_description, #id_faq_two, #id_faq_two_description, #id_faq_three, #id_faq_three_description, #id_salary, #id_service_level, #id_duration, #id_revision, #id_thumbnail, #id_video, #id_file_type').hide() 
  // $('#id_title, #id_preview, #id_category, #id_skill, #id_description, #id_sample_link, #id_faq_one, #id_faq_one_description, #id_faq_two, #id_faq_two_description, #id_faq_three, #id_faq_three_description, #id_salary, #id_service_level, #id_duration, #id_revision, #id_thumbnail, #id_video, #id_file_type').hide() 
  // $('#cke_id_description, #id_sample_link, #id_faq_one, #id_faq_one_description, #id_faq_two, #id_faq_two_description, #id_faq_three, #id_faq_three_description, #id_salary, #id_service_level, #id_duration, #id_revision, #id_thumbnail, #id_video, #id_file_type').slideToggle(200)

















