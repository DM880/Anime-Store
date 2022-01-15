// Search Bar

function searchDiv(){
  if(document.getElementById('search_bar').style.visibility === 'visible'){
    document.getElementById('search_bar').style.visibility = 'hidden';
  }
  else{
    document.getElementById('search_bar').style.visibility = 'visible';
  }
};


// User Menu (Signed In User Only)

var timeout;

function showUserMenu () {
  clearTimeout(timeout)
  document.getElementById('user-div').style.opacity = 1.0;
  document.getElementById('user-div').style.display = 'block';
  timeout = setTimeout(function(){document.getElementById('user-div').style.opacity = 0.0;}, 1000);
}

function keepMenu () {
  clearTimeout(timeout)
}

function hideUserMenu () {
  clearTimeout(timeout)
  document.getElementById('user-div').style.opacity = 0.0;
  timeout = setTimeout(function(){document.getElementById('user-div').style.display = 'none';}, 1000);
}

var hover_user = document.getElementById('user-menu');
hover_user.onmouseover = showUserMenu;

user_div =  document.getElementById('user-div');

user_div.onmouseover = keepMenu;
user_div.onmouseleave = hideUserMenu;


// Open Phone nav menu

function navMenu(){
  if(document.getElementById('p-menu').style.visibility == "visible"){
    document.getElementById('p-menu').style.visibility = "hidden";
  }
  else{
    document.getElementById('p-menu').style.visibility = "visible";
  }
}
