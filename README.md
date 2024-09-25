# Program Description

This Python script processes an ORCA `.out` file to extract and analyze temperature-dependent magnetic susceptibility tensors. The program specifically focuses on calculating various magnetic properties such as traceless tensors, eigenvalues, axiality, rhombicity, relative rhombicity, and isotropy for different temperature ranges.

# Key Features

1. Parsing ORCA Output: The script reads the magnetic susceptibility tensors from ORCA's output file, which contains tensors for various temperatures.
2. Unit Conversion: It converts the susceptibility tensors to appropriate units using the temperature-dependent conversion factor.
3. Magnetic Property Calculations:
    - Traceless Tensor: The program calculates the traceless part of the susceptibility tensor from ORCA tensor.
    - Eigenvalues are computed and sorted in Mehring order by absolute value.
    - Axiality (∆χ<sub>ax</sub>) & Rhombicity (∆χ<sub>rh</sub>) of magnetic susceptibility (unit in m<sup>3</sup>): The script computes these properties using two different methods.
      - Method 1 : ∆χ<sub>ax</sub> = 3/2 * χ<sub>zz</sub> and ∆χ<sub>rh</sub> = (χ<sub>xx</sub> - χ<sub>yy</sub>) / 2
      - Method 2 : ∆χ<sub>ax</sub> = χ<sub>zz</sub> - ((χ<sub>xx</sub> + χ<sub>yy</sub>))/2 and ∆χ<sub>rh</sub> = χ<sub>xx</sub> - χ<sub>yy</sub>
    - Relative Rhombicity: A relative measure of rhombicity is also calculated.
      - abs((χ<sub>xx</sub> - χ<sub>yy</sub>)/χ<sub>xx</sub>)
    - Isotropy: The isotropic value of the susceptibility tensor is derived.
4. Temperature Range Selection: The user can specify a range of temperatures for which the calculations should be performed.
5. Result Export: The calculated properties are saved into a user-specified `.txt` file for further analysis.

# Usage

The user inputs the path to the ORCA `.out` file, selects the desired temperature range, and specifies the output file location. The results are saved in a structured format in a text file.
