<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>TradingWheels - Signup</title>
  <!-- Axios API -->
  <script src="https://unpkg.com/axios/dist/axios.min.js"></script>

  <!-- Bootstrap CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous" />

  <!-- Bootstrap JS CDN -->
  <script defer src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>

  <!-- JQuery CDN -->
  <script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>

  <!-- file CSS -->
  <link rel="stylesheet" href="login.css" />
</head>

<body>
  <div class="signup-bar">
    <div class="scrolling">
      <div class="d-flex align-content-center fw-bold mb-3">
        <img src="images/logo.png" height="40px" width="66px" alt="" class="me-3" />
        <p class="logo-font">TradingWheels</p>
      </div>

      <div class="d-flex align-content-center">
        <p class="me-2 login-label subtext">User Sign Up</p>
        <hr width="10%" />
      </div>

      <h1 class="fw-bold mb-3">
        Paper Trading — <br />
        the place where trading<br />
        risk doesn't exist
      </h1>

      <hr class="mb-4" />

      <p class="login-label">First Name</p>
      <input type="text" id="first_name" />
      <p class="login-label">Last Name</p>
      <input type="text" id="last_name" />
      <p class="login-label">Email</p>
      <input type="text" id="email" />
      <p class="login-label">Password</p>
      <input type="password" id="password" />

      <div class="mb-2 mt-2">
        <button id="sign-up">Sign Up</button>
      </div>

      <p class="subtext">
        Already have an account? <a href="login.html">Login</a>
      </p>
    </div>
  </div>
  <iframe src="https://app.vectary.com/p/1A4CxAD3B8qVcn5OKNqYT8" frameborder="0" width="100%" height="100%"></iframe>
</body>

</html>

<script>
  $("#sign-up").click(function() {
    // alert("Handler for .click() called.");

    const url = "http://127.0.0.1:5002/signup";

    var first_name = $("#first_name").val();
    var last_name = $("#last_name").val();
    var email = $("#email").val();
    var password = $("#password").val();

    // console.log(first_name, last_name, email, password);
    axios
      .post(url, {
        first_name: first_name,
        last_name: last_name,
        email: email,
        password: password
      })
      .then((response) => {
        // process response.dataobject
        // console.log(typeof(response.data))
        var result = response.data.code;
        console.log(result);

        // if no error, redirect to homepage
        if (result == "201") {
          // $.ajax({
          //   type: 'POST',
          //   url: 'signup.php',
          //   data: {
          //     'email': email,
          //   },
          // });
          // <?php
          // require_once 'common.php';
          // $email = $_POST['email'];
          // $_SESSION['email'] = $email;
          // ?>

          // console.log (<?php $email ?>)
          $(".scrolling").append(
            "<p class='succeed-text'>Account successfully created. Redirecting you to the Homepage... </p>"
          );
          $(".scrolling").scrollTop($(".scrolling")[0].scrollHeight);

          setTimeout(function() {
            window.location.replace("stock_view.html");
          }, 5000);
        }
      })
      .catch((error) => {
        // process error object
        error_code = error.response.status;
        // console.log("error");
        // console.log(error_code);

        // if error
        if (error_code == "500") {
          console.log('error500')
        }

        // if user account already created error
        if (error_code == "400") {
          console.log('error400')
          $(".scrolling").append(
            "<p class='error-text'>Account already exists!</p>"
          );
          $(".scrolling").scrollTop($(".scrolling")[0].scrollHeight);
        }
      });
  });
</script>