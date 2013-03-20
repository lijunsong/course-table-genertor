<?php

require_once('conn.php');
require_once('util.php');

// php 5.3 needs quote to identify the fields! Fuck! waste time!
function add_quote($line)
{
    if ($line[0] != '"')
        $new_line = '"';
    else 
        $new_line = '';
    $inquote = false;
    for ($i = 0; $i < strlen($line); $i++){
        if ($line[$i] == '"'){//碰到引号
            if ($inquote == false){ //如果不在引号内
                $inquote = true;
                $new_line .= '"';
                continue;
            } else { //在引号内
                if ($i + 1 < strlen($line) && $line[$i+1] == '"'){ //处理双引号
                    $new_line .= '""';
                    $i++;
                    continue;
                } else { //引号关闭
                    $inquote = false;
                    $new_line .= '"';
                }
            }
        } else if ($line[$i] == ','){ //碰到逗号
            if ($inquote == true){ //如果在引号内 
                $new_line .= ',';
            } else { //不在引号内的逗号
                if ($line[$i-1] != '"'){
                    $new_line .= '"';
                }
                $new_line .= ',';
                if ($i + 1 < strlen($line) && $line[$i+1] != '"'){
                    $new_line .= '"';
                }
            }
        } else {
            $new_line .= $line[$i];
        }
    }
    return $new_line;
}
function parse_csv($file_name, $delimiter=",")
{
    $table = array();
    $row = 0;
    if (($handle = fopen("$file_name","r")) != FALSE) {
        while ($line = fgets($f) != NULL){
            $linesize = strlen($row) + 1;
            $new_line add_quote($line);
            echo $new_line;
            $data = str_getcsv($new_line, $linesize, "$delimiter");
            if (trim($data[0]) == "" || trim($data[1]) == "" || trim($data[2] == "")){
                if ($row == 0){
                    die(get_alert_error('csv 标题栏未填完整，返回重填'));
                } else {
                    $row++;
                    continue;
                }
            }
            $table[$row] = correct_array_reading($data);
            $row++;
        }
        fclose($handle);
    }
    print_r($table);
    //return $table
}

//返回二维数组
function get_data_from_csv($file_name, $delimiter=",")
{
    $row = 0;
    $table = array();
    echo parse_csv($file_name, $delimiter);

    if (($handle = fopen("$file_name", "r")) !== FALSE) {
        $filesize = filesize($file_name);
        while (($data = fgetcsv($handle, $filesize+1, "$delimiter")) !== FALSE) {
            if (trim($data[0]) == "" || trim($data[1]) == "" || trim($data[2] == "")){
                if ($row == 0){
                    die(get_alert_error('csv 标题栏未填完整，返回重填'));
                } else {
                    $row++;
                    continue;
                }
            }
            $table[$row] = correct_array_reading($data);
            $row++;
            /* $num = count($data); */
            /* echo "<p> $num fields in line $row: <br /></p>\n"; */
            /* $row++; */
            /* for ($c=0; $c < $num; $c++) { */
            /*     echo $data[$c] . "<br />\n"; */
            /* } */
        }
        fclose($handle);
    }
    //print_r($table);
    
    
    return $table;
}
// 读取 csv 的 title
function get_csv_title($table) //return array
{
    return $table[0];
}

/* 返回 Array 类型 每行是一个 array 里的元素*/
function get_csv_body($table, $preserve_order=true)
{
    //空行被省略，保持原来的 index
    $cells = array_slice($table, 1, count($table)+1, $preserve_order);
    return $cells;
}

function csv_title_thead_format($table, $add_id=true) //return string
{
    $csv_title = get_csv_title($table);
    return array_to_thead($csv_title, $add_id);
}



function are_the_same_contacts($c1, $c2)
{
    foreach($c1 as $k => $v){
        if ($c2[$k] != $v){
            return false;
        }
    }
    foreach($c2 as $k => $v){
        if ($c1[$k] != $v){
            return false;
        }
    }
    return true;
}


function insertupdate_csv_into_db($table)
{
    $lines = get_csv_body($table, $preserve_order=true);
    $success_p = true;
    $contacts = get_contacts_array();
    
    foreach($lines as $line_num => $line){
        //TODO: cache
        $maybe_contact = get_contact_by_id($line[0], $contacts);
        if ($maybe_contact != NULL){
            //数据库里有内容，需要update
            if (!are_the_same_contacts($maybe_contact, $line)){
                //如果内容不一致，更新
                $result_array = update_contacts($line);
                if (!$result_array[0]){
                    return $result_array;
                } else {
                    //echo "<p>更新联系人 $maybe_contact[0], $maybe_contact[1] 为 $line[0], $line[1]</p>";
                }
            } else {
                //echo "<p>联系人 （$maybe_contact[0], $maybe_contact[1]）信息无变化</p>";
            }
        } else {
            //直接添加
            $result_array = insert_list_into_contacts($line);
            if (!$result_array[0]){
                return $result_array;
            } else {
                //echo "<p>插入联系人信息：$line[0], $line[1]</p>";
            }
        }
    }
    return array(true, "");
}

