for pict in *.png; do
	echo "converting $pict into ${pict/.png/-Mono.png}"
	magick $pict -colorspace Gray ${pict/.png/-Mono.png}
done
for pict in *.pdf; do
	echo "converting $pict into ${pict/.pdf/-Mono.pdf}"
	magick $pict -colorspace Gray ${pict/.pdf/-Mono.pdf}
done