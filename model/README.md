# model/

Python reference model and data preprocessing.

Planned contents:
- `explore.py`: inspect a CMS NanoAOD file (event count, nMuon distribution,
  pT and eta ranges) to choose fixed-point bit widths.
- `quantize.py`: convert muon pT/eta/charge to fixed-point words.
- `select.py`: golden event-selection function (the reference for the RTL).
- `make_stimulus.py`: write stimulus and expected-output files into `data/`.
