// Dumps PU/BX info from the event
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include <vector>
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "PhysicsTools/Utilities/interface/LumiReWeighting.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

using std::vector;

class PUDumper : public edm::EDProducer {
    public:
        explicit PUDumper(const edm::ParameterSet& cfg);
        ~PUDumper();

    private:
        virtual void produce(edm::Event& event, const edm::EventSetup& setup);
        edm::InputTag puLabel;
        edm::InputTag vertexLabel;
        double ndofMin;
        double vtxMax;
        double vtxDxDyMax;
};

PUDumper::~PUDumper() { }

PUDumper::PUDumper(const edm::ParameterSet& iConfig):
    puLabel(iConfig.getParameter<edm::InputTag>("puLabel")),
    vertexLabel(iConfig.getParameter<edm::InputTag>("vertexLabel")),
    ndofMin(iConfig.getParameter<double>("vertexNdofMin")),
    vtxMax(iConfig.getParameter<double>("vertexZMax")),
    vtxDxDyMax(iConfig.getParameter<double>("vertexDxDyMax"))
{
    produces<int>("puBX0");
    produces<int>("puBXup");
    produces<int>("puBXdown");
    produces<int>("puBXOOT");
    produces<int>("puTrue");
    produces<int>("bestVertex");
}

void PUDumper::produce(edm::Event& iEvent, const edm::EventSetup& setup) {

    // Get PU info
    if ( ! iEvent.eventAuxiliary().isRealData() ) {
        std::auto_ptr<int> bx0(new int);
        std::auto_ptr<int> bxup(new int);
        std::auto_ptr<int> bxdown(new int);
        std::auto_ptr<int> bxoot(new int);
        std::auto_ptr<int> bxtrue(new int);
        *bx0 = *bxup = *bxdown = *bxoot = *bxtrue = 0;
        edm::Handle<std::vector<PileupSummaryInfo> > puHandle;
        iEvent.getByLabel(puLabel, puHandle);
        std::auto_ptr<vector<PileupSummaryInfo> > puColl(new vector<PileupSummaryInfo> (*puHandle));

        for (auto iter = puColl->begin(); iter != puColl->end(); ++iter) {
            int bx = iter->getBunchCrossing();
            int pu = iter->getPU_NumInteractions();
            if (bx == 0) {
                (*bx0) += pu;
                (*bxtrue) = iter->getTrueNumInteractions();
            } else if (bx == -1) {
                (*bxdown) += pu;
            } else if (bx == 1) {
                (*bxup) += pu;
            } else {
                (*bxoot) += pu;
            }
        }
        iEvent.put(bx0,"puBX0");
        iEvent.put(bxup,"puBXup");
        iEvent.put(bxdown,"puBXdown");
        iEvent.put(bxoot,"puBXOOT");
        iEvent.put(bxtrue,"puTrue");
    }

    // Count the best vertices
    std::auto_ptr<int> bestVertex(new int);
    *bestVertex = 0;
    edm::Handle<vector<reco::Vertex> > vertexHandle;
    iEvent.getByLabel(vertexLabel, vertexHandle);
    std::auto_ptr<vector<reco::Vertex> > pvColl(new vector<reco::Vertex> (*vertexHandle));
    for (auto iter = pvColl->begin(); iter != pvColl->end(); ++iter) {
        if (iter->isValid() && iter->isFake()) {
            double vtxDxy = sqrt((iter->x() * iter->x()) +
                                    (iter->y() * iter->y()));
            if ((iter->ndof() >= ndofMin) &&
                    (abs(iter->z()) < vtxMax) &&
                    (vtxDxy < vtxDxDyMax)) {
                (*bestVertex)++;
            }
        }
    }
    iEvent.put(bestVertex,"bestVertex");
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PUDumper);
