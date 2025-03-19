print("Soil Properties Calculator")
print("Leave unknown values blank")

def get_value(prompt, unit=""):
    while True:
        try:
            if unit:
                val = input(prompt + " (" + unit + "): ")
            else:
                val = input(prompt + ": ")
            if val.strip():
                return float(val)
            return None
        except ValueError:
            print("Invalid input. Please enter a number.")

# Initialize dictionary with default values
soil = {
    "rho_w": 1000,  # ρw Density of water (kg/m³)
    "gamma_w": 9.81,  # γw Unit weight of water (kN/m³)
    "Gs": None,  # Gs Specific gravity (dimensionless)
    "e": None,  # e Void ratio (dimensionless)
    "w": None,  # w Water content (decimal)
    "rho": None,  # ρ Bulk density (kg/m³)
    "rho_d": None,  # ρd Dry density (kg/m³)
    "gamma": None,  # γ Unit weight (kN/m³)
    "n": None,  # n Porosity (decimal)
    "S": None,  # S Degree of saturation (decimal)
    "Vs": None,  # Vs Volume of solids (m³)
    "Vw": None,  # Vw Volume of water (m³)
    "Va": None,  # Va Volume of air (m³)
    "V": None,  # V Total volume (m³)
    "Vv": None,  # Vv Volume of voids (m³)
    "Ms": None,  # Ms Mass of solids (kg)
    "Mw": None,  # Mw Mass of water (kg)
    "M": None,  # M Total mass (kg)
    "gamma_sat": None,  # γsat Saturated unit weight (kN/m³)
    "gamma_prime": None,  # γ' Buoyant unit weight (kN/m³)
    "rho_s": None,  # ρs Density of solids (kg/m³)
    "e_max": None,  # e_max Maximum void ratio (dimensionless)
    "e_min": None,  # e_min Minimum void ratio (dimensionless)
    "ID": None  # ID Relative density (%)
}

# Get key user inputs
for key, description, unit in [
    ("Gs", "Gs Specific gravity", "dimensionless"),
    ("e", "e Void ratio", "dimensionless"),
    ("w", "w Water content", "decimal"),
    ("rho", "ρ Bulk density", "kg/m³"),
    ("rho_d", "ρd Dry density", "kg/m³"),
    ("gamma", "γ Unit weight", "kN/m³"),
    ("n", "n Porosity", "decimal"),
    ("S", "S Degree of saturation", "decimal"),
    ("Vs", "Vs Volume of solids", "m³"),
    ("Vw", "Vw Volume of water", "m³"),
    ("Va", "Va Volume of air", "m³"),
    ("V", "V Total volume", "m³"),
    ("Ms", "Ms Mass of solids", "kg"),
    ("Mw", "Mw Mass of water", "kg"),
    ("M", "M Total mass", "kg"),
    ("gamma_sat", "γsat Saturated unit weight", "kN/m³"),
    ("gamma_prime", "γ' Buoyant unit weight", "kN/m³"),
    ("rho_s", "ρs Density of solids", "kg/m³"),
    ("e_max", "e_max Maximum void ratio", "dimensionless"),
    ("e_min", "e_min Minimum void ratio", "dimensionless"),
    ("ID", "ID Relative density", "%")
]:
    soil[key] = get_value(description, unit)

# Perform calculations based on available data
print("\nCalculating soil properties...\n")