function insertupdate_with_csv($file_name)
{
    $data = get_data_from_csv($file_name);
    $result = insertupdate_csv_into_db($data);
    return $result;
}

function overwrite_with_csv($file_name)
{
    $data = get_data_from_csv($file_name);
    $data = get_csv_body($data);
    $result = mysql_query('truncate table contacts');
    if ($result){
        foreach($data as $line_num => $line){
            $result_array = insert_list_into_contacts($line);
            if ($result_array[0] == false){
                return $result_array;
            }
        }
    } else {
        return array(false, get_alert_error('数据库错误 ' . mysql_errno() . ' ' . mysql_error()));
    }
    return array(true, "");
}

        
    

function csv_body_tbody_format($table, $check_db=false) 
/* 将 csv 的内容部分转化为 html5 中的tbody，如果 $check_db 为 true，
   将返回 array(body, conflict?) 的一个数组
*/
{
    $lines = get_csv_body($table, $preverse_order=false);
    $res = "<tbody>";
    $conflict = false;
    if ($check_db == true){
        $contacts = get_contacts_array();
    }
    
    foreach($lines as $line_num => $line){
        //当前行
        $contactid = $line[0];
        $line_num += 1;
        if ($check_db == false){
            
            $res .= array_to_tr(array_values(array('special_key' => $line_num) + $line),
                                $td_tag="td", $tr_style="class=\"success\"");
        //db 中的一行
        } else { 
            //检查数据库里面的内容
            $maybe_contact = get_contact_by_id($contactid, $contacts);
            if ($maybe_contact != NULL){
                //数据库里面有记录，记录不符合则显示红色
                if (!are_the_same_contacts($maybe_contact, $line)){
                    $conflict = true;
                    $res .= array_to_tr(array_values(array('special_key' => '<i class="icon-plus"></i>') + $line),
                                        $td_tag="td", $tr_style="class=\"success\"");
                    $res .= array_to_tr(array_values(array('special_key' => '<i class="icon-minus"></i>') + $maybe_contact),
                                        $td_tag="td", $tr_style='class="error"');
                } else{
                    $res .= array_to_tr(array_values(array('special_key' => $line_num) + $line),
                                        $td_tag="td");
                }
            } else {
                    $res .= array_to_tr(array_values(array('special_key' => '<i class="icon-plus"></i>') + $line),
                                        $td_tag="td", $tr_style="class=\"success\"");
            }
        }
    }
    $res = $res . "</tbody>";
    if ($check_db == true)
        $res = array($res, $conflict);
    return $res;
}

function check_title_against_dbfields($table)
{
    $csv_title = get_csv_title($table);
    //print_r($csv_title);
    $fields = array_values(get_fields_array());
    if (count($csv_title) != count($fields)){
        return array(false, get_alert_error("<p>Csv 中标题栏个数不正确</p>
                             <p>项目应该为：\"" . join('","', $fields) . '"。共 ' . count($fields) . " 个</p><p>
                             csv中则是：\"" . join('","', $csv_title) . '"。共 ' . count($csv_title) . '个</p>'));
    }
    for ($i = 0; $i < count($csv_title); $i += 1){
        if ($fields[$i] != $csv_title[$i]){
            return array(false, get_alert_error("<p>Csv标题栏中的'
                                                " . $csv_title[$i] . "
                                                '应该为'".$fields[$i]."'</p>"));
        }
    }
    return array(true,"");
}

function check_body_against_rules($table)
{
    $csv_body = get_csv_body($table, $preserve_order=true);
    
    foreach($csv_body as $line_num => $line){
        $check = check_line($line);
        if ($check[0] == false)
            return $check;
    }
    return array(true, "");
    
}

function check_csv($file_name)
{
    $table = get_data_from_csv($file_name);
    $check_title = check_title_against_dbfields($table);
    if ($check_title[0] == false){
        return $check_title;
    }
    $check_body = check_body_against_rules($table);
    return $check_body;
}

// 在使用这个函数之前，使用 check_csv 检查 csv 有没有问题
function csv_html5_format($file_name, $check_db=true)
{
    $table = get_data_from_csv($file_name);
    $res = '<table class="table table-bordered">';
    $res = $res . csv_title_thead_format($table);
    $tbody = csv_body_tbody_format($table, $check_db);
    if ( $check_db == true){
        $res = $res . $tbody[0];
        $res = $res . '</table>';
        return array($res, $tbody[1]);
    } else {
        $res = $res . $tbody;
        return $res . '</table>';
    }
}


?>
