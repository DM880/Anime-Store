var btn = $('.add');
btn.on('click', function(e){
  e.preventDefault();
    item_id = $(this).attr('data-id');
    console.log(item_id);
    var url = $('#form-item'+item_id).attr('action');
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
      // Ajax Call
      $.ajax({
        type: 'POST',
        url: url,
        headers: {"X-CSRFToken": csrftoken},
        dataType: 'json',
        success: function(response){
        }
      });
    });