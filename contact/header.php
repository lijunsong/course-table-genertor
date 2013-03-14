<?php
//nav content
$navs = array("通讯录" => "/contact/index.php",
              "项目管理" => "/contact/field_manage.php");
require_once('sidebar.php');


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
    <meta charset="utf-8">
    <link href="css/bootstrap.min.css" rel="stylesheet" media="screen">
    <link href="css/extra.css" rel="stylesheet" media="screen">
  </head>
  <body>
    <div class="navbar navbar-fixed-top navbar-inverse">
    <div class="navbar-inner">
    <a class="brand" href="/contact">北外国商通讯录</a>
<?
    if (in_array($current_file, $index_subentries) || $current_file == "index"){
        echo get_navs('index', $navs, "nav");
    } else {
        echo get_navs('field_manage', $navs, "nav");
    }
?>
    </div>
    </div>
    
    <div class="container-fluid">
    <div class="row-fluid">
