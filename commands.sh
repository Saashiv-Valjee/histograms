mkdir norm10000
cd norm10000
setupATLAS
asetup 21.6.96, AthGeneration
Gen_tf.py --ecmEnergy=13000. --maxEvents=10000 --firstEvent=1 --randomSeed=111 --outputEVNTFile=EVNT.root --jobConfig=../../100xxx/515502
asetup AthDerivation,21.2.132.0
Reco_tf.py --inputEVNTFile=EVNT.root --outputDAODFile=output.root --reductionConf TRUTH1
cd /eos/user/s/svaljee/svj-s-channel-signal-request/TruthAnalysisTests
rm -rf build
mkdir build
cd source
asetup AnalysisBase,21.2.156,here
cd ../build
cmake ../source
make
source x86*/setup.sh
cd ../run
TruthDerivationTester --input ../../condor/norm10000/DAOD_TRUTH1.output.root --output norm10000.root --nevents -1
cd ../../condor
rm -rf norm10000

mkdir min10000
cd min10000
setupATLAS
asetup 21.6.96, AthGeneration
Gen_tf.py --ecmEnergy=13000. --maxEvents=10000 --firstEvent=1 --randomSeed=111 --outputEVNTFile=EVNT.root --jobConfig=../../min_100xxx/515502
asetup AthDerivation,21.2.132.0
Reco_tf.py --inputEVNTFile=EVNT.root --outputDAODFile=output.root --reductionConf TRUTH1
cd ../../TruthAnalysisTests
rm -rf build
mkdir build
cd source
asetup AnalysisBase,21.2.156,here
cd ../build
cmake ../source
make
source x86*/setup.sh
cd ../run
TruthDerivationTester --input ../../condor/min10000/DAOD_TRUTH1.output.root --output min10000.root --nevents -1
cd ../../condor
rm -rf min10000

mkdir max10000
cd max10000
setupATLAS
asetup 21.6.96, AthGeneration
Gen_tf.py --ecmEnergy=13000. --maxEvents=10000 --firstEvent=1 --randomSeed=111 --outputEVNTFile=EVNT.root --jobConfig=../../max_100xxx/515502
asetup AthDerivation,21.2.132.0
Reco_tf.py --inputEVNTFile=EVNT.root --outputDAODFile=output.root --reductionConf TRUTH1
cd ../../TruthAnalysisTests
rm -rf build
mkdir build
cd source
asetup AnalysisBase,21.2.156,here
cd ../build
cmake ../source
make
source x86*/setup.sh
cd ../run
TruthDerivationTester --input DAOD_TRUTH3.37972286._000001.pool.root.1 --output idk.root --nevents -1
cd ../../condor
rm -rf max10000
