import FWCore.ParameterSet.Config as cms
import copy

#
# Tuple variables configuration - What will be saved
#    See: https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideEDMNtuples

# Define the variables all objects will want
basic = cms.EDProducer(
    "CandViewNtpProducer",
    src=cms.InputTag("skimmedPatMuons"),
    lazyParser=cms.untracked.bool(True),
    prefix=cms.untracked.string(""),
    # I'll only store the event info in the ntp producer below
    eventInfo=cms.untracked.bool(False),
    variables = cms.VPSet(
    cms.PSet(
    tag = cms.untracked.string("Mass"),
    quantity = cms.untracked.string("mass")
    ),
    cms.PSet(
    tag = cms.untracked.string("Pt"),
    quantity = cms.untracked.string("pt")
    ),
    cms.PSet(
    tag = cms.untracked.string("Eta"),
    quantity = cms.untracked.string("eta")
    ),
    cms.PSet(
    tag = cms.untracked.string("Y"),
    quantity = cms.untracked.string("rapidity")
    ),
    cms.PSet(
    tag = cms.untracked.string("Phi"),
    quantity = cms.untracked.string("phi")
    ),
    cms.PSet(
    tag = cms.untracked.string("E"),
    quantity = cms.untracked.string("energy")
    ),
    cms.PSet(
    tag = cms.untracked.string("Charge"),
    quantity = cms.untracked.string("charge")
    ),
    )
    )

# Define additional variables needed by specific objects
muonVars = (
    cms.PSet(
        tag = cms.untracked.string("IsPFMuon"),
        quantity = cms.untracked.string("isPFMuon")
    ),
    cms.PSet(
        tag = cms.untracked.string("IsLooseMuon"),
        quantity = cms.untracked.string("isLooseMuon")
    ),
    cms.PSet(
        tag = cms.untracked.string("IsSoftMuon"),
        quantity = cms.untracked.string("userFloat('isSoftMuon')")
    ),
    cms.PSet(
        tag = cms.untracked.string("IsTightMuon"),
        quantity = cms.untracked.string("userFloat('isTightMuon')")
    ),
    cms.PSet(
        tag = cms.untracked.string("GlobalChi2"),
        quantity = cms.untracked.string("? globalTrack.isNonnull ? globalTrack.hitPattern.numberOfValidTrackerHits : -999"),
    ),
    cms.PSet(
        tag = cms.untracked.string("GlobalValidHits"),
        quantity = cms.untracked.string("? globalTrack.isNonnull ? globalTrack.hitPattern.numberOfValidMuonHits : -999"),
    ),
    cms.PSet(
        tag = cms.untracked.string("NumberMatchedStations"),
        quantity = cms.untracked.string("numberOfMatchedStations"),
    ),
    cms.PSet(
        tag = cms.untracked.string("NumberValidPixelHits"),
        quantity = cms.untracked.string("? innerTrack.isNonnull ? innerTrack.hitPattern.numberOfValidPixelHits : -999")
    ),
    cms.PSet(
        tag = cms.untracked.string("NumberTrackerLayers"),
        quantity = cms.untracked.string("? track.isNonnull ? track.hitPattern.trackerLayersWithMeasurement : -999")
    ),
    cms.PSet(
        tag = cms.untracked.string("Dxy"),
        quantity = cms.untracked.string("userFloat('dxy')")
    ),
    cms.PSet(
        tag = cms.untracked.string("Dz"),
        quantity = cms.untracked.string("userFloat('dz')")
    ),
    cms.PSet(
        tag = cms.untracked.string("SumIso"),
        quantity = cms.untracked.string("trackIso + ecalIso + hcalIso")
    ),
    cms.PSet(
        tag = cms.untracked.string("SumChargedParticlePt"),
        quantity = cms.untracked.string("pfIsolationR04().sumChargedParticlePt")
    ),
    cms.PSet(
        tag = cms.untracked.string("SumChargedHadronPt"),
        quantity = cms.untracked.string("pfIsolationR04().sumChargedHadronPt")
    ),
    cms.PSet(
        tag = cms.untracked.string("SumNeutralHadronPt"),
        quantity = cms.untracked.string("pfIsolationR04().sumNeutralHadronEt")
    ),
    cms.PSet(
        tag = cms.untracked.string("SumPhotonPt"),
        quantity = cms.untracked.string("pfIsolationR04().sumPhotonEt")
    ),
    cms.PSet(
        tag = cms.untracked.string("SumPUPt"),
        quantity = cms.untracked.string("pfIsolationR04().sumPUPt")
    ),
)

electronVars = (
    cms.PSet(
        tag = cms.untracked.string("IsPassVeto"),
        quantity = cms.untracked.string("userInt('isPassVeto')")
    ),
    cms.PSet(
        tag = cms.untracked.string("IsPassLoose"),
        quantity = cms.untracked.string("userInt('isPassLoose')")
    ),
    cms.PSet(
        tag = cms.untracked.string("IsPassMedium"),
        quantity = cms.untracked.string("userInt('isPassMedium')")
    ),
    cms.PSet(
        tag = cms.untracked.string("IsPassTight"),
        quantity = cms.untracked.string("userInt('isPassTight')")
    ),
    cms.PSet(
        tag = cms.untracked.string("PassConversionVeto"),
        quantity = cms.untracked.string("passConversionVeto()")
    ),
    cms.PSet(
        tag = cms.untracked.string("SumChargedHadronPt"),
        quantity = cms.untracked.string("pfIsolationVariables().sumChargedHadronPt")
    ),
    cms.PSet(
        tag = cms.untracked.string("SumNeutralHadronEt"),
        quantity = cms.untracked.string("pfIsolationVariables().sumNeutralHadronEt")
    ),
    cms.PSet(
        tag = cms.untracked.string("SumPhotonEt"),
        quantity = cms.untracked.string("pfIsolationVariables().sumPhotonEt")
    ),
)

