<?php
$title="上传联系人信息";
include_once('header.php');
require_once('conn.php');
require_once('excel_reader_and_writer.php');
require_once('util.php');
?>

<div class="span2">
<?echo get_sidebar($current_file, $sidebar)?>
</div>

<div class="span10">

<?php    
if (!isset($_POST['file_upload']) && !isset($_POST['update_contact'])){
    //如果没有上传过东西，也没有需要更新联系人，那么显示上传按钮
?>

<form action="upload.php" method="post" enctype="multipart/form-data" class="form-horizontal">
    <fieldset>
    <legend>上传联系人信息</legend>
    <div class="alert alert-block">
      <h4>注意！</h4>
      <ul>
        <li>系统仅支持 <strong>xls</strong> 格式的文件导入，您可以在<a href="./template.xls">这里</a>下载模板文件。</li>
        <li>导入的数据将会覆盖掉现有的数据。</li>
        
      </ul>
    </div>
    <label for="file" >上传文件</label>
    <input type="file" name="file" id="file" />

    <button class="btn btn-primary" type="submit" name="file_upload">下一步</button>
    </fieldset>
</form>

<?php    
} else if (isset($_POST['file_upload'])){
    //如果上传了文件
    if ($_FILES["file"]["error"] > 0){
        echo "上传发生错误: " . $_FILES["file"]["error"] . "br />";
    } else {
?>
<?php        
        move_uploaded_file($_FILES["file"]["tmp_name"],
                           "/tmp/test.xsl");
        //echo "<br />type: " . $_FILES["file"]["type"];
        $check_result = check_excel("/tmp/test.xsl");
        if ($check_result[0] == true){
            //excel 符合条件
            $result = excel_html5_format("/tmp/test.xsl", $check_db = true);
            if ($result[1] == true){
                $button_style = "btn-danger";
                $alert_tag = "alert-block";
                $alert_title = "发现冲突！";
                $info = "您的“导入”操作即将覆盖数据库中的部分内容，请在下面确认信息无误，然后点击“导入”";
            } else {
                $button_style = "btn-primary";
                $alert_tag = "alert-info";
                $alert_title = "可以安全导入";
                $info = "点击“导入”完成本次批量上传";
            }
?>
            <? echo "<div class=\"alert $alert_tag\">"; ?> 
            <h4><? echo $alert_title; ?></h4>
            <? echo $info; ?>
            </div>
        
            
            <form class="form-inline" method="post" name="update_contact" action="upload.php">
            <button type="submit" class="btn <?echo $button_style;?>"  name="update_contact">导入</button>
            </form>
            <? echo $result[0]; ?>

<?php
        } else {
            //excel 不符合条件
            echo $check_result[1];
            
        }
    }
    
} else if (isset($_POST['update_contact'])){
    if (insertupdate_with_excel("/tmp/test.xsl")){
        //插入成功
        echo wrap_text('insert successfully!', 'alert alert-info');
    } else {
        //插入失败
        echo wrap_text('Failed!' . mysql_error(), 'alert alert-error');
    }
}
?>
</div>
<? include('footer.php'); /*end*/?>
