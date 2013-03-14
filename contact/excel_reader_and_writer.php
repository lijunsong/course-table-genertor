<?php

require_once('conn.php');
require_once('util.php');

// maybe also http://code.google.com/p/php-excel/wiki/QuickUsageGuide
error_reporting(E_ALL ^ E_NOTICE);
/* A sheet sample
 Array
(
    [0] => Array
        (
            [maxrow] => 0
            [maxcol] => 0
            [numRows] => 2
            [numCols] => 10
            [cells] => Array
                (
                    [1] => Array
                        (
                            [1] => 学号
                            [2] => 姓名
                            [3] => 性别
                            [4] => 年级专业班级
                            [5] => 手机号
                            [6] => 邮箱
                            [7] => 所在地区
                            [8] => 工作单位
                            [9] => 兴趣
                            [10] => 备注1
                        )

                    [2] => Array
                        (
                            [1] => 21568941
                            [2] => 学生姓名1
                            [3] => 男
                            [4] => 99级129班
                            [5] => 125-87254
                            [6] => TT@gg.com
                            [7] => 北京
                            [8] => 一个非常非常非常非常非常非常非常非常非常长的工作单位
                            [9] => 篮球
                            [10] => 试试备注1
                        )

                )
...
*/
require_once('excel_reader2.php');

function get_data_from_excel($file_name)
{
    // no need the font and color, etc.
    $excel_data = new Spreadsheet_Excel_Reader($file_name, false);
    
    //$data->dump($row_numbers=false,$col_letters=false,$sheet=0,$table_class='table-hover');
    return $excel_data;
}
// 读取 excel 的 title
function get_excel_title($excel_data) //return array
{
    $sheets = $excel_data->sheets[0]; //取第一个工作表
    return $sheets['cells'][1];
}

function excel_title_thead_format($excel_data) //return string
{
    $excel_title = get_excel_title($excel_data);
    $res = "<thead><tr>";
    foreach($excel_title as $n => $t){
        $res = $res . "<th>$t</th>";
    }
    $res = $res . "</tr></thead>";
    return $res;
}

/* 返回 Array 类型 每行是一个 array 里的元素*/
function get_excel_body($excel_data, $preserve_order=true)
{
    $sheets = $excel_data->sheets[0];
    //空行被省略，保持原来的 index
    $cells = array_slice($sheets['cells'], 1, $excel_data->sheets[0]['numRows'], $preserve_order);
    return $cells;
}

function insertupdate_excel_into_db($excel_data)
{
    $lines = get_excel_body($excel_data);
    $success_p = true;
    foreach($lines as $line_num => $line){
        //TODO: cache
        $maybe_contact = get_contact_by_id($line[1]);
        if ($maybe_contact != NULL){
            //数据库里有内容，需要update
            $result_array = update_contacts($line);
            if (!$result_array[0]){
                $success_p = false;
                break;
            }

        } else {
            //直接添加
            $result_array = insert_list_into_contacts($line);
            if (!$result_array[0]){
                $success_p = false;
                break;
            }
        }
    }
    return $success_p;
}

function insertupdate_with_excel($file_name)
{
    $data = get_data_from_excel($file_name);
    $result = insertupdate_excel_into_db($data);
    return $result;
}

function excel_body_tbody_format($excel_data, $check_db=false) 
/* 将 excel 的内容部分转化为 html5 中的tbody，如果 $check_db 为 true，
   将返回 array(body, conflict?) 的一个数组
*/
{
    $lines = get_excel_body($excel_data, false);
    $res = "<tbody>";
    $conflict = false;
    foreach($lines as $line_num => $line){
        //当前行
        $res = $res . '<tr class="success">';
        for ($i = 1; $i <= $excel_data->sheets[0]['numCols']; $i += 1){
            $res = $res . "<td>$line[$i]</td>";
        }
        $res = $res . "</tr>";
        
        if ($check_db == true){ 
            //检查数据库里面的内容
            $maybe_contact = get_contact_by_id($line[1]);
            if ($maybe_contact != NULL){
                //数据库里面有记录
                $conflict = true;
                $res = $res . '<tr class="error">';
                foreach($maybe_contact as $c){
                    $res = $res . "<td>$c</td>";
                }
                $res = $res . '</tr>';
            }
        }
    }
    $res = $res . "</tbody>";
    if ($check_db == true)
        $res = array($res, $conflict);
    return $res;
}

function check_title_against_dbfields($excel_data)
{
    $excel_title = get_excel_title($excel_data);
    $fields = array_values(get_fields_array());
    if (count($excel_title) != count($fields)){
        return array(false, get_alert_error("<p>Excel 中标题栏个数不正确</p>
                             <p>项目应该为：" . join('，', $fields) . '。共 ' . count($fields) . " 个</p><p>
                             Excel中则是：" . join('，', $excel_title) . '。共 ' . count($excel_title) . '个</p>'));
    }
    reset($excel_title);
    for ($i = 0; $i < count($excel_title); $i += 1){
        if ($fields[$i] != current($excel_title)){
            return array(false, get_alert_error("<p>Excel标题栏中的'
                                                " . current($excel_title) . "
                                                '应该为'".$fields[$i]."'</p>"));
        }
        next($excel_title);
        
    }
    return array(true,"");
}

function check_body_against_rules($excel_data)
{
    $excel_body = get_excel_body($excel_data);
    foreach($excel_body as $line_num => $line){
        
        if (!preg_match("/^\d+$/", $line[1])){
            return array(false, get_alert_error("Excel 第 $line_num 行第 1 列必须全为数字：当前为 “$line[1]”"));
        }
        if (!preg_match("/^(男|女)$/", $line[3])){
            return array(false, get_alert_error("Excel 第 $line_num 行第 3 列必须为'男'或者'女'：当前为 “$line[3]”"));
        }
        if ($line[5] != "" && !preg_match("/(\d|-)*/", $line[5])){
            return array(false, get_alert_error("Excel 第 $line_num 行第 5 列必须为横线与数字的组合：当前为 “$line[5]”"));
        }
        /*if ($line[6] != "" && !filter_var($line[6], FILTER_VALIDATE_EMAIL)){
            return array(false, get_alert_error("Excel 第 $line_num 行第 6 列必须为合法的邮箱地址：当前为 “$line[6]”"));
            }*/
    }
    return array(true, "");
    
}

function check_excel($file_name)
{
    $excel_data = get_data_from_excel($file_name);
    //print_r($excel_data->sheets);
    $check_title = check_title_against_dbfields($excel_data);
    if ($check_title[0] == false){
        return $check_title;
    }
    $check_body = check_body_against_rules($excel_data);
    return $check_body;
}

// 在使用这个函数之前，使用 check_excel 检查 excel 有没有问题
function excel_html5_format($file_name, $check_db=true)
{
    $excel_data = get_data_from_excel($file_name);
    $res = '<table class="table table-bordered">';
    $res = $res . excel_title_thead_format($excel_data);
    $tbody = excel_body_tbody_format($excel_data, $check_db);
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