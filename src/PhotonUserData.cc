#include <vector>

#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"


using std::vector;
//
// Class definition
//

class PhotonUserData : public edm::EDProducer {
    public:
        explicit PhotonUserData(const edm::ParameterSet&);
        ~PhotonUserData();
    private:
        edm::InputTag photonLabel;
        edm::InputTag vertexLabel;
        virtual void produce(edm::Event&, const edm::EventSetup&) override;
};

//
// Class methods
//

PhotonUserData::PhotonUserData(const edm::ParameterSet& iConfig):
    photonLabel(iConfig.getParameter<edm::InputTag>("photonLabel")),
    vertexLabel(iConfig.getParameter<edm::InputTag>("vertexLabel"))
{
    produces<std::vector<pat::Photon> >();
}


PhotonUserData::~PhotonUserData()
{

}


// Produce the data. In this case, add some user floats
void
PhotonUserData::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    // grab the input handles
    edm::Handle<vector<pat::Photon> > photonHandle;
    iEvent.getByLabel(photonLabel, photonHandle);
    std::auto_ptr<vector<pat::Photon> > photonColl(new vector<pat::Photon> (*photonHandle));

    edm::Handle<vector<reco::Vertex> > vertexHandle;
    iEvent.getByLabel(vertexLabel, vertexHandle);
    std::auto_ptr<vector<reco::Vertex> > pvColl(new vector<reco::Vertex> (*vertexHandle));
   
    // All the floats we need for photons are already in miniAOD. Nice!

    iEvent.put(photonColl);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PhotonUserData);
