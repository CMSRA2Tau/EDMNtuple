#include <vector>

#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"


using std::vector;
//
// Class definition
//

class TauUserData : public edm::EDProducer {
    public:
        explicit TauUserData(const edm::ParameterSet&);
        ~TauUserData();
    private:
        edm::InputTag tauLabel;
        edm::InputTag vertexLabel;
        virtual void produce(edm::Event&, const edm::EventSetup&) override;
};

//
// Class methods
//

TauUserData::TauUserData(const edm::ParameterSet& iConfig):
    tauLabel(iConfig.getParameter<edm::InputTag>("tauLabel")),
    vertexLabel(iConfig.getParameter<edm::InputTag>("vertexLabel"))
{
    produces<std::vector<pat::Tau> >();
}


TauUserData::~TauUserData()
{

}


// Produce the data. In this case, add some user floats
void
TauUserData::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    // grab the input handles
    edm::Handle<vector<pat::Tau> > tauHandle;
    iEvent.getByLabel(tauLabel, tauHandle);
    std::auto_ptr<vector<pat::Tau> > tauColl(new vector<pat::Tau> (*tauHandle));

    edm::Handle<vector<reco::Vertex> > vertexHandle;
    iEvent.getByLabel(vertexLabel, vertexHandle);
    std::auto_ptr<vector<reco::Vertex> > pvColl(new vector<reco::Vertex> (*vertexHandle));
   
    // All the floats we need for taus are already in miniAOD. Nice!

    iEvent.put(tauColl);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(TauUserData);
