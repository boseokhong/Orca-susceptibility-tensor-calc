import numpy as np

def parse_orca_output(file_path):
    """Extracts temperature-dependent susceptibility tensors from ORCA output (.out) file"""
    with open(file_path, 'r') as f:
        lines = f.readlines()

    tensors = {}
    current_temp = None

    # Locate the SOC CORRECTED MAGNETIZATION AND/OR SUSCEPTIBILITY section
    for i, line in enumerate(lines):
        if "TEMPERATURE/K:" in line:
            current_temp = float(line.split()[-1])
        if "Tensor in molecular frame" in line:
            tensor = []
            # Extract the 3x3 matrix of the susceptibility tensor
            for j in range(3):
                tensor.append([float(x) for x in lines[i + 1 + j].split()])
            tensors[current_temp] = np.array(tensor)

    return tensors

def convert_chi_tensor(chi_tensor, temperature):
    """Converts susceptibility tensor units"""
    avogadro_number = 6.02214129e23
    factor = (4 * np.pi * 1e24) / (avogadro_number * temperature)
    return chi_tensor * factor

def calculate_traceless_tensor(chi_tensor):
    """Calculates the traceless part of the susceptibility tensor"""
    trace = np.trace(chi_tensor) / 3.0  # Average diagonal element
    traceless_tensor = chi_tensor - np.eye(3) * trace  # Compute traceless tensor
    return traceless_tensor

def calculate_eigenvalues(chi_tensor):
    """Calculates eigenvalues, axiality, and rhombicity from the susceptibility tensor"""
    traceless_tensor = calculate_traceless_tensor(chi_tensor)
    
    # Compute eigenvalues of the traceless tensor
    eigvals, _ = np.linalg.eigh(traceless_tensor)

    # Sort in Mehring order (by absolute value, smallest to largest)
    idx = np.argsort(np.abs(eigvals))
    eigvals = eigvals[idx]

    # Axiality and Rhombicity computed in two different ways
    # Method 1
    ax_method1 = 3 * eigvals[2] / 2
    rh_method1 = (eigvals[0] - eigvals[1]) / 2
    
    # Method 2
    ax_method2 = eigvals[2] - ((eigvals[0] + eigvals[1]) / 2)
    rh_method2 = eigvals[0] - eigvals[1]
    
    # Relative Rhombicity calculation
    rh_rel = abs((eigvals[0] - eigvals[1]) / eigvals[0])
    
    # Isotropy (iso) calculation
    trace = np.trace(chi_tensor)
    iso = (trace / 3) * 1e-30  # Unit conversion

    return traceless_tensor, eigvals, ax_method1, rh_method1, ax_method2, rh_method2, rh_rel, iso

def process_orca_file(file_path, min_temp, max_temp):
    """Parses the ORCA file and computes tensors for the given temperature range"""
    tensors = parse_orca_output(file_path)
    
    results = []
    for temp, chi_tensor in tensors.items():
        if min_temp <= temp <= max_temp:
            # Convert susceptibility tensor units
            chi_tensor_converted = convert_chi_tensor(chi_tensor, temp)
            traceless_tensor, eigvals, ax1, rh1, ax2, rh2, rh_rel, iso = calculate_eigenvalues(chi_tensor_converted)
            ax1_m = ax1 * 1e-30  # Convert Axiality Method 1 units
            rh1_m = rh1 * 1e-30  # Convert Rhombicity Method 1 units
            ax2_m = ax2 * 1e-30  # Convert Axiality Method 2 units
            rh2_m = rh2 * 1e-30  # Convert Rhombicity Method 2 units
            results.append((temp, traceless_tensor, eigvals, ax1_m, rh1_m, ax2_m, rh2_m, rh_rel, iso))

    return results

def save_results_to_txt(results, output_file):
    """Saves the calculated results to a .txt file"""
    with open(output_file, 'w') as f:
        for temp, traceless_tensor, eigvals, ax1, rh1, ax2, rh2, rh_rel, iso in results:
            f.write(f"Temperature: {temp} K\n")
            f.write(f"Traceless Tensor (cm³*K/mol):\n")
            np.savetxt(f, traceless_tensor, fmt="%.6f")
            f.write(f"Eigenvalues (Mehring order): {eigvals}\n")  # Output eigenvalues in Mehring order
            f.write(f"Axiality (ax) Method 1: {ax1:.6e} m³\n")
            f.write(f"Rhombicity (rh) Method 1: {rh1:.6e} m³\n")
            f.write(f"Axiality (ax) Method 2: {ax2:.6e} m³\n")
            f.write(f"Rhombicity (rh) Method 2: {rh2:.6e} m³\n")
            f.write(f"Relative Rhombicity (rh_rel): {rh_rel:.6e}\n")
            f.write(f"Isotropy (iso): {iso:.6e} m³\n")
            f.write("\n")

def main():
    # Input the file path and temperature range
    file_path = input("Enter the path to the ORCA .out file: ")  # Input ORCA .out file path
    min_temp = float(input("Enter minimum temperature (K): "))
    max_temp = float(input("Enter maximum temperature (K): "))
    output_file = input("Enter the path to save the output (e.g., output.txt): ")  # Output file path
    
    results = process_orca_file(file_path, min_temp, max_temp)

    # Display results and save to file
    print(f"Results for temperature range: {min_temp} - {max_temp} K")
    save_results_to_txt(results, output_file)
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main()
