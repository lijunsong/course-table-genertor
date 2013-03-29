<?php

session_start();
unset($_SESSION['ibscontact']);
header( 'Location: ./signin.php' ) ;


?>