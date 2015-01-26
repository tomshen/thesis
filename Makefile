PROPPR:=./lib/ProPPR

all: compile run

setup:
	tar xvf data.tar.gz
	./process.py
	git submodule init
	git submodule update
	cd lib/junto && bin/build update compile
	cd lib/ProPPR && ant clean build

compile:
	python ${PROPPR}/src/scripts/compiler.py serialize 20NG.ppr > 20NG.wam

run:
	java -cp '${PROPPR}/conf:${PROPPR}/bin:${PROPPR}/lib/*' \
	edu.cmu.ml.proppr.QueryAnswerer \
	--programFiles 20NG.wam:20NG.graph:20NG_seed_10perc.cfacts \
	--queries 20NG_test.data \
	--solutions solutions.txt

evaluate:
	python ${PROPPR}/scripts/answermetrics.py --data 20NG_test.data \
	--answers solutions.txt --metric mrr --metric recall
