<?php
$title="编辑联系人";
require_once('conn.php');
require_once('util.php');
include_once('header.php');
require_once('sidebar.php');

$extra_info = NULL;

if (isset($_GET['edit'])){
    $edit_id = $_GET['edit'];
    $edit_name = $_GET['name'];
    $contacts = get_contacts_array();
    $contact = get_contact_by_id($edit_id, $contacts);
    if ($contact == NULL){
        die(get_alert_error("编辑联系人 $edit_name 时产生错误：查无此人！"));
    } 
}
if (isset($_POST['edit_contact'])){
    //print_r($_POST);
    if (trim($_POST['studentid']) == "" ||
        trim($_POST['name']) == "" ||
        trim($_POST['gender']) == ""){
        $extra_info = get_alert_error('有必填项没有填写');
    } else {
        $result = update_contacts(array_values($_POST));
        if ($result[0]){
            $extra_info = get_alert_info('更新成功');
            $contact = array_values(array_slice($_POST, 0, -1));
            //print_r($contact);
        } else {
            $extra_info = $result[1];
        } 
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
    <legend>编辑联系人信息</legend>
    <div class="alert alert-block">
      <h4>注意！</h4>
      <ul>
        <li>“学号“，“姓名”或者“性别”为必填项。</li>
      </ul>
    </div>
    
<?php
    $fields = get_fields_array();
    $col = 0;
    foreach ($fields as $f=>$field_name){
        $field_info = htmlspecialchars($contact[$col]);
        $field_name = htmlspecialchars($field_name);
        echo control_group("$f",  $field_name, "$field_info", "$field_info");
        $col++;
    }
?>
<div class="control-group">
    <div class="controls">
    <button type="submit" class="btn btn-primary" name="edit_contact" value="1">编辑</button>
    </div>
</div>
        </fieldset>
</form>
</div>
<? include('footer.php'); /*end*/?>
