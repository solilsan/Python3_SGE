<?php

// Use in the “Post-Receive URLs” section of your GitHub repo.

if ( $_POST['payload'] ) {
shell_exec( ‘cd /home/solil/Python3_SGE/ && git reset –hard HEAD && git pull’ );
}

?>hi