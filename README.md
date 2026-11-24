# CMS Event-Selection Accelerator (SKY130)

A streaming hardware block that selects collision events from CMS Open Data
using muon pT, |eta|, charge and multiplicity cuts. Written in Verilog,
verified against a Python reference model, and taken from RTL to GDSII
with Yosys, OpenROAD (OpenLane) and the SKY130 PDK.

## Goals
- Compare several architectures (combinational, pipelined, serial, multi-lane)
  on throughput, area, timing and estimated power.
- Learn the open-source ASIC flow end to end.
- Learn how trigger/DAQ-style data selection maps onto hardware.

## Scope and limitations
- Offline replay of CMS Open Data, not the real CMS trigger.
- CMS primary datasets are already filtered by the real trigger, so muon
  multiplicities and acceptance rates are biased and are not physics rates.
- Output is a post-layout GDSII plus reports, not a fabricated chip.

## Status
- [ ] Python reference model and data preprocessing
- [ ] RTL v1 + testbench
- [ ] OpenLane flow
- [ ] Architecture comparison
- [ ] Results writeup

## Repo layout
| Folder     | Contents |
|------------|----------|
| `model/`   | Python reference model and data preprocessing |
| `data/`    | Input data and stimulus files (large files are git-ignored) |
| `rtl/`     | Verilog source for each architecture |
| `tb/`      | Testbenches (cocotb / Verilog) |
| `flow/`    | OpenLane configs, one per architecture |
| `docs/`    | Notes, design decisions, diagrams |
| `results/` | Summary reports and plots (area, timing, power, throughput) |

## Data
CMS Open Data, NanoAOD muon branches (`nMuon`, `Muon_pt`, `Muon_eta`,
`Muon_charge`). See `data/README.md`.

## License
MIT, see `LICENSE`.
