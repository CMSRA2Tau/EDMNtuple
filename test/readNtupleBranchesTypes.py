##############################################################
# Author: Andres Florez, Universidad de los Andes, Colombia. #
# Author: Denis Rathjens, University of Hamburg, Germany     #
##############################################################

from optparse import OptionParser

#Parser for command line arguments
parser = OptionParser()
parser.add_option("--inFile", dest="inFile", default="OutTree.root", help="filepath for input ntuple file, default=%default")
parser.add_option("--AnaName",dest="AnaName",default="BSM3G_TNT_Analyzer", help="name of the automatically generated analyzer, default=%default")
parser.add_option("--dir", dest="dir", default="TNT", help="ntuple path to the tree, default=%default")
parser.add_option("--tree", dest="tree", default="BOOM", help="ntuple tree name, default=%default")
(options, args) = parser.parse_args()

print "Input file: " + options.inFile

print "producing list of ntuple branches"

import os, sys

#os.system("python getBrancheslist.py --inFile "+options.inFile+" --dir "+options.dir+" --tree "+options.tree)
from ROOT import gROOT, TF1, TFile, TTree
import sys

gROOT.Reset()
f1 = TFile(options.inFile)
f1.cd(options.dir)
if options.dir:
    tree = f1.Get(options.dir+"/"+options.tree)
else:
    tree = f1.Get(options.tree)
print "Got the tree %s" % tree

tree.MakeCode(options.inFile.rstrip(".root")+".C")

log_h = open(options.AnaName+".h", "w")

print >> log_h, "////////////////////////////////////////////////////////////////////"
print >> log_h, "// Developer: Andres Florez, Universidad de los Andes, Colombia. //"
print >> log_h, "// Developer: Denis Rathjens, University of Hamburg, Germany     //"
print >> log_h, "//////////////////////////////////////////////////////////////////"
print >> log_h, ""
print >> log_h, ""
print >> log_h, "#ifndef "+options.AnaName+"_h" 
print >> log_h, "#define "+options.AnaName+"_h"
print >> log_h, ""
print >> log_h, "#include <iostream>"
print >> log_h, "#include <fstream>"
print >> log_h, "#include <iomanip>"
print >> log_h, "#include <string>"
print >> log_h, "#include <math.h>"
print >> log_h, "#include <stdio.h>"
print >> log_h, "#include <stdlib.h>"
print >> log_h, "#include <vector>"
print >> log_h, ""
print >> log_h, "#include <TROOT.h>"
print >> log_h, "#include <TFile.h>"
print >> log_h, "#include <TBranch.h>"
print >> log_h, "#include <TApplication.h>"
print >> log_h, "#include <TTree.h>"
print >> log_h, ""
print >> log_h, "using namespace std;"
print >> log_h, ""
print >> log_h, "class "+options.AnaName+" {"
print >> log_h, "public :"
print >> log_h, "   "+options.AnaName+"();"
print >> log_h, "   ~"+options.AnaName+"();"
print >> log_h, ""
print >> log_h, "   void setBranchAddress(TTree* "+options.tree+");"

ReadLeaves=0

with open(options.inFile.rstrip(".root")+".C") as f:
    for line in f:	
    	if ReadLeaves==1:
		if line.find("// Set branch addresses.")!=-1:
			print >> log_h, "};"
			print >> log_h, "#endif"
			break
                # Strip EDNtuple naming scheme
                line = line.rstrip("\n")
                if line.endswith("present;"):
                    continue;
                line = line.rstrip("_obj;");
                
		print >> log_h, "%s;" % line
        if line.find("//Declaration of leaves types")!=-1:
		ReadLeaves=1
    
print "writing "+options.AnaName+".cc"

log_cc = open(options.AnaName+".cc", "w")

print >> log_cc, "#include \""+options.AnaName+".h\""
print >> log_cc, ""
print >> log_cc, "int main (int argc, char *argv[])"
print >> log_cc, "{"
print >> log_cc, ""
print >> log_cc, "  TApplication app(\"App\",&argc, argv);"
print >> log_cc, "  gROOT->ProcessLine(\"#include <vector>\");"
print >> log_cc, "  "+options.AnaName+" "+options.AnaName+";"
print >> log_cc, ""
print >> log_cc, "}"
print >> log_cc, ""+options.AnaName+"::"+options.AnaName+"()"
print >> log_cc, "{"
print >> log_cc, ""
print >> log_cc, "  TFile *f = new TFile (\"OutTree.root\");"
print >> log_cc, "  f->cd(\"TNT\");"
print >> log_cc, "  TTree* "+options.tree+" = (TTree*)f->Get(\""+options.dir+"/"+options.tree+"\");"
print >> log_cc, ""
print >> log_cc, "  int nentries = (int) "+options.tree+"->GetEntries();"
print >> log_cc, "  setBranchAddress("+options.tree+");"
print >> log_cc, ""  
print >> log_cc, "  for (int i = 0; i < nentries; ++i)"  
print >> log_cc, "    {"
print >> log_cc, "       "+options.tree+"->GetEntry(i);"
print >> log_cc, "       for (int j = 0; j < Muon_pt.size(); j++)"
print >> log_cc, "         {"
print >> log_cc, "            cout <<Muon_pt.at(j)<<endl;"
print >> log_cc, "         }"
print >> log_cc, "     }"
print >> log_cc, ""
print >> log_cc, "}"
print >> log_cc, ""
print >> log_cc, ""+options.AnaName+"::~"+options.AnaName+"()"
print >> log_cc, "{"
print >> log_cc, ""
print >> log_cc, "  // do anything here that needs to be done at desctruction time"
print >> log_cc, ""
print >> log_cc, "}"
print >> log_cc, ""
print >> log_cc, "void "+options.AnaName+"::setBranchAddress(TTree* "+options.tree+")"
print >> log_cc, "{"
print >> log_cc, ""

ReadBranches=0

with open(options.inFile.rstrip(".root")+".C") as f:
	for line in f:	
    		if ReadBranches==1:
			if line.find("//     This is the loop skeleton")!=-1:
				print >> log_cc, "};"
				break
			print >> log_cc, line.rstrip("\n")				
    		if line.find("// Set branch addresses.")!=-1:
			ReadBranches=1
		
os.system("rm "+options.inFile.rstrip(".root")+".C")		
		
print "All done! Run: \"make "+options.AnaName+" to compile the analyzer skeleton"		

