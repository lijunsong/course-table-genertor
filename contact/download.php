<?php
require_once('conn.php');
//这个文件用于生成模板文件，或者导出数据库时候下载 csv 文件

/* array 的格式为：
array[0][0] = 'title1';
array[0][1] = 'title2';
array[1][0] = 'field1';
array[1][1] = 'field2';
*/

function export_to_csv($inarray, $delimiter=";"){
      while (list ($key1, $val1) = each ($inarray)) {
        while (list ($key, $val) = each ($val1)) {
          if (is_numeric($val)){
        $sendback .= $val."$delimiter";
           }else{
            $sendback .= "\"". $val ."\"$delimiter";
          }//fi
        }//wend
        $sendback = substr($sendback, 0, -1); //chop last ,
        $sendback .= "\n";
      }//wend
    return ($sendback);
}// end function

// function send_file_to_client($file_name,$str) { 
//     header("Content-type:text/csv; charset=utf-8"); 
//     header('Cache-Control: no-store, no-cache'); 
//     header('Expires:0'); 
//     header('Pragma:public'); 
//     header('Content-Disposition:attachment;filename="'.$file_name.'"'); 
//     echo $str;
// }

function send_file_to_client($filename, $data){
    header("Content-type: text/csv");
    header("Content-Disposition: attachment; filename=$filename");
    echo $data;   
}; 


if (!isset($_GET['download'])){

} else if ($_GET['download'] == 'export_db'){
    $file_name = date('Ymd') . '.csv';

    //导出
    $fields = array();
    $fields[0] = array_values(get_fields_array());
    $contacts = get_contacts_array();
    $str = export_to_csv($fields);

    $str .= export_to_csv($contacts);
    //echo $str;

    ob_end_clean(); //在设置 header 之前都不能有输出操作，于是直接clean掉。
    send_file_to_client($file_name, iconv('utf-8', 'gb2312', $str));
//    exit();
} else if ($_GET['download'] == 'template'){
	$file_name = 'template.csv';

	$field_title = get_fields_array();
	$table_field_title = array_keys($field_title);
	$fields = array();
	$fields[0] = array_values($field_title); //表头
	$fields[1] = array(); //示例数据
	for ($i = 0; $i < count($fields[0]); $i += 1){
		if ($table_field_title[$i] == 'studentid'){
			$val = '全为数字，必填';
		} else if ($table_field_title[$i] == 'gender'){
			$val = '男或女，必填';
		} else if ($table_field_title[$i] == 'name') {
			$val = '姓名，必填';
		} else if ($table_field_title[$i] == 'mobile'){
			$val = '横线与数字的任意组合，可为空';
		} else {
			$val = '任意数据，可为空';
		}
		$fields[1][$i] = $val;
	}
	$str = export_to_csv($fields);
	send_file_to_client($file_name, iconv('utf-8', 'gb2312', $str));
}

?>
