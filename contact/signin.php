<?php
require_once('util.php');
require_once('conn.php');
$errorinfo = NULL;

if (isset($_POST['username']) && isset($_POST['password'])){
  $username = trim($_POST['username']);
  $password = trim($_POST['password']);

  if ( $username != '' or $password != ''){
    $query = "select salt, password, available from users where username=\"$username\"";
    $result = mysql_query($query);

    if ($result) {
      $row = mysql_fetch_row($result);
      if ($row){
        $salt = $row[0];
        $hashed_password = $row[1];
        $available = $row[2];
        if ($hashed_password == md5($password . $salt) && $available == true) {
          session_start();
          $_SESSION["ibscontactadmin"] = true;
          header( 'Location: ./index.php' );
        }
      }      
    } else {echo mysql_error();}
  }
  $errorinfo = "用户名或者密码错误";
}

?>
<html lang="zh">
  <head>
    <title>北外商学院通讯录管理员登录</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta charset="utf-8">
    <link href="css/bootstrap.min.css" rel="stylesheet" media="screen">
    <link href="css/extra.css" rel="stylesheet" media="screen">
    <style>
      .form-signin {
          background-color: #FFFFFF;
          border: 1px solid #E5E5E5;
          border-radius: 5px 5px 5px 5px;
          box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
          margin: 0 auto 20px;
          max-width: 300px;
          padding: 19px 29px 29px;
      }
      .form-signin-heading{
        font-size:25px;
        text-align: center;
      }
      .form-signin input[type="text"], .form-signin input[type="password"]{
        font-size: 18px;
        height: auto;
        margin-bottom: 20px;
        padding: 10px;
      }
      body{
        background: #eeeeee;
      }
    </style>
    <script language="javascript" src="js/md5.js"></script>
    <script language="javascript">
      <!--
      function passResponse() {
        document.login.password.value = MD5(document.login.password.value);
        document.login.submit();
      }
      // -->
    </script>
  </head>
<body>
<div class="container">
  <form class="form-signin" method="post" name="login" action="signin.php">
    <h2 class="form-signin-heading">北外商学院通讯录<br />管理员登录</h2>
      <input class="input-block-level" id="username" name="username" type="text" placeholder="用户名" />
      <input class="input-block-level" id="password" name="password" type="password" placeholder="密码" />
      <?php
      if ($errorinfo != NULL){
        echo get_alert_error("$errorinfo");
      }
      ?>
      <input class="btn btn-primary btn-large" type="submit" name="submit" value="确定" onClick="passResponse(); return false;"/>
  </form>

</div>
<?php include('footer.php'); /*end*/?>
</body>
</html>


