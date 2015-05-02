#include <vector>

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"


using std::vector;
//
// Class definition
//

class JetUserData : public edm::EDProducer {
    public:
        explicit JetUserData(const edm::ParameterSet&);
        ~JetUserData();
    private:
        edm::InputTag jetLabel;
        edm::InputTag vertexLabel;
        virtual void produce(edm::Event&, const edm::EventSetup&) override;
};

//
// Class methods
//

JetUserData::JetUserData(const edm::ParameterSet& iConfig):
    jetLabel(iConfig.getParameter<edm::InputTag>("jetLabel")),
    vertexLabel(iConfig.getParameter<edm::InputTag>("vertexLabel"))
{
    produces<std::vector<pat::Jet> >();
}


JetUserData::~JetUserData()
{

}


// Produce the data. In this case, add some user floats
void
JetUserData::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    // grab the input handles
    edm::Handle<vector<pat::Jet> > jetHandle;
    iEvent.getByLabel(jetLabel, jetHandle);
    std::auto_ptr<vector<pat::Jet> > jetColl(new vector<pat::Jet> (*jetHandle));

    edm::Handle<vector<reco::Vertex> > vertexHandle;
    iEvent.getByLabel(vertexLabel, vertexHandle);
    std::auto_ptr<vector<reco::Vertex> > pvColl(new vector<reco::Vertex> (*vertexHandle));
   
    // All the floats we need for jets are already in miniAOD. Nice!

    iEvent.put(jetColl);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(JetUserData);
