<?php

require_once('util.php');
$db_host = 'localhost';
$db_user = 'root';
$db_password = '';
$db_name = 'ljstest';

$conn = mysql_connect($db_host, $db_user, $db_password);

if (! $conn){
    die("数据库无法链接，联系管理员。错误代号： " . mysql_error());
}

mysql_select_db($db_name, $conn) or die('数据表无法链接');
mysql_query('set names utf8');

$fields_array = array(); //for caching
$contact_array = array(); //for caching

function query_contacts()
{
    $result = mysql_query("select * from contacts");
    if ($result)
        return $result;
    else
        die('在数据库中无法得到联系人信息，请联系管理员');
    
}

function query_fields()
{
    $result = mysql_query("select * from fields");
    if ($result)
        return $result;
    else
        die('在数据库中无法得到标题栏信息，请联系管理员');
}

function sql_to_array($result)
{
    if ($result){
        $arr = array();
        while($field = mysql_fetch_row($result)){
            $arr[] = $field;
        }
        return $arr;       
    } else {
        return array();
    }
}
function get_fields_array()
{
    //TODO: cache
    $fields = query_fields();
    $arr = array();
    while ($field = mysql_fetch_row($fields)){
        $arr[$field[1]] = $field[2];
    }
    return $arr;
}

function get_contacts_array()
{
    $contacts = query_contacts();
    return sql_to_array($contacts);
}

function insert_list_into_contacts($contact_info)
{
    $checking = check_line($contact_info);
    if ($checking[0] == false){
        return $checking;
    }
    $fields = array_keys(get_fields_array());
    $q = "insert into contacts(`" . join("`,`", $fields) . "`) values ('";
    for ($i = 0; $i < count($fields) - 1; $i += 1){
        $q = $q . $contact_info[$i] . "','";
    }
    $q = $q . $contact_info[$i] . "')";
    $result = mysql_query($q);
    if ($result)
        return array(true, "");
    else
        return array(false, get_alert_error('行：' . join(",", $contact_info) . '插入数据库错误：' . mysql_errno() . ' ' . mysql_error()));
}

function update_contacts($contact_info)
{
    $checking = check_line($contact_info);
    if ($checking[0] == false){
        return $checking;
    }

    $fields = array_keys(get_fields_array());
    $q = "update contacts set ";
    $attribs = array();
    for($i = 0; $i < count($fields); $i += 1){
        $attribs[$i] = "$fields[$i]='".$contact_info[$i] . "'";
    }
    $q = $q . join(",", $attribs);
    $q = $q . "where $fields[0]='$contact_info[0]'";
    $result = mysql_query($q);
    if ($result)
        return array(true, "");
    else
        return array(false, get_alert_error('行：' . join(",", $contact_info) . '插入数据库错误：' . mysql_errno() . ' ' . mysql_error()));
}



function contacts_to_tbody($add_id)
{
    $res = '<tbody>';
    $contacts = get_contacts_array();
    for ($i = 0; $i < count($contacts); $i += 1){
        $res .= array_to_tr($contacts[$i]);
    }
    $res .= '</tbody>';
    return $res;
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

?>
