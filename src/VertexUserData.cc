#include <vector>
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"


using std::vector;
//
// Class definition
//

class VertexUserData : public edm::EDProducer {
    public:
        explicit VertexUserData(const edm::ParameterSet&);
        ~VertexUserData();
    private:
        edm::InputTag vertexLabel;
        virtual void produce(edm::Event&, const edm::EventSetup&) override;
};

//
// Class methods
//

VertexUserData::VertexUserData(const edm::ParameterSet& iConfig):
    vertexLabel(iConfig.getParameter<edm::InputTag>("vertexLabel"))
{
   produces<std::vector<reco::Vertex> >();
}


VertexUserData::~VertexUserData()
{

}


// Produce the data. In this case, add some user floats
void
VertexUserData::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    // grab the input handles
    edm::Handle<vector<reco::Vertex> > vertexHandle;
    iEvent.getByLabel(vertexLabel, vertexHandle);
    std::auto_ptr<vector<reco::Vertex> > pvColl(new vector<reco::Vertex> (*vertexHandle));
   
    // All the floats we need for jets are already in miniAOD. Nice!
    iEvent.put(pvColl);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(VertexUserData);
