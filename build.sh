mkdir -p deps
cd deps

#if [ -f "data-latest.xml" ];
#then
#	echo ""
#else
#	header='--header=User-Agent: Mozilla/5.0'
#	wget "$header" https://www.intel.com/content/dam/develop/public/us/en/include/intrinsics-guide/data-latest.xml
#fi

if [ -f "instructions.xml" ]; 
then
	echo ""
else
	wget https://www.uops.info/instructions.xml
fi

curl -L 'https://www.intel.com/content/dam/develop/public/us/en/include/intrinsics-guide/perf2.js' > "perf2.js"
curl -L 'https://www.intel.com/content/dam/develop/public/us/en/include/intrinsics-guide/data-3-6-3.xml' > "data-latest.xml"
curl -L 'https://developer.arm.com/architectures/instruction-sets/intrinsics/data/intrinsics.json' > "intrinsics.json"
curl -L 'https://developer.arm.com/architectures/instruction-sets/intrinsics/data/operations.json' > "operations.json"
curl -L 'https://github.com/dzaima/rvv-intrinsic-doc/releases/download/v7/rvv_base.json' > "rvv_base.json"
curl -L 'https://github.com/dzaima/riscv-v-spec/releases/download/v1/v-spec.html' > "v-spec.html"


