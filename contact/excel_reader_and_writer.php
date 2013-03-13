<?php
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
    $res = "<thead><tr>"
    foreach($excel_title as $n => $t){
        $res = $res . "<td>$t</td>";
    }
    $res = $res . "</tr></thead>";
    return $res;
}

function excel_body_tbody_format($excel_data) //return string
{
    //TODO
}


?>