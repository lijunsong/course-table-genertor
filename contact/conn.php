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
mysql_query('set names utf8');

$fields_array = array(); //for caching
$contact_array = array(); //for caching

function query_contacts()
{
    return mysql_query("select * from contacts");
}

function query_fields()
{
    return mysql_query("select * from fields");
}

function get_fields_array()
{
    //TODO: cache
    $fields = query_fields();
    $arr = array();
    while($field = mysql_fetch_row($fields)){
        $arr[$field[1]] = $field[2];
    }
    return $arr;
}

function insert_list_into_contacts($contact_info)
{
    $fields = array_keys(get_fields_array());
    $q = "insert into contacts(" . join(",", $fields) . ") values ('";
    for ($i = 0; $i < count($fields) - 1; $i += 1){
        $q = $q . $contact_info[$i+1] . "','";
    }
    $q = $q . $contact_info[$i+1] . "')";
    return array(mysql_query($q), $q);
}

function update_contacts($contact_info)
{
    $fields = array_keys(get_fields_array());
    $q = "update contacts set ";
    $attribs = array();
    for($i = 0; $i < count($fields); $i += 1){
        $attribs[$i] = "$fields[$i]='".$contact_info[$i+1] . "'";
    }
    $q = $q . join(",", $attribs);
    $q = $q . "where $fields[0]='$contact_info[1]'";
    return array(mysql_query($q), $q);         
}

function fields_to_thead()
{
    $fields = query_fields();
    echo "<thead><tr>";
    while ($field = mysql_fetch_row($fields)){
        echo "<th>$field[2]</th>";
    }
    echo "</tr></thead>";
}

function contacts_to_tbody()
{
    $contacts = query_contacts();
    echo "<tbody>";
    while ($contact = mysql_fetch_row($contacts)){
        echo "<tr>";
        foreach ($contact as $info){
            echo "<td>$info</td>";
        }
        echo "</tr>";
    }
    echo "</tbody>";
}

function get_contacts_array()
{
    $arr = array();
    $contacts = query_contacts();
    while ($contact = mysql_fetch_row($contacts)){
        $arr[] = $contact;
    }
    return $arr;
}

//更新 fields。
//NOTE: 数组中为空的项不需要更新
function update_fields($new_fields)
{
    foreach($new_fields as $field => $field_name){
        if ($field_name != ""){
            $q = "update `fields`
                  set field_name = '$field_name'
                  where field='$field'";
            mysql_query($q);
        }
    }
}

/*
  $new_fields 是 array: array('field_n'=>'field_name')

 */
function add_fields($new_fields)
{
    foreach($new_fields as $field => $field_name){
        if ($field_name != ""){
            //在 fields 中增加一项
            $q = "insert into `fields`(field, field_name) values
                 ('$field', '$field_name')";
            //同时需要在 contacts 数据表中加入一个bolumn
            $q1 = "alter table `contacts` add $field varchar(32)";
            mysql_query($q);
            mysql_query($q1);
        }
    }
}

/* 在数据库中查找学号为 id 的记录 */

function get_contact_by_id($id)
{
    if ($result = mysql_query("select * from contacts where studentid=\"$id\"")){
        return mysql_fetch_row($result);
    } else {
        return NULL;
    }
}
?>
