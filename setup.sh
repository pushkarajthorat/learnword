for file in `cat today`
#for file in acerbity
do
    [ -d oxford-dict/"$file" ] && continue
	mkdir oxford-dict/"$file";
	#wget http://www.oxforddictionaries.com/definition/english/$file -O oxford-dict/$file/$file
	wget "http://www.oxforddictionaries.com/search/english/?direct=1&multi=1&q=$file" -O oxford-dict/$file/$file
	python FormatWordPage.py oxford-dict/"$file/$file" | tr '\n' ' ' | sed -e 's/<header class/\n<header class/g' -e 's/<\/header>/<\/header>\n/g' -e 's/<\/h2>/<\/h2>\n/g' -e 's/<h2/\n<h2/g'  | grep -v '</div>/</div></header>$' | grep -v '^<header class="entryHeader">' | tr '\n' ' ' | sed -e 's/<h2> Definition of <strong>/\n<h2> Definition of <strong>/g' -e 's/<\/ul>/<\/ul>\n/g'  | grep -v "^<h2> Definition of <strong>" > oxford-dict/"$file"/meaning
done;




