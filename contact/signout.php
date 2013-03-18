<?php

session_start();
unset($_SESSION['ibscontactadmin']);
header( 'Location: ./signin.php' ) ;


?>