# Run multiple calculation passes to ensure all possible values are calculated
for _ in range(3):  # Run 3 passes to ensure interdependent calculations are resolved
    
    # Volume relationships
    # Volume of voids = Volume of air + Volume of water
    if soil["Vv"] is None and soil["Va"] is not None and soil["Vw"] is not None:
        soil["Vv"] = soil["Va"] + soil["Vw"]
        print("Vv =", soil["Vv"], "m³")

    # Total volume = Volume of solids + Volume of voids
    if soil["V"] is None and soil["Vs"] is not None and soil["Vv"] is not None:
        soil["V"] = soil["Vs"] + soil["Vv"]
        print("V =", soil["V"], "m³")

    # Volume of voids = Total volume - Volume of solids
    if soil["Vv"] is None and soil["V"] is not None and soil["Vs"] is not None:
        soil["Vv"] = soil["V"] - soil["Vs"]
        print("Vv =", soil["Vv"], "m³")

    # Volume of air = Volume of voids - Volume of water
    if soil["Va"] is None and soil["Vv"] is not None and soil["Vw"] is not None:
        soil["Va"] = soil["Vv"] - soil["Vw"]
        print("Va =", soil["Va"], "m³")

    # Volume of water = Volume of voids - Volume of air
    if soil["Vw"] is None and soil["Vv"] is not None and soil["Va"] is not None:
        soil["Vw"] = soil["Vv"] - soil["Va"]
        print("Vw =", soil["Vw"], "m³")
    
    # Volume of solids = Total volume - Volume of voids
    if soil["Vs"] is None and soil["V"] is not None and soil["Vv"] is not None:
        soil["Vs"] = soil["V"] - soil["Vv"]
        print("Vs =", soil["Vs"], "m³")

    # Mass relationships
    # Total mass = Mass of solids + Mass of water
    if soil["M"] is None and soil["Ms"] is not None and soil["Mw"] is not None:
        soil["M"] = soil["Ms"] + soil["Mw"]
        print("M =", soil["M"], "kg")

    # Mass of solids = Total mass - Mass of water
    if soil["Ms"] is None and soil["M"] is not None and soil["Mw"] is not None:
        soil["Ms"] = soil["M"] - soil["Mw"]
        print("Ms =", soil["Ms"], "kg")

    # Mass of water = Total mass - Mass of solids
    if soil["Mw"] is None and soil["M"] is not None and soil["Ms"] is not None:
        soil["Mw"] = soil["M"] - soil["Ms"]
        print("Mw =", soil["Mw"], "kg")

    # Void ratio and porosity relationship
    if soil["e"] is None and soil["n"] is not None:
        soil["e"] = soil["n"] / (1 - soil["n"])
        print("e =", soil["e"])

    if soil["n"] is None and soil["e"] is not None:
        soil["n"] = soil["e"] / (1 + soil["e"])
        print("n =", soil["n"])

    # Void ratio = Volume of voids / Volume of solids
    if soil["e"] is None and soil["Vv"] is not None and soil["Vs"] is not None:
        soil["e"] = soil["Vv"] / soil["Vs"]
        print("e =", soil["e"])

    # Volume of voids = Void ratio * Volume of solids
    if soil["Vv"] is None and soil["e"] is not None and soil["Vs"] is not None:
        soil["Vv"] = soil["e"] * soil["Vs"]
        print("Vv =", soil["Vv"], "m³")

    # Volume of solids = Volume of voids / Void ratio
    if soil["Vs"] is None and soil["Vv"] is not None and soil["e"] is not None:
        soil["Vs"] = soil["Vv"] / soil["e"]
        print("Vs =", soil["Vs"], "m³")

    # Porosity = Volume of voids / Total volume
    if soil["n"] is None and soil["Vv"] is not None and soil["V"] is not None:
        soil["n"] = soil["Vv"] / soil["V"]
        print("n =", soil["n"])

    # Volume of voids = Porosity * Total volume
    if soil["Vv"] is None and soil["n"] is not None and soil["V"] is not None:
        soil["Vv"] = soil["n"] * soil["V"]
        print("Vv =", soil["Vv"], "m³")

    # Water content relationship
    # Water content = Mass of water / Mass of solids
    if soil["w"] is None and soil["Mw"] is not None and soil["Ms"] is not None:
        soil["w"] = soil["Mw"] / soil["Ms"]
        print("w =", soil["w"])

    # Mass of water = Water content * Mass of solids
    if soil["Mw"] is None and soil["w"] is not None and soil["Ms"] is not None:
        soil["Mw"] = soil["w"] * soil["Ms"]
        print("Mw =", soil["Mw"], "kg")

    # Mass of solids = Mass of water / Water content
    if soil["Ms"] is None and soil["Mw"] is not None and soil["w"] is not None and soil["w"] > 0:
        soil["Ms"] = soil["Mw"] / soil["w"]
        print("Ms =", soil["Ms"], "kg")

    # Degree of saturation relationship
    # Degree of saturation = Volume of water / Volume of voids
    if soil["S"] is None and soil["Vw"] is not None and soil["Vv"] is not None and soil["Vv"] > 0:
        soil["S"] = soil["Vw"] / soil["Vv"]
        print("S =", soil["S"])

    # Volume of water = Degree of saturation * Volume of voids
    if soil["Vw"] is None and soil["S"] is not None and soil["Vv"] is not None:
        soil["Vw"] = soil["S"] * soil["Vv"]
        print("Vw =", soil["Vw"], "m³")

    # Relationship between S, e, w, and Gs
    # S = w*Gs/e
    if soil["S"] is None and soil["w"] is not None and soil["Gs"] is not None and soil["e"] is not None and soil["e"] > 0:
        soil["S"] = (soil["w"] * soil["Gs"]) / soil["e"]
        print("S =", soil["S"])

    # w = S*e/Gs
    if soil["w"] is None and soil["S"] is not None and soil["e"] is not None and soil["Gs"] is not None and soil["Gs"] > 0:
        soil["w"] = (soil["S"] * soil["e"]) / soil["Gs"]
        print("w =", soil["w"])

    # e = w*Gs/S
    if soil["e"] is None and soil["w"] is not None and soil["Gs"] is not None and soil["S"] is not None and soil["S"] > 0:
        soil["e"] = (soil["w"] * soil["Gs"]) / soil["S"]
        print("e =", soil["e"])

    # Density relationships
    # Density of solids = Mass of solids / Volume of solids
    if soil["rho_s"] is None and soil["Ms"] is not None and soil["Vs"] is not None and soil["Vs"] > 0:
        soil["rho_s"] = soil["Ms"] / soil["Vs"]
        print("ρs =", soil["rho_s"], "kg/m³")

    # Specific gravity = Density of solids / Density of water
    if soil["Gs"] is None and soil["rho_s"] is not None and soil["rho_w"] is not None and soil["rho_w"] > 0:
        soil["Gs"] = soil["rho_s"] / soil["rho_w"]
        print("Gs =", soil["Gs"])

    # Density of solids = Specific gravity * Density of water
    if soil["rho_s"] is None and soil["Gs"] is not None and soil["rho_w"] is not None:
        soil["rho_s"] = soil["Gs"] * soil["rho_w"]
        print("ρs =", soil["rho_s"], "kg/m³")

    # Bulk density = Total mass / Total volume
    if soil["rho"] is None and soil["M"] is not None and soil["V"] is not None and soil["V"] > 0:
        soil["rho"] = soil["M"] / soil["V"]
        print("ρ =", soil["rho"], "kg/m³")

    # Dry density = Mass of solids / Total volume
    if soil["rho_d"] is None and soil["Ms"] is not None and soil["V"] is not None and soil["V"] > 0:
        soil["rho_d"] = soil["Ms"] / soil["V"]
        print("ρd =", soil["rho_d"], "kg/m³")

    # Bulk density = Dry density * (1 + water content)
    if soil["rho"] is None and soil["rho_d"] is not None and soil["w"] is not None:
        soil["rho"] = soil["rho_d"] * (1 + soil["w"])
        print("ρ =", soil["rho"], "kg/m³")

    # Dry density = Bulk density / (1 + water content)
    if soil["rho_d"] is None and soil["rho"] is not None and soil["w"] is not None:
        soil["rho_d"] = soil["rho"] / (1 + soil["w"])
        print("ρd =", soil["rho_d"], "kg/m³")

    # Water content = (Bulk density / Dry density) - 1
    if soil["w"] is None and soil["rho"] is not None and soil["rho_d"] is not None and soil["rho_d"] > 0:
        soil["w"] = (soil["rho"] / soil["rho_d"]) - 1
        print("w =", soil["w"])

    # Dry density = Gs * rho_w / (1 + e)
    if soil["rho_d"] is None and soil["Gs"] is not None and soil["rho_w"] is not None and soil["e"] is not None:
        soil["rho_d"] = (soil["Gs"] * soil["rho_w"]) / (1 + soil["e"])
        print("ρd =", soil["rho_d"], "kg/m³")

    # Void ratio = (Gs * rho_w / rho_d) - 1
    if soil["e"] is None and soil["Gs"] is not None and soil["rho_w"] is not None and soil["rho_d"] is not None and soil["rho_d"] > 0:
        soil["e"] = (soil["Gs"] * soil["rho_w"] / soil["rho_d"]) - 1
        print("e =", soil["e"])

    # Gs = (rho_d * (1 + e)) / rho_w
    if soil["Gs"] is None and soil["rho_d"] is not None and soil["e"] is not None and soil["rho_w"] is not None and soil["rho_w"] > 0:
        soil["Gs"] = (soil["rho_d"] * (1 + soil["e"])) / soil["rho_w"]
        print("Gs =", soil["Gs"])

    # Complex density relationship
    # ρ = (Gs * (1 + w) / (1 + e)) * ρw
    if soil["rho"] is None and soil["Gs"] is not None and soil["w"] is not None and soil["e"] is not None and soil["rho_w"] is not None:
        soil["rho"] = (soil["Gs"] * (1 + soil["w"]) / (1 + soil["e"])) * soil["rho_w"]
        print("ρ =", soil["rho"], "kg/m³")

    # e = ((Gs * (1 + w) * ρw) / ρ) - 1
    if soil["e"] is None and soil["Gs"] is not None and soil["w"] is not None and soil["rho"] is not None and soil["rho_w"] is not None and soil["rho"] > 0:
        soil["e"] = ((soil["Gs"] * (1 + soil["w"]) * soil["rho_w"]) / soil["rho"]) - 1
        print("e =", soil["e"])

    # Unit weight relationships
    # Unit weight = Bulk density * g / 1000 (convert to kN/m³)
    if soil["gamma"] is None and soil["rho"] is not None:
        soil["gamma"] = soil["rho"] * 9.81 / 1000
        print("γ =", soil["gamma"], "kN/m³")

    # Bulk density = Unit weight * 1000 / g
    if soil["rho"] is None and soil["gamma"] is not None:
        soil["rho"] = soil["gamma"] * 1000 / 9.81
        print("ρ =", soil["rho"], "kg/m³")

    # Saturated unit weight calculation
    # γsat = ((Gs + e) / (1 + e)) * γw
    if soil["gamma_sat"] is None and soil["Gs"] is not None and soil["e"] is not None and soil["gamma_w"] is not None:
        soil["gamma_sat"] = ((soil["Gs"] + soil["e"]) / (1 + soil["e"])) * soil["gamma_w"]
        print("γsat =", soil["gamma_sat"], "kN/m³")

    # Buoyant unit weight calculations
    # γ' = γsat - γw
    if soil["gamma_prime"] is None and soil["gamma_sat"] is not None and soil["gamma_w"] is not None:
        soil["gamma_prime"] = soil["gamma_sat"] - soil["gamma_w"]
        print("γ' =", soil["gamma_prime"], "kN/m³")

    # γ' = ((Gs - 1) / (1 + e)) * γw
    if soil["gamma_prime"] is None and soil["Gs"] is not None and soil["e"] is not None and soil["gamma_w"] is not None:
        soil["gamma_prime"] = ((soil["Gs"] - 1) / (1 + soil["e"])) * soil["gamma_w"]
        print("γ' =", soil["gamma_prime"], "kN/m³")

    # Relative density calculation
    # ID = ((emax - e) / (emax - emin)) * 100
    if soil["ID"] is None and soil["e"] is not None and soil["e_max"] is not None and soil["e_min"] is not None and (soil["e_max"] - soil["e_min"]) > 0:
        soil["ID"] = ((soil["e_max"] - soil["e"]) / (soil["e_max"] - soil["e_min"])) * 100
        print("ID =", soil["ID"], "%")

    # e = emax - (ID / 100) * (emax - emin)
    if soil["e"] is None and soil["ID"] is not None and soil["e_max"] is not None and soil["e_min"] is not None:
        soil["e"] = soil["e_max"] - (soil["ID"] / 100) * (soil["e_max"] - soil["e_min"])
        print("e =", soil["e"])

    # Sr = w*Gs/e
    if soil["S"] is None and soil["w"] is not None and soil["Gs"] is not None and soil["e"] is not None and soil["e"] > 0:
        soil["S"] = (soil["w"] * soil["Gs"]) / soil["e"]
        print("Sr =", soil["S"])

    # e*Sr = w*Gs
    if soil["e"] is None and soil["S"] is not None and soil["w"] is not None and soil["Gs"] is not None:
        soil["e"] = (soil["w"] * soil["Gs"]) / soil["S"]
        print("e =", soil["e"])

print("\nSummary of soil properties:")
for key, value in sorted(soil.items()):
    if value is not None:
        if key == "Mw":
            print("Mw = " + str(value) + " kg")
        elif key == "w":
            print("w = " + str(value))
        elif key == "e":
            print("e = " + str(value))
        elif key == "rho_s":
            print("ρs = " + str(value) + " kg/m³")
        elif key == "rho":
            print("ρ = " + str(value) + " kg/m³")
        elif key == "rho_d":
            print("ρd = " + str(value) + " kg/m³")
        elif key == "gamma":
            print("γ = " + str(value) + " kN/m³")
        elif key == "gamma_sat":
            print("γsat = " + str(value) + " kN/m³")
        elif key == "gamma_prime":
            print("γ' = " + str(value) + " kN/m³")
        elif key == "n":
            print("n = " + str(value))
        elif key == "Vv":
            print("Vv = " + str(value) + " m³")
        elif key == "Vw":
            print("Vw = " + str(value) + " m³")
        elif key == "Va":
            print("Va = " + str(value) + " m³")
        elif key == "Vs":
            print("Vs = " + str(value) + " m³")
print("Don't be retarded, use as a guide only")