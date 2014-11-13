<?php
require_once __DIR__ . DIRECTORY_SEPARATOR . 'vendor' . DIRECTORY_SEPARATOR . 'autoload.php';

$db_con;
use \SEOstats\Services as SEOstats;

function connect_database() {
	$servername = "localhost";
	$username = "root";
	$password = "";

	// Create connection
	global $db_con ;
	$db_con = mysqli_connect($servername, $username, $password, "cs6422");

	// Check connection
	if (!$db_con) {
		die("Connection failed: " . mysqli_connect_error());
	}
	return true;
}


function get_page_rank($url) {
	try {
		$seostats = new \SEOstats\SEOstats;
		if ($seostats->setUrl($url)) {
			return array('alexa'=>SEOstats\Alexa::getGlobalRank(), 'google'=>SEOstats\Google::getPageRank());
		}
	}catch (SEOstatsException $e) {
		die($e->getMessage());
	}
}

function get_page_links($baseUrl, $dom) {
	$links = $dom->getElementsByTagName('a');
	$linkList = array();
	$siteBase = 'http://www.cc.gatech.edu';
	foreach ($links as $link){
		$link = $link->getAttribute('href');
		if(strlen($link) > 1){
			//convert relative to absolute URLs
			if($link[0] == '/') {
				$link = $siteBase.$link;
				
			}
			
			//add only urls inside the gatech network
			if(strpos($link,'gatech.edu') > 0) {
				array_push($linkList, $link);
			}
			echo "\nGot $link";
		}
	}
	return $linkList;
}

function store_page_outlinks($baseUrl,$dom) {
	global $db_con;
	$page_outlinks = array();
	$page_links = get_page_links($baseUrl,$dom);
	$values = "";
	$outlink_values = "";
	foreach ($page_links as $link) {
		$values .= "('$link', 0),";
		$outlink_values .= "('$link','$baseUrl'),";
	}
	if(strlen($values) > 1) {
		$sql = "INSERT INTO linkstatus(url,status) VALUES ".substr($values,0,-1)." ON DUPLICATE KEY UPDATE url=url";
		if (!mysqli_query($db_con, $sql)) {
			echo "Error: " . $sql . "<br>" . mysqli_error($db_con);
			return -1;
		}
		
		$sql2 = "INSERT INTO linkstructure(url,parentUrl) VALUES ".substr($outlink_values,0,-1)." ON DUPLICATE KEY UPDATE url=url";
		if (!mysqli_query($db_con, $sql2)) {
			echo "Error: <br>" . mysqli_error($db_con);
			return -1;
		}
		echo "\n<br/>Got ".count($page_links)." out-links from current page";
		return 1;
	}
	
	return -1;
}

function get_page_text($dom) {
	$page_text = "";
	$body = $dom->getElementsByTagName('body');
	if ( $body && 0<$body->length ) {
		$body = $body->item(0);
		$page_text .= " ".$body->nodeValue;
	}
	return $page_text;
}

function store_page_text($baseUrl , $dom) {
	global $db_con;
	$page_text = get_page_text($dom);
	$path = str_replace("http://","",$baseUrl);		//removing http:// from file path
	$path = str_replace("/","!",$path);				//removing / from file path
	$path = str_replace("?","!",$path);				//removing ? from file path
	$path = str_replace(":","!colon!",$path);				//removing : from file path
	$file_location = "data/$path";
	$myfile = fopen($file_location, "w+");
	$status = fwrite($myfile, $page_text);
	if(!$status) {
		echo "File writing failed! exiting! empty text = ".empty($page_text);
		insert_skipped_url($baseUrl,'empty-text');
		return ;
	}
	fclose($myfile);
	
	$page_rank = get_page_rank($baseUrl);
	$alexaRank = $page_rank['alexa'];
	$gRank = $page_rank['google'];
	$sql = "INSERT INTO pagedetails(url,alexaPageRank,googlePageRank,filePath) VALUES ('$baseUrl','$alexaRank','$gRank','$file_location') ON DUPLICATE KEY UPDATE url=url";
	
	if (!mysqli_query($db_con, $sql)) {
		echo "Error: " . $sql . "<br>" . mysqli_error($db_con);
		return -1;
	}
	$sql = "INSERT INTO linkstatus(url,status) VALUES ('$baseUrl',1) ON DUPLICATE KEY UPDATE status=1";
	if (mysqli_query($db_con, $sql)) {
		echo "\n<br/>Page details inserted successfully";
		return 1;
	} else {
		echo "Error: " . $sql . "<br>" . mysqli_error($db_con);
		return -1;
	}
}

