# EDMNtuple
Dumping ground for a quick EDMNtuple proposal

## Installation

From your source directory:
```
git cms-merge-topic ikrav:egm_id_phys14
git clone https://github.com/CMSRA2Tau/EDMNtuple.git BSM3GAna/EDMNtuple
cd ..
scram b -j 10
```

## Running

The CMSSW configuration lives at `EDMNtuple/test/bsm_3g_tuple.py`. It accepts
miniAOD and emits an EDMNtuple
