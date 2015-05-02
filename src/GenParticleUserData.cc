#include <vector>

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"


using std::vector;
//
// Class definition
//

class GenParticleUserData : public edm::EDProducer {
    public:
        explicit GenParticleUserData(const edm::ParameterSet&);
        ~GenParticleUserData();
    private:
        edm::InputTag genParticleLabel;
        edm::InputTag vertexLabel;
        virtual void produce(edm::Event&, const edm::EventSetup&) override;
};

//
// Class methods
//

GenParticleUserData::GenParticleUserData(const edm::ParameterSet& iConfig):
    genParticleLabel(iConfig.getParameter<edm::InputTag>("genParticleLabel")),
    vertexLabel(iConfig.getParameter<edm::InputTag>("vertexLabel"))
{
    produces<std::vector<reco::GenParticle> >();
}


GenParticleUserData::~GenParticleUserData()
{

}


// Produce the data. In this case, add some user floats
void
GenParticleUserData::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    // grab the input handles
    edm::Handle<vector<reco::GenParticle> > genParticleHandle;
    iEvent.getByLabel(genParticleLabel, genParticleHandle);
    std::auto_ptr<vector<reco::GenParticle> > genParticleColl(new vector<reco::GenParticle> (*genParticleHandle));

    edm::Handle<vector<reco::Vertex> > vertexHandle;
    iEvent.getByLabel(vertexLabel, vertexHandle);
    std::auto_ptr<vector<reco::Vertex> > pvColl(new vector<reco::Vertex> (*vertexHandle));
   
    // All the floats we need for genParticles are already in miniAOD. Nice!
    if ( ! iEvent.eventAuxiliary().isRealData() ) {
        iEvent.put(genParticleColl);
    }
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(GenParticleUserData);
