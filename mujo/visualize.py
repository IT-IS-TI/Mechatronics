import matplotlib.pyplot as plt
import seaborn as sns

joints = ['Joint 1', 'Joint 2', 'Joint 3', 'Joint 4', 'Joint 5', 'Joint 6']
torques = [15, 25, 20, 10, 8, 5]  
rated_torques = [20, 30, 25, 15, 10, 7]  

plt.bar(joints, torques, label="Simulated Torques")
plt.plot(joints, rated_torques, color="red", linestyle="--", label="Rated Torques")
plt.ylabel("Torque (Nm)")
plt.title("Static Torque Comparison")
plt.legend()
plt.show()

sns.violinplot(data=[torques], scale='count', inner="stick")
plt.xticks(ticks=range(len(joints)), labels=joints)
plt.ylabel("Torque (Nm)")
plt.title("Torque Distribution Across Joints")
plt.show()
