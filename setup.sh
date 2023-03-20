if [ -d "deps" ];
then
	echo ""
else
	mkdir deps
fi


cd deps

if [ -f "data-latest.xml" ]; 
then
	echo ""
else
	header='--header=User-Agent: Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'
	wget "$header" https://www.intel.com/content/dam/develop/public/us/en/include/intrinsics-guide/data-latest.xml
fi

if [ -f "instructions.xml" ]; 
then
	echo ""
else
	wget https://www.uops.info/instructions.xml
fi
