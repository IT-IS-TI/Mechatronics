import pybullet as p
import numpy as np

physicsClient = p.connect(p.DIRECT)
p.loadURDF("ur3.urdf")

joint_angles = [0, np.pi/4, -np.pi/2, np.pi/4, np.pi/4, 0]
p.setJointMotorControlArray(
    bodyUniqueId=1, 
    jointIndices=range(6), 
    controlMode=p.POSITION_CONTROL, 
    targetPositions=joint_angles
)

torques = []
for i in range(6):
    joint_info = p.getJointInfo(1, i)
    torque = p.calculateInverseDynamics(1, joint_angles, [0]*6, [0]*6)[i]
    torques.append(torque)

print("Static Torques:", torques)
p.disconnect()
