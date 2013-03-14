<?php
$title="下载联系人信息";
require_once('conn.php');
require_once('util.php');
include_once('header.php');
require_once('sidebar.php');

function export_csv($file_name,$str) { 
    header("Content-type:text/csv; charset=utf-8"); 
    header('Cache-Control:must-revalidate,post-check=0,pre-check=0'); 
    header('Expires:0'); 
    header('Pragma:public'); 
    header("Content-Disposition:attachment;filename=".$file_name); 
    echo $str; 
}

if (isset($_POST['download'])){
    $file_name = date('Ymd') . '.csv';
    
    //导出
    $fields = array_values(get_fields_array());
    $contacts = get_contacts_array();
    $str = join(",", $fields) . "\n";
    for ($i = 0; $i < count($contacts); $i += 1){
        $str = $str . join(",", $contacts[$i]) . "\n";
    }
    echo $str;
    
    export_csv($file_name, $str);
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
          您可以将通讯录导出成为 xls 格式并下载。
        </div>  
        <button type="submit" class="btn btn-primary" name="download">下载</button>
      </fieldset>
    </form>
</div>
<? include('footer.php'); /*end*/?>
