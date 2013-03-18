<?php
require_once('util.php');

session_start();

if (!isset($_SESSION['ibscontactadmin']) || $_SESSION['ibscontactadmin'] != true){
  $_SESSION['ibscontactadmin'] = false;
  header( 'Location: ./signin.php' ) ;

}

?>