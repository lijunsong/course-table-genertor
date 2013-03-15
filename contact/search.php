<?php
$title="搜索联系人";
require_once('conn.php');
require_once('util.php');
include_once('header.php');
require_once('sidebar.php');

$extra_info = NULL;

if (isset($_GET['delete']) && isset($_GET['name'])){
    $id = $_GET['delete'];
    $name = $_GET['name'];
    if (trim($id) == "" || trim($name) == ""){
        $extra_info = get_alert_error("删除联系人 $name 时产生错误");
    } else {
        $result = mysql_query("delete from contacts where studentid='$id'");
        if ($result){
            $extra_info = get_alert_info("删除联系人 $name");
        } else {
            $extra_info = get_alert_error("删除联系人 $name 时产生错误");            
        }
    }
} else if (isset($_POST['search'])){
    $q = 'select * from contacts where ';
    $fields = array_keys(get_fields_array());
    $arr = array();
    for($i = 0; $i < count($fields); $i++){
        if ($_POST[$fields[$i]] != ""){
            $arr[] = $fields[$i] . ' like "%' . $_POST[$fields[$i]] . '%"';
        }
    }
    $q .= join(" and ", $arr);
    $result = mysql_query($q);
    if (!$result){
        die(get_alert_error('搜索联系人发生错误。' . mysql_errno() . ' ' . mysql_error()));
    } else {
        $search_array = sql_to_array($result);
        $fields = get_fields_array();
        echo '<div class="span2">';
        echo get_sidebar($current_file, $sidebar);
        echo '</div>';
        echo '<div class="span10">';
        echo '<table class="table table-bordered">';
        echo array_to_thead($fields, $add_id=true, $add_op=true);
        echo array_to_tbody($search_array, $add_id=true, $add_op=true);
        echo '</table>';
        echo '</div>';
        include('footer.php'); /*end*/
        exit();
    }
}

?>
<div class="span2">
<?echo get_sidebar($current_file, $sidebar)?>
</div>
<div class="span10">
<?
if ($extra_info != NULL){
    echo $extra_info;
}
?>

<form class="form-horizontal" method="post" name="search">
    <fieldset>
    <legend>搜索联系人信息</legend>
    <!--<div class="alert alert-block">
      <h4>注意！</h4>
      <ul>
    <li>
      </ul>
    </div>-->
    
<?php
    $fields = get_fields_array();
    foreach ($fields as $f=>$field_name){
        echo control_group("$f",  $field_name, "");
    }
?>
<div class="control-group">
    <div class="controls">
    <button type="submit" class="btn btn-primary" name="search" value="1">搜索</button>
    </div>
</div>
        </fieldset>
</form>
</div>
<? include('footer.php'); /*end*/?>