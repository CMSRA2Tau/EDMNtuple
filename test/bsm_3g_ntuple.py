import copy

# bsm_3g_ntuple.py - Generates EDNTuples (hopefully) compatible with all bsm3g
#       analyses.
# 
# How does this work? In order, we would like to do the following things
#
# 1) Use the PATMuonSelector (jet, tau, etc..) EDFilter to cut on objects
# 2) Run ID modules to add additional values to objects
# 3) Use CandViewNtpProducer to extract and write floats to output
#
# Unfortunately, the PAT<type>Selector's cut routines aren't completely fully-
# featured, so we run our own <type>UserData EDProducers to perform more
# detailed cuts and add variables that don't exist by default in miniAOD in
# a way CandViewNtpProducer can get at them. The flow is then:
# 1) Use the PATMuonSelector (jet, tau, etc..) EDFilter to cut on objects
# 2) Run ID modules to add additional values to objects
# 3) Run our <type>UserData modules for detailed cutting and for new user floats
# 4) Use CandViewNtpProducer to extract and write floats to output
#
# Ideally, things that end up in #3 are added to the upstream miniAOD production
# eventually

import os.path
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as opts

options = opts.VarParsing ('analysis')

options.register('maxEvts',
                 100,# default value: process all events
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.int,
                 'Number of events to process')

# Run locally if needed, remotely otherwise
if os.path.exists('ntuple_test_miniaod_skim.root'):
    inputDefault = 'file:ntuple_test_miniaod_skim.root'
else:
    inputDefault = '/store/mc/Phys14DR/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/MINIAODSIM/PU30bx50_PHYS14_25_V1-v1/00000/003B6371-8D81-E411-8467-003048F0E826.root'

options.register('sample',
                 inputDefault,
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 'Sample to analyze')

options.register('outputLabel',
                 'bsm_3g_ntuple.root',
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 'Output label')

options.register('globalTag',
                 'PHYS14_25_V2',
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 'Global Tag')

options.register('isData',
                 False,
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.bool,
                 'Is data?')

options.register('LHE',
                 True,
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.bool,
                 'Keep LHEProducts')

options.parseArguments()

if(options.isData):options.LHE = False

#
# "Hardcoded" configuration values, could be promoted to "command line"
#   configuration values
#
elLabel = 'slimmedElectrons'
muLabel = 'slimmedMuons'
photonLabel = 'slimmedPhotons'
jLabel = 'slimmedJets'
jLabelAK8 = 'slimmedJetsAK8'
pvLabel = 'offlineSlimmedPrimaryVertices'
metLabel = 'slimmedMETs'
tauLabel = 'slimmedTaus'
triggerLabel = 'TriggerResults'
prescaleLabel = 'patTrigger'
objects = 'selectedPatTrigger'
electronVetoIdMapLabel   = ("egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V1-miniAOD-standalone-veto")
electronLooseIdMapLabel  = ("egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V1-miniAOD-standalone-loose")
electronMediumIdMapLabel = ("egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V1-miniAOD-standalone-medium")
electronTightIdMapLabel  = ("egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V1-miniAOD-standalone-tight")
# muon cuts
muonPtMin              = 10.0
muonEtaMax             = 2.4
muonVertexNdofMin        = 4
muonVertexRhoMax         = 2
muonVertexZMax  = 24.0

# electron cuts
electronPtMin       = 10.0
electronEtaMax      = 2.4

# tau cuts
Tau_pt_min    = 20.0
Tau_eta_max   =  2.3

# jet cuts
jetPtMin    = 20.0

# primary vertex cuts
Pvtx_ndof_min   = 4.0
Pvtx_vtx_max  = 24.0
Pvtx_vtxdxy_max = 24.0

#
# Boilerplate includes
#
process = cms.Process("bsm3gEDNtuples")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.categories.append('HLTrigReport')
### Output Report
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
### Number of maximum events to process
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvts) )
### Source file
process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(
        options.sample
        )
)

