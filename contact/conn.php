<?php

$db_host = 'localhost';
$db_user = 'root';
$db_password = '';
$db_name = 'ljstest';

$conn = mysql_connect($db_host, $db_user, $db_password);

if (! $conn){
    die("Couldn't connect: " . mysql_error());
}

mysql_select_db($db_name, $conn) or die('select db failed');
?>
