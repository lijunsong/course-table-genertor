<?php
$title="下载联系人信息";
require_once('conn.php');
require_once('util.php');
include_once('header.php');
require_once('sidebar.php');

function export_csv($file_name,$str) { 
    header("Content-type:text/csv; charset=utf-8"); 
    header('Cache-Control: no-store, no-cache'); 
    header('Expires:0'); 
    header('Pragma:public'); 
    header('Content-Disposition:attachment;filename="'.$file_name.'"'); 
    echo $str;
}

function convert_str($a)
{
    return (string)$a;
}

if (isset($_POST['download'])){
    $file_name = date('Ymd') . '.csv';

    //导出
    $fields = array_values(get_fields_array());
    $contacts = get_contacts_array();
    //$fields = array_map("convert_str", $fields);
    $outstream = fopen("php://output", 'w');
    fputcsv($outstream, $fields, ',', '"');
    foreach( $contacts as $row){
        fputcsv($outstream, $row, ',', '"');
    }

    
    /* ob_end_clean(); */

    /* exit(); */
    
}

?>
<div class="span2">
<?echo get_sidebar($current_file, $sidebar)?>
</div>
<div class="span10">
    <form class="form" method="post">
      <fieldset>
        <legend><?echo $title?></legend>
        <div class="alert alert-info">
          <button type="button" class="close" data-dismiss="alert">&times;</button>
          您可以将通讯录导出成为 csv 格式并下载。
        </div>  
        <button type="submit" class="btn btn-primary" name="download">下载</button>
      </fieldset>
    </form>
</div>
<? include('footer.php'); /*end*/?>