jetVars = ( 
    cms.PSet(
        tag = cms.untracked.string("CSV"),
        quantity = cms.untracked.string("bDiscriminator(\"combinedSecondaryVertexV1BJetTags\")")
    ),
    cms.PSet(
        tag = cms.untracked.string("NeutralHadronEnergy"),
        quantity = cms.untracked.string("neutralHadronEnergy()")
    ),
    cms.PSet(
        tag = cms.untracked.string("NeutralEmEnergy"),
        quantity = cms.untracked.string("neutralEmEnergy()")
    ),
    cms.PSet(
        tag = cms.untracked.string("ChargedHadronEnergy"),
        quantity = cms.untracked.string("chargedHadronEnergy()")
    ),
    cms.PSet(
        tag = cms.untracked.string("ChargedEmEnergy"),
        quantity = cms.untracked.string("chargedEmEnergy()")
    ),
    cms.PSet(
        tag = cms.untracked.string("MuonEnergy"),
        quantity = cms.untracked.string("muonEnergy()")
    ),
    cms.PSet(
        tag = cms.untracked.string("ElectronEnergy"),
        quantity = cms.untracked.string("electronEnergy()")
    ),
    cms.PSet(
        tag = cms.untracked.string("PhotonEnergy"),
        quantity = cms.untracked.string("photonEnergy()")
    ),
#    cms.PSet(
#        tag = cms.untracked.string("PtUncorrected"),
#        quantity = cms.untracked.string("correctedJet('Uncorrected').pt()")
#j    ),
)

tauVars = ( ) 
photonVars = ( )
pileupVars = ( 
    cms.PSet(
        tag = cms.untracked.string("puBX0"),
        quantity = cms.untracked.string("puBX0")
    ),
    cms.PSet(
        tag = cms.untracked.string("puBXup"),
        quantity = cms.untracked.string("puBXup")
    ),
    cms.PSet(
        tag = cms.untracked.string("puBXdown"),
        quantity = cms.untracked.string("puBXdown")
    ),
    cms.PSet(
        tag = cms.untracked.string("puBXOOT"),
        quantity = cms.untracked.string("puBXOOT")
    ),
    cms.PSet(
        tag = cms.untracked.string("puTrue"),
        quantity = cms.untracked.string("puTrue")
    ),
    cms.PSet(
        tag = cms.untracked.string("bestVertex"),
        quantity = cms.untracked.string("bextVertex")
    ),
) 
genParticleVars = ( 
        cms.PSet(
            tag = cms.untracked.string("ID"),
            quantity = cms.untracked.string("pdgId")
        ),
        cms.PSet(
            tag = cms.untracked.string("Status"),
            quantity = cms.untracked.string("status")
        ),
        cms.PSet(
            tag = cms.untracked.string("MomID"),
            quantity = cms.untracked.string("?numberOfMothers>0 ? mother(0).pdgId : -900")
        )
    )

# Tuple process generation
#

# Muons
muons = copy.deepcopy(basic)
muons.variables += muonVars
muons.src = cms.InputTag("muonUserData")

## Electrons
electrons = copy.deepcopy(basic)
electrons.variables += electronVars
electrons.src = cms.InputTag("electronUserData")

## Jets
jets = copy.deepcopy(basic)
jets.variables += jetVars
jets.src = cms.InputTag("jetUserData")

# Taus
taus = copy.deepcopy(basic)
taus.variables += tauVars
taus.src = cms.InputTag("tauUserData")

# Photons
photons = copy.deepcopy(basic)
photons.variables += photonVars
photons.src = cms.InputTag("photonUserData")

# GenParticle
genParticles = copy.deepcopy(basic)
genParticles.variables += genParticleVars
genParticles.src = cms.InputTag("genParticleUserData")

#
# MET (special case since it's weird)
met =  cms.EDProducer(
    "CandViewNtpProducer",
    src=cms.InputTag("skimmedPatMET"),
    lazyParser=cms.untracked.bool(True),
    prefix=cms.untracked.string(""),
    eventInfo=cms.untracked.bool(False),
    variables = cms.VPSet(
    cms.PSet(
    tag = cms.untracked.string("Pt"),
    quantity = cms.untracked.string("pt")
    ),
    cms.PSet(
    tag = cms.untracked.string("Px"),
    quantity = cms.untracked.string("px")
    ),
    cms.PSet(
    tag = cms.untracked.string("Py"),
    quantity = cms.untracked.string("py")
    ),
    cms.PSet(
    tag = cms.untracked.string("Phi"),
    quantity = cms.untracked.string("phi")
    ),
    )
    )

### event info: EventNumber, RunNumber, LumiBlock
eventInfo =  cms.EDProducer(
    "CandViewNtpProducer",
    src=cms.InputTag("skimmedPatMET"),
    lazyParser=cms.untracked.bool(True),
    prefix=cms.untracked.string("evtInfo"),
    eventInfo=cms.untracked.bool(True),
    variables = cms.VPSet()
    )
