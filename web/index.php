<?php
// Retrieve YAML Settings
$yamlsettings = yaml_parse_file('/home/pi/redyellowgreen/settings.yaml');
$dbserver = $yamlsettings['Database']['ServerName'];
$dbuser = $yamlsettings['Database']['Username'];
$dbpass = $yamlsettings['Database']['Password'];
$dbname = $yamlsettings['Database']['DBName'];

// Load Settings
$dbconn = new mysqli($dbserver, $dbuser, $dbpass, $dbname);
if ($dbconn->connect_error) {
    die("Connection failed: " . $dbconn->connect_error);
}
$rssettings = mysqli_query($dbconn, "SELECT * FROM settings") or die("Error in Selecting " . mysqli_error($dbconn));
$rowsettings = mysqli_fetch_assoc($rssettings);
$displayname = $rowsettings["displayname"];
$lenscol = $rowsettings["lenscol"];
$hostname = gethostname(); // may output e.g,: sandie
?>
<html>
  <head>
    <title>RedYellowGreen</title>
    <meta http-equiv="refresh" content="5" />
  </head>
  <body>
    <font face="Arial">
    <H1><?php echo $hostname; ?></H1>
    <table cellspacing="0" cellpadding="0">
    	<tr height="130">
	    <td width="20">&nbsp;</td>
	    <td width="128" bgcolor="#<?php echo $lenscol; ?>">&nbsp;</td>
	    <td width="20">&nbsp;</td>
	</tr>
    	<tr>
	    <td width="20" bgcolor="gray">&nbsp;</td>
	    <td width="128" bgcolor="gray">&nbsp;</td>
	    <td width="20" bgcolor="gray">&nbsp;</td>
	</tr>
    	<tr>
	    <td width="20" bgcolor="gray">&nbsp;</td>
	    <td widht="128"><img src="oled.png?<?php echo time(); ?>"></td>
	    <td width="20" bgcolor="gray">&nbsp;</td>
	</tr>
    	<tr>
	    <td width="20" bgcolor="gray">&nbsp;</td>
	    <td width="128" bgcolor="gray">&nbsp;</td>
	    <td width="20" bgcolor="gray">&nbsp;</td>
	</tr>

	<tr>
            <td colspan="3" align="center"><?php echo $displayname; ?></td>
	</tr>
    </table>
  </body>
</html>
