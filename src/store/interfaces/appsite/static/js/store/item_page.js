function decrementValue()
{
    var value = parseInt(document.getElementById('quantity').value);
    if(value > 1){
    value = isNaN(value) ? 0 : value;
    value--;
    document.getElementById('quantity').value = value;
    }
}

function incrementValue()
{
    var value = parseInt(document.getElementById('quantity').value);
    if(value < 10){
    value = isNaN(value) ? 0 : value;
    value++;
    document.getElementById('quantity').value = value;
    }
}

function addedCart() {
  if (document.getElementById("added") != null) {
    setTimeout(function() {
      document.getElementById('added').style.visibility = 'visible';
    }, 500);
    setTimeout(function(){
      document.getElementById('added').style.visibility = 'hidden';
    }, 2000);
  }
}

// For posting review

// If logged in
function openDiv(){
  document.getElementById('rev-wrap-div').style.display = 'block';
  document.getElementById('change-div').style.opacity = '0.5';
}

function closeDiv(){
  document.getElementById('rev-wrap-div').style.display = 'none';
  document.getElementById('change-div').style.opacity = '1';
}

// If not logged in

function openLogDiv(){
  document.getElementById('log-wrap-div').style.display = 'block';
  document.getElementById('change-div').style.opacity = '0.5';
}

function closeLogDiv(){
  document.getElementById('log-wrap-div').style.display = 'none';
  document.getElementById('change-div').style.opacity = '1';
}

/////////

var btn = $('.add');
btn.on('click', function(e){
  e.preventDefault();
    var quantity = parseInt(document.getElementById('quantity').value);
    var url = $('#form').attr('action');
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
      // Ajax Call
      $.ajax({
        type: 'POST',
        url: url,
        headers: {"X-CSRFToken": csrftoken},
        data:  {"quantity":quantity},
        dataType: 'json',
        success: function(response){
        addedCart();
        quantity = document.getElementById('quantity').value;
        document.getElementById("q-add").innerText = quantity;
        document.getElementById('quantity').value  = 1;
      }
      });
    });

