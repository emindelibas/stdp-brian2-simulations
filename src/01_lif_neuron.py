"""
01_lif_neuron.py

Single Leaky Integrate-and-Fire (LIF) neuron simulation used in the thesis.
The script generates the membrane potential response and marks spike times.

Output:
    outputs/fig_2_1_lif_neuron.png
"""

from brian2 import *
from pylab import *
from pathlib import Path


# -------------------------------------------------------------------------
# Output folder
# -------------------------------------------------------------------------

output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)


# -------------------------------------------------------------------------
# LIF neuron model
# -------------------------------------------------------------------------

start_scope()

tau = 5 * ms

eqs = """
dv/dt = (1-v)/tau : 1
"""

G = NeuronGroup(
    1,
    eqs,
    threshold="v > 0.8",
    reset="v = 0",
    method="exact"
)

G.v = 0

statemon = StateMonitor(G, "v", record=0)
spikemon = SpikeMonitor(G)


# -------------------------------------------------------------------------
# Run simulation
# -------------------------------------------------------------------------

run(50 * ms)


# -------------------------------------------------------------------------
# Plot result
# -------------------------------------------------------------------------

figure(figsize=(6, 4))

plot(statemon.t / ms, statemon.v[0])

for t in spikemon.t:
    axvline(t / ms, ls="--", c="C1", lw=3)

xlabel("Time (ms)")
ylabel("v")
title("Single LIF Neuron Simulation")
grid(True, alpha=0.3)
tight_layout()

savefig(output_dir / "fig_2_1_lif_neuron.png", dpi=300)
show()
