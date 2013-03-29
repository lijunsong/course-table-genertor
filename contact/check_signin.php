<?php
require_once('util.php');

session_start();

if (!isset($_SESSION['ibscontact']) || $_SESSION['ibscontact'] != true){
  $_SESSION['ibscontact'] = false;
  header( 'Location: ./signin.php' ) ;

}

?>