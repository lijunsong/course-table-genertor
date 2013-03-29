<?php
$title="用户管理";
include_once('header.php');
require_once('conn.php');
require_once('util.php');

$sql = "select username, password, salt, changablename from users";

$userinfo = array();
$users = array();
if (($result = mysql_query($sql)) != NULL){
    while ($info = mysql_fetch_row($result)){
        $users[] = $info[0];
        $userinfo[$info[0]] = array($info[1], $info[2], $info[3]);
    }
} else {
    echo get_alert_error('数据库链接错误');
}


//print_r($_POST);
$msg = NULL;

if (isset($_POST['username'])){
    $username = trim($_POST['username']);
    $newname = trim($_POST['newname']);
    $oldpass = trim($_POST['originpassword']);
    $pass1 = trim($_POST['password']);
    $pass2 = trim($_POST['retypepassword']);

    if ($newname == ''){
        $msg = get_alert_error('用户名为空');
    }else if ($newname != $username && in_array($newname, $users)){
        $msg = get_alert_error($newname.'已经存在！');
    } else if ( $pass1 != $pass2 ){
        $msg = get_alert_error('密码输入不一致，请重新输入');
    } else if ($pass1 == '' || $oldpass == ''){
        $msg = get_alert_error('密码不能为空');
    } else if ( !preg_match('/^[a-zA-Z0-9]+$/', $newname)){
        $msg = get_alert_error('用户名只能为字母，或数字，或其任意组合');
    } else{
        $stored_pass = $userinfo[$username][0];
        $salt = $userinfo[$username][1];
        if (get_pass($oldpass, $salt) != $stored_pass){
            $msg = get_alert_error('原始密码错误');
        } else {
            $sql = 'update users set';
            $sql .= '`username` = ' . "'$newname',";
            $sql .= "`password` = '" . get_pass($pass1, $salt);
            
            $sql .= "' where " . '`username` = ' . "'$username'";
            if ($result = mysql_query($sql)){
                $msg = get_alert_info('密码更新成功');
                
                $userinfo[$newname] = $userinfo[$username];
                unset($userinfo[$username]);
                
            } else {
                $msg = get_alert_error('更新错误，请到开发主页反馈该问题');
            }
            
        }
        
    }
}
?>

<div class="span2">
</div>
<div class="span8">
    <fieldset>
    <legend><?echo $title;?></legend>
<?php
//列出所有用户
foreach($userinfo as $user => $info){
    $changable = $info[2];
    if ($changable == false)
        continue;
    if ($msg){
        echo $msg;
    }
?>    
    <form class="form-horizontal" method="post" name="<?php echo $user;?>">
    <div class="control-group">
    <label class="control-label" for="newname">更改用户名</label>
    <div class="controls">
    <input type="text" name="newname" value="<?php echo $user; ?>" />
    </div>
    </div>

    <div class="control-group">
    <label class="control-label" for="originpassword">原始密码</label>
    <div class="controls">
    <input type="password" name="originpassword" placeholder="输入原始密码" />
    </div>
    </div>

    <div class="control-group">
    <label class="control-label" for="password">新密码</label>
    <div class="controls">
    <input type="password" name="password" placeholder="输入新密码" />
    </div>
    </div>

    <div class="control-group">
    <label class="control-label" for="retypepassword">确认新密码</label>
    <div class="controls">
    <input type="password" name="retypepassword" placeholder="再次输入新密码" />
    </div>
    </div>
    
        <div class="control-group">
        <div class="controls">
        <button type="submit" class="btn btn-primary" name="username" value="<? echo $user?>">更新密码</button>
        </div>
        </div>
        
        </form>
<?php        
}
    
?>    
      </fieldset>
</div>
<div class="span2">
</div>

<?php include('footer.php'); /*end*/?>