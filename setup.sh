mkdir deps
cd deps
header='--header=User-Agent: Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'
wget "$header" https://www.intel.com/content/dam/develop/public/us/en/include/intrinsics-guide/data-latest.xml
wget https://www.uops.info/instructions.xml
