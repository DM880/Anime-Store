// window.onscroll = function () {
//     if (document.documentElement.scrollTop > 10) {
//       document.getElementById('nav').style.borderBottom = '1px solid black';
//     } else {
//     	document.getElementById('nav').style.borderBottom = 'none';
//     }
// }

// Search Bar

function searchDiv(){
  if(document.getElementById('search_bar').style.visibility === 'visible'){ document.getElementById('search_bar').style.visibility = 'hidden';
  }
  else{
    document.getElementById('search_bar').style.visibility = 'visible';
  }
};


// User Menu (Signed In User Only)

var timeout;

function showMenu () {
  clearTimeout(timeout)
  document.getElementById('user-div').style.opacity = 1.0;
  document.getElementById('user-div').style.display = 'block';
  timeout = setTimeout(function(){document.getElementById('user-div').style.opacity = 0.0;}, 1000);
}

function keepMenu () {
  clearTimeout(timeout)
}

function hideMenu () {
  clearTimeout(timeout)
  document.getElementById('user-div').style.opacity = 0.0;
  timeout = setTimeout(function(){document.getElementById('user-div').style.display = 'none';}, 1000);
}

var hover = document.getElementById('user-menu')
hover.onmouseover = showMenu

user_div =  document.getElementById('user-div');

user_div.onmouseover = keepMenu;
user_div.onmouseleave = hideMenu;