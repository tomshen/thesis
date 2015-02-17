PROPPR:=./lib/ProPPR
THREADS:=22
HEAPSIZE:=24g

all: compile pre.solutions.txt pre.evaluate

setup:
	tar xvf data.tar.gz
	./process.py
	git submodule init
	git submodule update
	cd lib/junto && bin/build update compile
	cd lib/ProPPR && ant clean build

compile:
	python ${PROPPR}/src/scripts/compiler.py serialize 20NG.ppr > 20NG.wam

ground:
	java -Xmx${HEAPSIZE} -cp '${PROPPR}/conf:${PROPPR}/bin:${PROPPR}/lib/*' \
	edu.cmu.ml.proppr.Grounder --apr eps=1e-6 \
	--programFiles 20NG.wam:small.graph:small_seed_10perc.cfacts \
	--queries small.data --grounded small.grounded

train:
	java -cp '${PROPPR}/conf:${PROPPR}/bin:${PROPPR}/lib/*' \
	edu.cmu.ml.proppr.Trainer --train programs/20NG.grounded \
	--params 20NG.wts

small:
	java -Xmx${HEAPSIZE} -cp '${PROPPR}/conf:${PROPPR}/bin:${PROPPR}/lib/*' \
	edu.cmu.ml.proppr.QueryAnswerer --apr eps=1e-6 --threads ${THREADS} \
	--programFiles 20NG.wam:small.graph:small_seed_10perc.cfacts \
	--queries small.data \
	--solutions small.solutions.txt

pre.solutions.txt:
	java -cp '${PROPPR}/conf:${PROPPR}/bin:${PROPPR}/lib/*' \
	edu.cmu.ml.proppr.QueryAnswerer --apr eps=1e-6 --threads ${THREADS} \
	--programFiles 20NG.wam:20NG.graph:20NG_seed_10perc.cfacts \
	--queries 20NG_test.data \
	--solutions pre.solutions.txt

post.solutions.txt:
	java -cp '${PROPPR}/conf:${PROPPR}/bin:${PROPPR}/lib/*' \
	edu.cmu.ml.proppr.QueryAnswerer --apr eps=1e-6 --threads ${THREADS} \
	--programFiles 20NG.wam:20NG.graph:20NG_seed_10perc.cfacts \
	--queries 20NG_test.data --params 20NG.wts \
	--solutions post.solutions.txt

pre.evaluate:
	python ${PROPPR}/scripts/answermetrics.py --data 20NG_test.data \
	--answers pre.solutions.txt --metric mrr --metric recall

post.evaluate:
	python ${PROPPR}/scripts/answermetrics.py --data 20NG_test.data \
	--answers post.solutions.txt --metric mrr --metric recall