process.load("PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff")
process.load("Configuration.EventContent.EventContent_cff")
process.load('Configuration.StandardSequences.Geometry_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.GlobalTag.globaltag = options.globalTag

#
# Step 1) Object cut definitions
#
process.skimmedPatMuons = cms.EDFilter(
    "PATMuonSelector",
    src = cms.InputTag(muLabel),
    cut = cms.string("pt > %f && isLooseMuon && abs(eta) < %f" % (muonPtMin, muonEtaMax))
    )

process.skimmedPatElectrons = cms.EDFilter(
    "PATElectronSelector",
    src = cms.InputTag(elLabel),
    cut = cms.string("pt > %f && abs(eta) < %f" % (electronPtMin, electronEtaMax))
    )

process.skimmedPatMET = cms.EDFilter(
    "PATMETSelector",
    src = cms.InputTag(metLabel),
    cut = cms.string("")
    )

process.skimmedPatJets = cms.EDFilter(
    "PATJetSelector",
    src = cms.InputTag(jLabel),
    cut = cms.string("pt > %f" % jetPtMin)
    )

process.skimmedPatTaus = cms.EDFilter(
    "PATTauSelector",
    src = cms.InputTag(tauLabel),
    cut = cms.string(" pt > 25 && abs(eta) < 4.")
    )

process.skimmedPatPhotons = cms.EDFilter(
    "PATPhotonSelector",
    src = cms.InputTag(photonLabel),
    cut = cms.string("")
    )

#
# Step 2) Run external modules to further enhance incoming AOD objects
#

#
# Electron ID
#
#from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
#process.load("RecoEgamma.ElectronIdentification.egmGsfElectronIDs_cfi")
#process.egmGsfElectronIDs.physicsObjectSrc = cms.InputTag('slimmedElectrons')
#from PhysicsTools.SelectorUtils.centralIDRegistry import central_id_registry
#process.egmGsfElectronIDSequence = cms.Sequence(process.egmGsfElectronIDs)
## Define which IDs we want to produce
## Each of these two example IDs contains all four standard
## cut-based ID working points (only two WP of the PU20bx25 are actually used here).
#my_id_modules = ['RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_PHYS14_PU20bx25_V1_miniAOD_cff']
##Add them to the VID producer
#for idmod in my_id_modules:
#    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)



#
# Step 3) Add User Data
#
process.muonUserData = cms.EDProducer(
    'MuonUserData',
    muonLabel = cms.InputTag("skimmedPatMuons"),
    vertexLabel = cms.InputTag("offlineSlimmedPrimaryVertices"),
    vertexNdofMin = cms.int32(muonVertexNdofMin),
    vertexRhoMax = cms.int32(muonVertexRhoMax),
    vertexZMax  = cms.double(muonVertexZMax)
)
process.electronUserData = cms.EDProducer(
    'ElectronUserData',
    electronLabel = cms.InputTag("skimmedPatElectrons"),
    vertexLabel = cms.InputTag("offlineSlimmedPrimaryVertices"),
    electronVetoIdMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V1-miniAOD-standalone-veto"),
    electronLooseIdMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V1-miniAOD-standalone-loose"),
    electronMediumIdMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V1-miniAOD-standalone-medium"),
    electronTightIdMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V1-miniAOD-standalone-tight"),
)
process.tauUserData = cms.EDProducer(
    'TauUserData',
    tauLabel = cms.InputTag("skimmedPatTaus"),
    vertexLabel = cms.InputTag("offlineSlimmedPrimaryVertices"),
)
process.jetUserData = cms.EDProducer(
    'JetUserData',
    jetLabel = cms.InputTag("skimmedPatJets"),
    vertexLabel = cms.InputTag("offlineSlimmedPrimaryVertices"),
)
process.photonUserData = cms.EDProducer(
    'PhotonUserData',
    photonLabel = cms.InputTag("skimmedPatPhotons"),
    vertexLabel = cms.InputTag("offlineSlimmedPrimaryVertices"),
)
process.pileupData = cms.EDProducer(
    'PUDumper',
    puLabel = cms.InputTag("addPileupInfo"),
    vertexLabel = cms.InputTag("offlineSlimmedPrimaryVertices"),
    vertexNdofMin = cms.double(4),
    vertexZMax = cms.double(24),
    vertexDxDyMax = cms.double(24)
)
process.genParticleUserData = cms.EDProducer(
    'GenParticleUserData',
    genParticleLabel = cms.InputTag("prunedGenParticles"),
    vertexLabel = cms.InputTag("offlineSlimmedPrimaryVertices"),
)

#
# Step 4) Configure the output file content (different file since it's so long)
#
process.load("BSM3GAna.EDNtuple.EventContent_cfi")

#
# Output File Configuration
#
# unscheduled mode is for champions
process.options = cms.untracked.PSet( allowUnscheduled = cms.untracked.bool(True) )
process.edmNtuplesOut = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string(options.outputLabel),
    outputCommands = cms.untracked.vstring(
    "drop *",
    "keep *_muons_*_*",
    "keep *_electrons_*_*",
    "keep *_photons_*_*",
    "keep *_jets_*_*",
    "keep *_taus_*_*",
    "keep *_met_*_*",
    "keep *_vertices_*_*",
    "keep *_pileupData_*_*",
    "keep *_genParticles_*_*",
    ),
    dropMetaData = cms.untracked.string('ALL'),
    )
process.endPath = cms.EndPath(process.edmNtuplesOut)
