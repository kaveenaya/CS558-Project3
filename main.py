import math
import matplotlib.pyplot as plt

# Constants
AVOGADRO = 6.022e23  # atoms/mole
MW_ALUMINUM = 26.98  # g/mol
DECAY_CONSTANT = 0.005145  # s^-1
NEUTRON_FLUX = 1e8  # neutrons/cm^2/s
CROSS_SECTION = 231e-24  # cm^2

# User inputs
mass = float(input("Enter mass of aluminum (1e-6 to 1 g): "))
activation_time = int(input("Enter activation time in seconds (60 to 600): "))

# Input validation
if not (1e-6 <= mass <= 1):
    raise ValueError("Mass must be between 1e-6 and 1 gram.")
if not (60 <= activation_time <= 600):
    raise ValueError("Activation time must be between 60 and 600 seconds.")

# Calculate number of atoms
atoms = (mass * AVOGADRO) / MW_ALUMINUM

# Activation phase
time_step = 30
time_elapsed = 0
total_time = []
activation_activity = []

while time_elapsed <= activation_time:
    activity = NEUTRON_FLUX * atoms * CROSS_SECTION * (1 - math.exp(-DECAY_CONSTANT * time_elapsed))
    activation_activity.append(activity)
    total_time.append(time_elapsed)
    time_elapsed += time_step

# Final activation value becomes A₀ for decay
A0 = activation_activity[-1]

# Decay phase
decay_activity = []
while activity > 0.25 * A0:
    activity = A0 * math.exp(-DECAY_CONSTANT * (time_elapsed - activation_time))
    decay_activity.append(activity)
    total_time.append(time_elapsed)
    time_elapsed += time_step

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))

# Activation plot
ax.plot(total_time[:len(activation_activity)], activation_activity, label="Activation")

# Decay plot
ax.plot(total_time[len(activation_activity):], decay_activity, label="Decay")

# Mark transition point
ax.axvline(x=activation_time, color='red', linestyle='--', label="Decay begins")

# Labels and styling
ax.set_xlabel("Time (seconds)")
ax.set_ylabel("Activity (decays/second)")
ax.set_title("Radioactive Activation and Decay of Aluminum Sample")
ax.legend()
ax.grid(True)

# Save and show
plt.savefig("Activation_Decay_Plot.pdf")
plt.show()
