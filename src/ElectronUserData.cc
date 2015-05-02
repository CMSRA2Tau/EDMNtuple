#include <vector>

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"


using std::vector;
//
// Class definition
//

class ElectronUserData : public edm::EDProducer {
    public:
        explicit ElectronUserData(const edm::ParameterSet&);
        ~ElectronUserData();
    private:
        edm::InputTag electronLabel;
        edm::InputTag vertexLabel;
        edm::InputTag electronVetoIdMapLabel;
        edm::InputTag electronLooseIdMapLabel;
        edm::InputTag electronMediumIdMapLabel;
        edm::InputTag electronTightIdMapLabel;
        virtual void produce(edm::Event&, const edm::EventSetup&) override;
};

//
// Class methods
//

ElectronUserData::ElectronUserData(const edm::ParameterSet& iConfig):
    electronLabel(iConfig.getParameter<edm::InputTag>("electronLabel")),
    vertexLabel(iConfig.getParameter<edm::InputTag>("vertexLabel")),
    electronVetoIdMapLabel(iConfig.getParameter<edm::InputTag>("electronVetoIdMap")),
    electronLooseIdMapLabel(iConfig.getParameter<edm::InputTag>("electronLooseIdMap")),
    electronMediumIdMapLabel(iConfig.getParameter<edm::InputTag>("electronMediumIdMap")),
    electronTightIdMapLabel(iConfig.getParameter<edm::InputTag>("electronTightIdMap"))
{
    produces<std::vector<pat::Electron> >();
}


ElectronUserData::~ElectronUserData()
{

}


// Produce the data. In this case, add some user floats
void
ElectronUserData::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    // grab the input handles
    edm::Handle<edm::View<pat::Electron> > electronHandle;
    edm::Handle<vector<pat::Electron> > electronVector;
    iEvent.getByLabel(electronLabel, electronHandle);
    iEvent.getByLabel(electronLabel, electronVector);
    std::auto_ptr<vector<pat::Electron> > electronColl(new vector<pat::Electron> (*electronVector));

    edm::Handle<vector<reco::Vertex> > vertexHandle;
    iEvent.getByLabel(vertexLabel, vertexHandle);
    std::auto_ptr<vector<reco::Vertex> > pvColl(new vector<reco::Vertex> (*vertexHandle));
    reco::TrackBase::Point vtxPoint(0,0, 0);
    if(  pvColl->size() >= 1 ) {
        vtxPoint = pvColl->at(0).position();
    }


    edm::Handle<edm::ValueMap<bool> > vetoDecision;
    iEvent.getByLabel(electronVetoIdMapLabel, vetoDecision);
    edm::Handle<edm::ValueMap<bool> > looseDecision;
    iEvent.getByLabel(electronLooseIdMapLabel, looseDecision);
    edm::Handle<edm::ValueMap<bool> > mediumDecision;
    iEvent.getByLabel(electronMediumIdMapLabel, mediumDecision);
    edm::Handle<edm::ValueMap<bool> > tightDecision;
    iEvent.getByLabel(electronTightIdMapLabel, tightDecision);
    // Can't initialize for loop with two types
    auto i = electronHandle->begin();
    auto j = electronColl->begin();
    for ( /* nothing */ ;i != electronHandle->end(); ++i, ++j) {
        // Collect variables
        float d0 = (-1) * j->gsfTrack()->dxy(vtxPoint);
        float dz = j->gsfTrack()->dz(vtxPoint);                                     
        float missHits = j->gsfTrack()->hitPattern().numberOfLostTrackerHits(reco::HitPattern::MISSING_INNER_HITS);
        const edm::Ptr<pat::Electron> ptr(electronHandle, i - electronHandle->begin() );
        int isPassVeto, isPassLoose, isPassMedium, isPassTight;
        // On my (Melo) machine, the electron module won't compile properly, so
        // the values aren't in the event data. Hack around it temporarily
        if ( !vetoDecision.isValid() || !looseDecision.isValid() || 
                !mediumDecision.isValid() || !tightDecision.isValid() ) {
            // FIXME Obviously wrong
            isPassVeto   = -1;                          
            isPassLoose  = -1;                     
            isPassMedium = -1;                    
            isPassTight  = -1;
        } else {
            isPassVeto   = (*vetoDecision)[ ptr ];                             
            isPassLoose  = (*looseDecision)[ ptr ];                            
            isPassMedium = (*mediumDecision)[ ptr ];                           
            isPassTight  = (*tightDecision)[ ptr ];
        }


        // Store variables  
        j->addUserInt("isPassVeto", isPassVeto);
        j->addUserInt("isPassLoose", isPassLoose);
        j->addUserInt("isPassMedium", isPassMedium);
        j->addUserInt("isPassTight", isPassTight);
        j->addUserFloat("d0", d0);
        j->addUserFloat("dz", dz);
        j->addUserFloat("MissingHits", missHits);
    }
    iEvent.put(electronColl);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(ElectronUserData);
