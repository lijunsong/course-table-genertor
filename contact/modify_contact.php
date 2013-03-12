<?php
//print_r($_POST);
require('conn.php');

if (isset($_POST['update'])){
    //处理update
} else if (isset($_POST['add'])){
    //处理insert
    $fields = array_keys($_POST);
    $vals = array_values($_POST);
    
    $query = "insert into contacts(";
    $query = $query . join(",", array_slice($fields,0,-1));
    $query = $query . ") values ('";
    $query = $query . join("','", array_slice($vals, 0, -1)) . "')";
    echo $query;
    
    $result = mysql_query($query);
    echo $result;
    
    
}


    
?>