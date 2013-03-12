if (!isset($_POST['submit'])) {
    exit('非法访问！');

}

$username = htmlspecialchars($_POST['username']);
$password = MD5($_POST['password']);

include('conn.php');

$usercheck_query = mysql_query("select uid from user where username = '$username' and password = '$password'");

if ($result = mysql_fetch_array($usercheck_query)) {
    $_SESSION['username'] = $username;
    $_SESSION['userid'] = $result['uid'];
}

