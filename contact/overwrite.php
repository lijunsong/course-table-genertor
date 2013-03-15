<?php
$title="更替联系人信息";
include_once('header.php');
require_once('conn.php');
require_once('csv_reader_and_writer.php');
require_once('util.php');

$new_file = "/tmp/test.csv";
?>

<div class="span2">
<?echo get_sidebar($current_file, $sidebar)?>
</div>

<div class="span10">

<?php    
if (!isset($_POST['file_upload']) && !isset($_POST['update_contact'])){
    //如果没有上传过东西，也没有需要更新联系人，那么显示上传按钮
?>

<form action="overwrite.php" method="post" enctype="multipart/form-data" class="form-horizontal">
    <fieldset>
    <legend>全部更替联系人信息</legend>
    <div class="alert alert-block">
      <h4>注意！</h4>
      <ul>
        <li><span style="color: red">导入的数据将会完全替换掉现有的所有数据。</span></li>
        <li>系统仅支持 <strong>csv</strong> 格式的文件导入，您可以在<a href="./download.php?download=template">这里</a>下载模板文件。</li>
        <li>系统将忽略“学号“，“姓名”或者“性别”为空的行</li>
      </ul>
    </div>
    <label for="file" >上传文件</label>
    <input type="file" name="file" id="file" />

    <button class="btn btn-danger" type="submit" name="file_upload">下一步</button>
    </fieldset>
</form>

<?php    
} else if (isset($_POST['file_upload'])){
    //如果上传了文件
    if ($_FILES["file"]["error"] > 0){
        echo "上传发生错误: " . $_FILES["file"]["error"] . "br />";
    } else {
        if ($_FILES["file"]["type"] != "text/csv"){
            die(get_alert_error('请上传 csv 文件'));
        }
        move_uploaded_file($_FILES["file"]["tmp_name"], $new_file);

        $check_result = check_csv($new_file);
        if ($check_result[0] == true){
            //csv 符合条件
            $result = csv_html5_format($new_file, $check_db = true);
                $button_style = "btn-danger";
                $alert_tag = "alert-block";
                $alert_title = "即将更替所有的联系人信息";
                $info = "您的“导入”操作即将覆盖数据库中的<strong>全部</strong>内容，请在下面确认信息无误，然后点击“导入”";
?>
            <? echo "<div class=\"alert $alert_tag\">"; ?> 
            <h4><? echo $alert_title; ?></h4>
            <? echo $info; ?>
            </div>
        
            
            <form class="form-inline" method="post" name="update_contact" action="overwrite.php">
            <button type="submit" class="btn <?echo $button_style;?>"  name="update_contact">更替</button>
            </form>
            <? echo $result[0]; ?>

<?php
        } else {
            //csv 不符合条件
            echo $check_result[1];
            
        }
    }
    
} else if (isset($_POST['update_contact'])){
    if (overwrite_with_csv($new_file)){
        //插入成功
        echo get_alert_info('更换数据完成');
    } else {
        //插入失败
        $errno = "" . mysql_errno();
        if ($errno == "1062"){
            echo get_alert_error('数据表中有重复的学生 ID：' . mysql_error());
        } else {
            echo get_alert_error('Mysql 错误：' . mysql_errno() . mysql_error());
        }
        
    }
}
?>
</div>
<? include('footer.php'); /*end*/?>
