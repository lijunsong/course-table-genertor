<?php

function control_group($input_id, $label_text, $placeholder)
{
    $groups = "
     <div class=\"control-group\">
     <label class=\"control-label\" for=\"$input_id\">$label_text</label>
     <div class=\"controls\"> 
     <input type=\"text\" name=\"$input_id\" id=\"$input_id\" placeholder=\"$placeholder\">
     </div></div>";
    return $groups;
}

function startsWith($haystack, $needle)
{
    return strpos($haystack, $needle) === 0;
}
function endsWith($haystack, $needle)
{
    return substr($haystack, -strlen($needle)) == $needle;
}

function wrap_text($text, $class="alert")
{
	return "<div class=\"$class\">$text</div>";
}

function get_alert($title, $text, $extra_class="")
{
    return wrap_text('<button type="button" class="close" data-dismiss="alert">&times;</button>
            <h4>' . $title . '</h4>' . "$text", "alert " . $extra_class);
}

function get_alert_info($text)
{
}

function get_alert_error($text)
{
    return get_alert("出错啦！", $text, "alert-error");
}

function get_navs($current_nav, $navs, $extra_nav_tag = "")
{
    $res = "<ul class=\"nav $extra_nav_tag\">";
    foreach ($navs as $name => $link){
        if (basename($link, ".php") == $current_nav)
            $res = $res . "<li class=\"active\">";
        else
            $res = $res . "<li>";
        $res = $res . "<a href=\"$link\">$name</a></li>";
    }
    $res = $res . "</ul>";
    return $res;
}

function array_to_tr($inarray, $td="td")
{
    $res = '<tr>';
    for($i = 0; $i < count($inarray); $i += 1){
        $res .= "<$td>".$inarray[$i]."</$td>";
    }
    $res .= '</tr>';
    return $res;   
}

function array_to_thead($inarray, $add_id=false, $add_op=false)
{
    $id = array();
    $op = array();
    if ($add_id == true){
        $id = array('specialkey_23x' => '序号');
    }
    if ($add_op == true){
        $op = array('specialkey_24z' => '操作');
    }
    $ths = array_values($id+ $inarray + $op);

    return '<thead>'.array_to_tr($ths, $td="th").'</thead>';
}

function array_to_tbody($inarrays, $add_id=false, $add_op=false)
{
    $id = array();
    $op = array();

    $res = '<tbody>';
    for($i = 0; $i < count($inarrays); $i += 1){
        if ($add_id == true){
            $id = array('specialkey_23x' => $i+1);
        }
        if ($add_op == true){
            $op = array('specialkey_24z' => 'button');
        }
        $new_line = array_values($id+$inarrays[$i]+$op);
        $res .= array_to_tr($new_line);
    }
    $res .= '</tbody>';
    return $res;
}

?>