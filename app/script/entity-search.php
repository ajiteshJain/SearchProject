<?php

$db_con;

function connect_database() {
	$servername = "127.0.0.1";
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

function shutdown()
{
	global $db_con;
	mysqli_close($db_con);
}

function setTfIdfWordWeights($searchTerms) {
	$streams = array("robotics","database","databases","artificial","intelligence","machine","learning","human","computer","interaction","research","analytics");
	$wordWeights = array();
	$termCount = count($searchTerms);
	for($i = 0; $i < $termCount; $i++) {
		if(in_array(strtolower($searchTerms[$i]), $streams)) {
			$wordWeights[$searchTerms[$i]] = 10;
		}
		else {
			$wordWeights[$searchTerms[$i]] = 1;	
		}

	}
	return $wordWeights;
}


function getDocuments($searchQuery) {
	connect_database();
	global $db_con;
	$entity_list = array("professor"=>"person","course"=>"course","professors"=>"person","courses"=>"course","news"=>"news");
	$weights = array("gpr"=>0.5 , "apr"=>0.5, "entity" => 1 , "tf-idf"=>1);
	$input_entity = "";
	$searchTerms = explode(" ",$searchQuery);
	$wordWeights = setTfIdfWordWeights($searchTerms);
	$documentCount = 6455;
	$subQuery = "(";
	$termCount = count($searchTerms);

	for($i = 0; $i < $termCount; $i++) {
		$subQuery .= "DocumentWordFrequency.word LIKE \"".$searchTerms[$i]."\"";
		if(array_key_exists(strtolower($searchTerms[$i]) , $entity_list)) {
			$weights["entity"] = 10;
			$input_entity = strtolower($entity_list[$searchTerms[$i]]);
		}
		if($i+1 < $termCount) {
			$subQuery .= " OR ";
		}
	}

	$subQuery .= ")";
	
	$sql = "SELECT pagedetails.*,DocumentWordFrequency.word,DocumentWordFrequency.frequency as tF ,WordDocumentFrequency.frequency as dF 
			FROM pagedetails,WordDocumentFrequency,DocumentWordFrequency 
			WHERE pagedetails.url = DocumentWordFrequency.url AND DocumentWordFrequency.word = WordDocumentFrequency.word
				AND ".$subQuery;
	
	$result = mysqli_query($db_con,$sql);
	
	$aprScores = array();
	$gprScores = array();
	$tfIdfScores = array(array());
	$documentEntities = array();
	$seen_urls = array();

	echo mysqli_num_rows($result)." results found";

	while($row = mysqli_fetch_array($result)) {
		$current_url = $row['url'];
		$tfIdfScore = $row['tF']/$row['dF'];//(1+log($row["tF"])) * log($documentCount / $row["dF"]);
		$word = $row['word'];
		if(array_key_exists($word, $wordWeights)) {
			$tfIdfScore *= $wordWeights[$word];
		}
		
		if(!in_array($current_url, $seen_urls)) {
			$gpr = $row["googlePageRank"]/10;
			$apr = $row["alexaPageRank"]/10000;
			$entity = $row["entity"];
			$gprScores[$current_url] = $weights['gpr']*$gpr;
			$aprScores[$current_url] = $weights['apr']*$gpr;
			$documentEntities[$current_url] = $entity;
			$tfIdfScores[$current_url] = $tfIdfScore;
			array_push($seen_urls, $current_url);
		}
		else {
			$tfIdfScores[$current_url] += $tfIdfScore;
		}
	}

	$urlScores = array();
	foreach ($seen_urls as $candidateUrl) {
		$score = ($weights['gpr']*$gprScores[$candidateUrl]) + ($weights['apr']*$aprScores[$candidateUrl]) + ($weights['tf-idf']*$tfIdfScores[$candidateUrl]);
		if(strlen($input_entity) > 0 && strcasecmp($documentEntities[$candidateUrl],$input_entity) == 0) {
			$score += $weights['entity'] * 10;
		}
		$urlScores[$candidateUrl] = $score;
	}

	arsort($urlScores);
	$rank = 1;
	foreach ($urlScores as $url=>$score) {
		echo "<br/><h3>Rank = $rank, URL = <a href='".$url."'>$url</a></h3>";//.$score;//. " tf-idf=".$tfIdfScores[$url];//. ", apr=".$aprScores[$url].", gpr=".$gprScores[$url]. " and entity = ".$documentEntities[$url];
		$rank++;
	}

	shutdown();
	return ;
}

if(!empty($_GET["q"])) {
	getDocuments($_GET["q"]);
}
else {
	echo '
		<script>
			function submitSearch() {
			    alert("Url = localhost"+"/search.php?q="+document.getElementById("searchBox").value);
			    setTimeout(function(){document.location.href = "page.html;"},500);
			    alert("Set complete!");

			}
		</script>
		<form onsubmit="submitSearch()">
			What would you like to search for today ? <input id="searchBox" type="text"/><input type="submit"/>	
		</form>
		';

}


?>