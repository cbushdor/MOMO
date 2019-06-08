<?php
$to = "dorey_s@laposte.net";
$subject = "My subject";
$txt = "Hello world!";
$headers = "From: webmaster@example.com" . "\r\n" .
"CC: sebastien.dorey@laposte.net";

mail($to,$subject,$txt,$headers);
?> 