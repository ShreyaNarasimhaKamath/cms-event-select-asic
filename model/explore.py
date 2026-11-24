"""Explore a CMS NanoAOD muon file to choose fixed-point widths for the RTL.

Usage:
    python model/explore.py <path-or-url-to-root-file> [--max-events N] [--plot]

Examples:
    python model/explore.py data/muons.root --max-events 500000 --plot
    python model/explore.py root://eospublic.cern.ch//eos/opendata/cms/... (needs fsspec-xrootd, Linux/WSL)
"""
import argparse
import math

import awkward as ak
import numpy as np
import uproot

BRANCHES = ["nMuon", "Muon_pt", "Muon_eta", "Muon_charge"]


def bits_needed(max_value: int) -> int:
    """Unsigned bits needed to represent integers 0..max_value."""
    return max(1, math.ceil(math.log2(max_value + 1)))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="local path or root:// URL")
    ap.add_argument("--max-events", type=int, default=500_000)
    ap.add_argument("--pt-step", type=float, default=0.25, help="pT resolution in GeV")
    ap.add_argument("--eta-step", type=float, default=0.01, help="eta resolution")
    ap.add_argument("--plot", action="store_true", help="save docs/explore.png")
    args = ap.parse_args()

    with uproot.open(args.file) as f:
        tree = f["Events"]
        total = tree.num_entries
        arrays = tree.arrays(BRANCHES, entry_stop=args.max_events)

    n_events = len(arrays)
    nmu = ak.to_numpy(arrays["nMuon"])
    pt = ak.to_numpy(ak.flatten(arrays["Muon_pt"]))
    eta = ak.to_numpy(ak.flatten(arrays["Muon_eta"]))
    charge = ak.to_numpy(ak.flatten(arrays["Muon_charge"]))

    print(f"File events: {total:,}   read: {n_events:,}   muons read: {len(pt):,}")

    print("\nMuon multiplicity (nMuon):")
    counts = np.bincount(nmu)
    for n, c in enumerate(counts):
        if c:
            print(f"  nMuon={n:2d}: {c:9,d}  ({100 * c / n_events:6.2f}%)")
    max_nmu = int(nmu.max())
    print(f"  max nMuon = {max_nmu}  -> count field needs {bits_needed(max_nmu)} bits")

    print("\nMuon pT (GeV):")
    print(f"  min {pt.min():.3f}  median {np.median(pt):.3f}  "
          f"p99 {np.percentile(pt, 99):.1f}  p99.9 {np.percentile(pt, 99.9):.1f}  max {pt.max():.1f}")
    pt_max_code = int(math.ceil(pt.max() / args.pt_step))
    print(f"  at {args.pt_step} GeV/step: max code {pt_max_code} -> {bits_needed(pt_max_code)} bits "
          f"(saturate at p99.9 to save bits)")

    print("\nMuon eta:")
    print(f"  min {eta.min():.3f}  max {eta.max():.3f}  |eta| p99 {np.percentile(np.abs(eta), 99):.2f}")
    eta_abs_code = int(math.ceil(np.abs(eta).max() / args.eta_step))
    print(f"  at {args.eta_step}/step: |eta| max code {eta_abs_code} -> "
          f"{bits_needed(eta_abs_code)} bits + 1 sign bit")

    print("\nMuon charge:")
    for q in np.unique(charge):
        print(f"  charge {int(q):+d}: {(charge == q).sum():,}")

    if args.plot:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(1, 3, figsize=(13, 3.6))
        ax[0].bar(range(len(counts)), counts)
        ax[0].set(xlabel="nMuon", ylabel="events", yscale="log")
        ax[1].hist(pt, bins=100, range=(0, min(pt.max(), 200)))
        ax[1].set(xlabel="Muon pT [GeV]", yscale="log")
        ax[2].hist(eta, bins=100)
        ax[2].set(xlabel="Muon eta")
        fig.tight_layout()
        fig.savefig("docs/explore.png", dpi=130)
        print("\nSaved docs/explore.png")


if __name__ == "__main__":
    main()
