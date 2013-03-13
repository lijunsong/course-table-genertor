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
        $res = $res . "<td>$t</td>";
    }
    $res = $res . "</tr></thead>";
    return $res;
}

/* 返回 Array 类型 每行是一个 array 里的元素*/
function get_excel_body($excel_data)
{
    $sheets = $excel_data->sheets[0];
    $cells = array_slice($sheets['cells'], 1);
    return $cells;
}

function insertupdate_excel_into_db($excel_data)
{
    $lines = get_excel_body($excel_data);
    $success_p = true;
    foreach($lines as $line_num => $line){
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

function excel_body_tbody_format($excel_data, $check_db=false) //return string
{
    $lines = get_excel_body($excel_data);
    $res = "<tbody>";
    foreach($lines as $line_num => $line){
        if ($check_db == true){ 
            //检查数据库里面的内容
            $maybe_contact = get_contact_by_id($line[1]);
            if ($maybe_contact != NULL){
                //数据库里面有记录
                $res = $res . '<tr class="warning">';
                foreach($maybe_contact as $c){
                    $res = $res . "<td>$c</td>";
                }
                $res = $res . '</tr>';
            }
        }
        $res = $res . '<tr class="success">';
        foreach($line as $n => $c){
            $res = $res . "<td>$c</td>";
        }
        $res = $res . "</tr>";
    }
    $res = $res . "</tbody>";
    return $res;
}

function excel_html5_format($file_name)
{
    $excel_data = get_data_from_excel($file_name);
    $res = '<table class="table table-hover">';
    $res = $res . excel_title_thead_format($excel_data);
    $res = $res . excel_body_tbody_format($excel_data, $check_db=true);
    $res = $res . '</table>';
    return $res;
}


?>