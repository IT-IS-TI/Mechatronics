from lxml import etree
import numpy as np

def update_joint_parameters(xml_path, output_path, motor_variants):
    def calculate_motor_inertia(mass, radius, height):
        I = np.array([
            [1/12 * mass * (3 * radius**2 + height**2), 0, 0],
            [0, 1/12 * mass * (3 * radius**2 + height**2), 0],
            [0, 0, 1/2 * mass * radius**2]
        ])
        return I

    def apply_parallel_axis_theorem(I, mass, offset):
        d = np.linalg.norm(offset)
        return I + mass * d**2 * np.eye(3)

    tree = etree.parse(xml_path)
    root = tree.getroot()

    for joint in root.findall(".//joint"):
        joint_name = joint.get("name")

        armature = 0.01
        joint.set("armature", str(armature))

        parent_body = joint.getparent()
        inertial = parent_body.find("inertial")

        if inertial is not None:
            mass = float(inertial.get("mass", "0"))
            motor_mass = 0.5  
            new_mass = mass + motor_mass
            inertial.set("mass", str(new_mass))

            diaginertia = np.array(list(map(float, inertial.get("diaginertia").split())))
            motor_radius = 0.05  
            motor_height = 0.1   
            motor_inertia = calculate_motor_inertia(motor_mass, motor_radius, motor_height)
            offset = np.array([0, 0, 0.05]) 
            new_inertia = apply_parallel_axis_theorem(motor_inertia, motor_mass, offset) + diaginertia
            inertial.set("diaginertia", " ".join(map(str, new_inertia.diagonal())))

    for variant in motor_variants:
        for joint in root.findall(".//joint"):
            motor = etree.Element("motor", name=f"{joint.get('name')}_motor",
                                  joint=joint.get("name"),
                                  ctrlrange="-100 100")
            root.append(motor)

    tree.write(output_path, pretty_print=True)

motor_variants = [
    {"mass": 0.5, "radius": 0.05, "height": 0.1},
    {"mass": 0.6, "radius": 0.06, "height": 0.12}
]
update_joint_parameters("UR3_copy.xml", "updated_UR3.xml", motor_variants)

# UNCOMMENT THE NEXT CODE SNIPPET IN CASE OF AN ERROR

# def update_model_with_actuators(xml_path, output_path, motor_configurations):
#     parser = etree.XMLParser(remove_blank_text=True)
#     tree = etree.parse(xml_path, parser)
#     root = tree.getroot()

#     actuator_tag = root.find("actuator")
#     if actuator_tag is None:
#         actuator_tag = etree.SubElement(root, "actuator")

#     for motor in motor_configurations:
#         actuator_element = etree.SubElement(actuator_tag, "motor")
#         actuator_element.set("name", motor["name"])
#         actuator_element.set("joint", motor["joint"])
#         actuator_element.set("ctrlrange", f"{motor['ctrlrange'][0]} {motor['ctrlrange'][1]}")
#         actuator_element.set("gear", str(motor["gear"]))

#     tree.write(output_path, pretty_print=True, xml_declaration=True, encoding="UTF-8")


# # We need to change a bit
# motor_configs = [
#     {"name": "motor_shoulder_pan", "joint": "shoulder_pan_joint", "ctrlrange": [-330, 330], "gear": 120},
#     {"name": "motor_shoulder_lift", "joint": "shoulder_lift_joint", "ctrlrange": [-330, 330], "gear": 100},
#     {"name": "motor_elbow", "joint": "elbow_joint", "ctrlrange": [-150, 150], "gear": 80},
#     {"name": "motor_wrist_1", "joint": "wrist_1_joint", "ctrlrange": [-54, 54], "gear": 50},
#     {"name": "motor_wrist_2", "joint": "wrist_2_joint", "ctrlrange": [-54, 54], "gear": 40},
#     {"name": "motor_wrist_3", "joint": "wrist_3_joint", "ctrlrange": [-54, 54], "gear": 30},
# ]

# update_model_with_actuators("UR3_copy.xml", "updated_UR3.xml", motor_configs)
