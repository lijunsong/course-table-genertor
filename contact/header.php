<?php
//nav content
function get_navs($current_nav, $nav_tag = "nav-tabs")
{
    $navs = array("MainView" => "/contact/index.php",
                  "Upload"   => "/contact/upload.php",
                  "Search"   => "/contact/search.php",
                  "Field Manage" => "/contact/field_manage.php");
    
    echo "<ul class=\"nav $nav_tag\">";
    foreach ($navs as $name => $link){
        if (basename($link, ".php") == $current_nav)
            echo "<li class=\"active\">";
        else
            echo "<li>";
        echo "<a href=\"$link\">$name</a></li>";
    }
    echo "</ul>";
}

if (! isset($title)){
    $title = "北外国商通讯录";
}

$current_file = basename($_SERVER['PHP_SELF'], ".php");

?>
<!DOCTYPE html>
<html lang="zh">
  <head>
    <title><?echo $title?></title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta http-equiv="Content-Language" content="zh-cn" />
    <link href="css/bootstrap.min.css" rel="stylesheet" media="screen">
  </head>
  <body>
    <div class="container">
    <div class="navigationbar">
<? get_navs($current_file, "nav-pills"); ?>
    </div>
