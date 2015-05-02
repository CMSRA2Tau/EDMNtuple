#include <vector>

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"


using std::vector;
//
// Class definition
//

class MuonUserData : public edm::EDProducer {
    public:
        explicit MuonUserData(const edm::ParameterSet&);
        ~MuonUserData();
    private:
        edm::InputTag muonLabel;
        edm::InputTag vertexLabel;
        int vtxNdofMin;
        int vtxRhoMax;
        double vtxZMax;
        virtual void produce(edm::Event&, const edm::EventSetup&) override;
};

//
// Class methods
//

MuonUserData::MuonUserData(const edm::ParameterSet& iConfig):
    muonLabel(iConfig.getParameter<edm::InputTag>("muonLabel")),
    vertexLabel(iConfig.getParameter<edm::InputTag>("vertexLabel")),
    vtxNdofMin(iConfig.getParameter<int>("vertexNdofMin")),
    vtxRhoMax(iConfig.getParameter<int>("vertexRhoMax")),
    vtxZMax(iConfig.getParameter<double>("vertexZMax"))
{
    produces<std::vector<pat::Muon> >();
}


MuonUserData::~MuonUserData()
{

}


// Produce the data. In this case, add some user floats
void
MuonUserData::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    // grab the input handles
    edm::Handle<vector<pat::Muon> > muonHandle;
    iEvent.getByLabel(muonLabel, muonHandle);
    std::auto_ptr<vector<pat::Muon> > muonColl(new vector<pat::Muon> (*muonHandle));

    edm::Handle<vector<reco::Vertex> > vertexHandle;
    iEvent.getByLabel(vertexLabel, vertexHandle);
    std::auto_ptr<vector<reco::Vertex> > pvColl(new vector<reco::Vertex> (*vertexHandle));

    // Get the vertex
    auto vtx = pvColl->end();
    for (auto i = pvColl->begin(); i != pvColl->end(); ++i) {
        if ( (!i->isFake()) &&
                (i->ndof() >= vtxNdofMin) &&
                (i->position().Rho() <= vtxRhoMax) &&
                (fabs(i->position().Z() <= vtxZMax) ) ) {
            vtx = i;
            break;
        }
    }
    bool goodPrimaryVertex = false;

    for (auto i = muonColl->begin(); i != muonColl->end(); ++i) {
        pat::Muon & m = *i;

        // Collect variables
        double isSoftMuon, isTightMuon, dz, dxy;
        if (goodPrimaryVertex && m.isLooseMuon()) {
            isSoftMuon = m.isSoftMuon(*vtx);
            isTightMuon = m.isTightMuon(*vtx);
            dz = m.muonBestTrack()->dz(vtx->position());
            dxy = m.muonBestTrack()->dxy(vtx->position());
        } else {
            isSoftMuon = isTightMuon = dz = dxy = -999;
        }

        // Store variables
        m.addUserFloat("dz", dz);
        m.addUserFloat("dxy", dxy);
        m.addUserFloat("isSoftMuon", isSoftMuon);
        m.addUserFloat("isTightMuon", isTightMuon);
    }

    iEvent.put(muonColl);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MuonUserData);
