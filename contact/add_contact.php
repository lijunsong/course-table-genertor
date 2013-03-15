<?php
$title="添加联系人";
require_once('conn.php');
require_once('util.php');
include_once('header.php');
require_once('sidebar.php');

$extra_info = NULL;

if (isset($_POST['add_contact'])){
    //print_r($_POST);
    if (trim($_POST['studentid']) == "" ||
        trim($_POST['name']) == "" ||
        trim($_POST['gender']) == ""){
        $extra_info = get_alert_error('有必填项没有填写');
    } else {
        $fields = array_keys(get_fields_array());
        $contacts = get_contacts_array();
        $maybe_contact = get_contact_by_id($_POST['studentid'], $contacts);
        if ($maybe_contact == NULL){
            for($i = 0; $i < count($fields); $i++){
                $contacts[$i] = $_POST["$fields[$i]"];
            }
            $result = insert_list_into_contacts($contacts);
            if ($result[0]){
                $extra_info = get_alert_info('添加成功');
            } else {
                $extra_info = $result[1];
                
            }
        } else {
            $extra_info = get_alert_error('联系人已经存在');
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
    <legend>添加一个联系人信息</legend>
    <div class="alert alert-block">
      <h4>注意！</h4>
      <ul>
        <li>“学号“，“姓名”或者“性别”为必填项。</li>
      </ul>
    </div>
    
<?php
    $fields = get_fields_array();
    foreach ($fields as $f=>$field_name){
        $field_info = "";
        if ($f == 'studentid' || $f == 'gender' || $f == 'name'){
            $field_info = '必填';
        } 
        
        echo control_group("$f",  $field_name, "$field_info");
    }
?>
<div class="control-group">
    <div class="controls">
    <button type="submit" class="btn btn-primary" name="add_contact" value="1">添加</button>
    </div>
</div>
        </fieldset>
</form>
</div>
<? include('footer.php'); /*end*/?>