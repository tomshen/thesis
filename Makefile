PROPPR:=./lib/ProPPR

all: compile pre.solutions.txt train

setup:
	tar xvf data.tar.gz
	./process.py
	git submodule init
	git submodule update
	cd lib/junto && bin/build update compile
	cd lib/ProPPR && ant clean build

compile:
	python ${PROPPR}/src/scripts/compiler.py serialize 20NG.ppr > 20NG.wam

train:
	java -cp '${PROPPR}/conf:${PROPPR}/bin:${PROPPR}/lib/*' \
	edu.cmu.ml.proppr.Grounder \
	--programFiles 20NG.wam:20NG.graph:20NG_seed_10perc.cfacts \
	--queries 20NG_train.data --grounded 20NG.grounded
	java -cp '${PROPPR}/conf:${PROPPR}/bin:${PROPPR}/lib/*' \
	edu.cmu.ml.proppr.Trainer --train 20NG.grounded --params 20NG.wts

pre.solutions.txt:
	java -cp '${PROPPR}/conf:${PROPPR}/bin:${PROPPR}/lib/*' \
	edu.cmu.ml.proppr.QueryAnswerer \
	--programFiles 20NG.wam:20NG.graph:20NG_seed_10perc.cfacts \
	--queries 20NG_test.data \
	--solutions pre.solutions.txt

post.solutions.txt:
	java -cp '${PROPPR}/conf:${PROPPR}/bin:${PROPPR}/lib/*' \
	edu.cmu.ml.proppr.QueryAnswerer \
	--programFiles 20NG.wam:20NG.graph:20NG_seed_10perc.cfacts \
	--queries 20NG_test.data --params 20NG.wts \
	--solutions post.solutions.txt

pre.evaluate:
	python ${PROPPR}/scripts/answermetrics.py --data 20NG_test.data \
	--answers pre.solutions.txt --metric mrr --metric recall

post.evaluate:
	python ${PROPPR}/scripts/answermetrics.py --data 20NG_test.data \
	--answers post.solutions.txt --metric mrr --metric recall
