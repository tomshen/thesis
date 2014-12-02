PROPPR:=./lib/ProPPR
NAME:=webkb

all: program train

setup:
	git submodule init
	git submodule update

	cd lib/junto
	bin/build update compile
	cd ../..

	cd lib/ProPPR
	ant clean build
	cd ../..

program:
	mkdir -p programs/${NAME}
	python src/convert.py data/${NAME}.config programs/${NAME}

compile:
	python ${PROPPR}/src/scripts/compiler.py serialize src/junto.ppr > src/junto.wam

train:
	java -cp '${PROPPR}/conf:${PROPPR}/bin:${PROPPR}/lib/*' \
	edu.cmu.ml.proppr.Trainer --train programs/${NAME}/${NAME}.grounded \
	--params programs/${NAME}/${NAME}.wts
