// Main Img Zoom

$(".main-img-cont")
  // tile mouse actions
  .on("mouseover", function() {
    $(this)
      .children("#main-img")
      .css({ transform: "scale(" + $(this).attr("data-scale") + ")" })
      .addClass("zoom-cont");
  })
  .on("mouseout", function() {
    $(this)
      .children("#main-img")
      .css({ transform: "scale(1)" })
      .removeClass("zoom-cont")
      .removeClass("zoom-img");
  })
  .on("mousemove", function(e) {
    $(this)
      .children("#main-img")
      .css({
        "transform-origin":
          ((e.pageX - $(this).offset().left) / $(this).width()) * 100 +
          "% " +
          ((e.pageY - $(this).offset().top) / $(this).height()) * 100 +
          "%"
      })
      .addClass("zoom-img")
  });


// Images

function changeImg(img_id){
  var original = document.getElementById('main-img').src;
  var temp = document.getElementById('oth-img-'+img_id).src;
  document.getElementById('oth-img-'+img_id).src = original;
  document.getElementById('main-img').src = temp;
}


// Quantity Buttons

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

// Added To Cart Div

function addedCart() {
  if (document.getElementById("added") != null) {
    setTimeout(function() {
      document.getElementById('added').style.opacity = 1;
    },);
    setTimeout(function(){
      document.getElementById('added').style.opacity = 0;
    }, 1000);
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

