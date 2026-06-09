"""
02_symmetric_stdp_window.py

Symmetric Spike-Timing-Dependent Plasticity (STDP) learning window simulation.

This script generates the symmetric STDP learning window discussed in Chapter 2
of the graduation thesis.

Output:
    outputs/fig_2_2_symmetric_stdp.png
"""

from brian2 import *
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np


# -------------------------------------------------------------------------
# Output folder
# -------------------------------------------------------------------------

output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)


# -------------------------------------------------------------------------
# Simulation setup
# -------------------------------------------------------------------------

start_scope()

# STDP parameters
taupre = taupost = 20 * ms
Apre = 0.001
Apost = -0.001
tmax = 80 * ms
N = 100


# -------------------------------------------------------------------------
# Presynaptic and postsynaptic spike times
# -------------------------------------------------------------------------

G = NeuronGroup(
    N,
    "tspike : second",
    threshold="t > tspike",
    refractory=100 * ms
)

H = NeuronGroup(
    N,
    "tspike : second",
    threshold="t > tspike",
    refractory=100 * ms
)

G.tspike = "i * tmax / (N - 1)"
H.tspike = "(N - 1 - i) * tmax / (N - 1)"


# -------------------------------------------------------------------------
# STDP synapse model
# -------------------------------------------------------------------------

S = Synapses(
    G,
    H,
    """
    w : 1
    dapre/dt = -apre/taupre : 1 (event-driven)
    dapost/dt = -apost/taupost : 1 (event-driven)
    """,
    on_pre="""
    apre += Apre
    w += apost
    """,
    on_post="""
    apost += Apost
    w += apre
    """
)

S.connect(j="i")
S.w = 0.0


# -------------------------------------------------------------------------
# Run simulation
# -------------------------------------------------------------------------

run(tmax + 1 * ms)


# -------------------------------------------------------------------------
# Calculate time difference and weight change
# -------------------------------------------------------------------------

dt = (H.tspike - G.tspike) / ms
dw = np.array(S.w[:])

# Sort values for a cleaner curve
sort_index = np.argsort(dt)
dt = dt[sort_index]
dw = dw[sort_index]


# -------------------------------------------------------------------------
# Plot STDP learning window
# -------------------------------------------------------------------------

plt.figure(figsize=(5.5, 4))

plt.plot(dt, dw, "g")

plt.axhline(0, ls="--", c="k")
plt.axvline(0, ls="--", c="k")

plt.xlabel("Time (Post - Pre) (ms)")
plt.ylabel("Weight change")
plt.title("Symmetric STDP Learning Window")

plt.xlim(-80, 80)
plt.ylim(-0.0011, 0.0011)

plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(output_dir / "fig_2_2_symmetric_stdp.png", dpi=300)
plt.show()
