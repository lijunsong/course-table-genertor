<?php
require_once('check_signin.php');
require_once('util.php');

//nav content
error_reporting(E_ALL ^ E_NOTICE);

$navs = array("通讯录" => $current_dir."/index.php",
              "项目管理" => $current_dir."/field_manage.php",
              "用户管理" => $current_dir."/user_manage.php");

require_once('sidebar.php');

if (! isset($title)){
    $title = "北外国商通讯录";
}

$current_file = basename($_SERVER['PHP_SELF'], ".php");
$current_dir = dirname($_SERVER['PHP_SELF']); // may be duplicated,
                                              // but let it go

?>
<!DOCTYPE html>
<html lang="zh">
  <head>
    <title><?php echo $title;?></title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta charset="utf-8">
    <!--<link href="css/bootstrap.min.css" rel="stylesheet" media="screen">-->
    <link href="css/bootstrap.css" rel="stylesheet" media="screen">
    <link href="css/extra.css" rel="stylesheet" media="screen">
  </head>
  <body>
    <div class="navbar navbar-fixed-top navbar-inverse">
    <div class="navbar-inner">
        <div class="container">
        <a class="brand" href=<?php echo "\"$current_dir\"" ?>>北外国商通讯录</a>
        <div class="nav-collapse collapse">
            <p class="navbar-text pull-right"><a href="signout.php">登出</a></p>


<?php

    if (in_array($current_file, $index_subentries) || $current_file == "index"){
        echo get_navs('index', $navs, "nav");
    } else {
        echo get_navs('field_manage', $navs, "nav");
    }
?>
        </div>
        </div>
    </div>
    </div>
    
    <div class="container-fluid">
    <div class="row-fluid">