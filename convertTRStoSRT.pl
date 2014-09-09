# The goal is to convert trs file (transcriber) to standard srt file
# Developed by : Ali Reza Ebadat (arezae at -- gmail.com)

# trs files are in xml format which includes more information rather to srt files
# 
# srt file format
# 
# 					    Subtitle number
#    					Start time --> End time (hours:minutes:seconds,milliseconds)
#    					Text of subtitle (one or more lines)
#    					Blank line

sub convertToTime{
	$sec=shift;
	$msec=($sec*1000)%1000;
	$hours=($sec/(60*60))%24;
	if(length("$hours")==1){ $hours="0".$hours;}
	$mins=($sec/60)%60;
	if(length("$mins")==1){ $mins="0".$mins;}
	$secs=$sec%60;
	if(length("$secs")==1){ $secs="0".$secs;}
	if(length("$msec")==1){ $msec="00".$msec;}
	if(length("$msec")==2){ $msec="0".$msec;}
	return $hours.":".$mins.":".$secs.",$msec";
}
open(infile,"<$ARGV[0]") or die $!." $ARGV[0]\n";
open(outfile,">$ARGV[1]") or die $!." $ARGV[1]\n";

@lines = ();
while($line = <infile>){
	chomp($line);
	next if($line eq "");
	push(@lines,$line);	
}
close(infile);
print scalar(@lines)." lines read from $ARGV[0]\n";
$j=1;
for($i=0;$i<scalar(@lines);$i++){
	my $startTime="";
	my $endTime="";
	my $line = $lines[$i];
	#print $line."\n"; 
	if($line =~ /^<Turn.*/){
		$line =~ /.+startTime=\"([0-9]+\.[0-9]+)\".+/;
		$startTime=convertToTime($1);
		$line =~ /.+endTime=\"([0-9]+\.[0-9]+)\".+/;
		$endTime=convertToTime($1);
		 
		if($lines[$i+2] =~ "<\/Turn>") {
#			print outfile $j++."\n";
#			print outfile "$startTime --> $endTime\n";	
#			print outfile "<s>_<\/s>\n\n";
		}
		else{
			print outfile $j++."\n";
			print outfile "$startTime --> $endTime\n";		
			print outfile "\<s\>$lines[$i+2]\<\/s\>\n\n";
		}	
	}
}
close(infile);
close(outfile);

