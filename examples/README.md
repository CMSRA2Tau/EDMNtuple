BSM3GAna Example Code
=====================

The EDMNtuple format is both simple and powerful, improving on the speed of bare
TTrees while adding the shared expertise of a number of centrally-managed tools
for processing these files.

The subdirectories have a few standalone toy examples for processing these
EDMNtuples using a few different frameworks. Two options need a CMSSW checkout:

* PyFWLite - Python bindings to the FWLite framework
* FWLite - C++ version of the FWLite framework

Two others can work with a standalone ROOT checkout:

* BareROOT - Simple C++ script linked directly to ROOT
* TNTAnalyzer - Existing TNTAnalyzer code modified to also read EDMNtuples
