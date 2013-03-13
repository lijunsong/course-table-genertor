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

?>


    