function get_frequency_vector($text) {
	$wordFrequency = array_count_values(str_word_count($text, 1));
	arsort($wordFrequency);
	return $wordFrequency;
}


function get_pending_urls($url_count=3) {
	global $db_con;
	$result = mysqli_query($db_con,"SELECT url FROM linkstatus WHERE status=0 ORDER BY serialNum ASC LIMIT $url_count");
	$urls = array();
	while($row = mysqli_fetch_array($result)) {
		array_push($urls, $row['url']);
	}
	return $urls;
}

function insert_skipped_url($url, $reason) {
	global $db_con;
	$sql = "UPDATE linkstatus SET status = 1 WHERE url = '$url'";
	
	if (!mysqli_query($db_con, $sql)) {
		echo "Error: " . $sql . "<br>" . mysqli_error($db_con);
		return -1;
	}
	
	$sql = "INSERT INTO skippedurls(url,reason) VALUES ('$url','$reason') ON DUPLICATE KEY UPDATE url=url";
	if (!mysqli_query($db_con, $sql)) {
		echo "Error: " . $sql . "<br>" . mysqli_error($db_con);
		return -1;
	}
}

function shutdown()
{
	global $db_con;
	mysqli_close($db_con);
}

/*
	This function uses BFS to crawl the web from a given starting point i.e. base URL.
	A configurable crawl count is given to keep things under control in case things go wrong.
	
*/
function start_crawl($crawl_count=3) {
	
	connect_database();
	$i = 0;
	while($i<$crawl_count) {
		$crawl_list = get_pending_urls($crawl_count - $i);
		if(empty($crawl_list)) {
			echo "\nLooks like you're all done! Woohoo!";
			shutdown();
			return;
		}
		
		foreach ($crawl_list as $crawl_url) {
			if(!strpos($crawl_url,'cc.gatech.edu')) {
				insert_skipped_url($crawl_url, 'oon');
				$i++;
				continue;
			}
			//DIrty way to remove unfit URLs
			if($crawl_url[0] != 'h' || strpos($crawl_url, '@') || strpos($crawl_url, '#') || strpos($crawl_url, '?')
				|| strpos($crawl_url, '.pdf') || strpos($crawl_url, '.mov') || strpos($crawl_url, '.MOV') || strpos($crawl_url, '.avi') || strpos($crawl_url, '.AVI')
				|| strpos($crawl_url, '.ppt') || strpos($crawl_url, '.doc') || strpos($crawl_url, '.wav')
				|| strpos($crawl_url, '.m4v') || strpos($crawl_url, '.jpg') || strpos($crawl_url, '.gif') || strpos($crawl_url, '.ps') || strpos($crawl_url, '.ics')
				|| strpos($crawl_url, '.zip') || strpos($crawl_url, '.exe') 
				|| strpos($crawl_url, '/2014-') || strpos($crawl_url, '/2013-') || strpos($crawl_url, '/2012-') || strpos($crawl_url, '/2011-')
				|| strpos($crawl_url, '/2015-') || strpos($crawl_url, '/2016-') || strpos($crawl_url, '/2017-')) {
				echo "\nSkipping $crawl_url";
				insert_skipped_url($crawl_url, 'media/email');
				$i++;
				continue;
			}
			echo "\n\nTotal = $crawl_count , Current = $i , currently fetching $crawl_url";
			$html = file_get_contents($crawl_url);
			if($html === False || empty($html)) {
				echo "\nSkipping! Got 404 for $crawl_url";
				insert_skipped_url($crawl_url, '404');
				$i++;
				continue;
			}
			$dom = new DOMDocument;
			@$dom->loadHTML($html);
			store_page_text($crawl_url, $dom);
			store_page_outlinks($crawl_url,$dom);
			$i++;
		}
		
	}
	shutdown();
	return ;
}

$crawl_count=3;
if(!empty($argv[1]))$crawl_count = $argv[1];
start_crawl($crawl_count);

?>