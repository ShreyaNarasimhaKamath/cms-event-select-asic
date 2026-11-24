# data/

Large files are git-ignored. Only this README and small samples (`data/sample/`)
are tracked.

## Source
CMS Open Data, CERN Open Data Portal (CC0):
- Record 12341: DoubleMuParked 2012, NanoAOD reduced to muons (good for a first pass).
- Record 30555: DoubleMuon 2016H NanoAOD (Run 2, larger files).

Files are read with `uproot` over XRootD (`root://eospublic.cern.ch//eos/opendata/...`)
or downloaded from the record page. Only these branches are needed:
`nMuon`, `Muon_pt`, `Muon_eta`, `Muon_charge`.

## Note
Primary datasets are already trigger-selected, so muon multiplicity is biased.
