var check_password = function() {

  password1 = document.getElementById('password1');
  password2 = document.getElementById('password2');
  button = document.getElementById('submit-btn');
  message = document.getElementById('message');

  if ((password1.value == password2.value) && password1.value.length > 7) {
    button.type = "submit";
    password1.style.color = 'green';
    password2.style.color = 'green';
    message.innerHTML = 'Password matching';
    message.style.color = 'green';
  }
  else if(password1.value.length > 7) {
    button.type = "button";
    password1.style.color = 'red';
    password2.style.color = 'red';
    message.innerHTML = 'Password not matching';
    message.style.color = 'red';
  }
  else{
    button.type = "button";
    password1.style.color = 'red';
    password2.style.color = 'red';
    message.innerHTML = 'Password must be at least 8 characters';
    message.style.color = 'red';
  }
}