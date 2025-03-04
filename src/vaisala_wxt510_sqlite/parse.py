import re


def parse_response(response) -> dict:
    """
    Parse the data message from the Vaisala WXT510.

    Args:
        response (str): The response string from the WXT510.

    Returns:
        dict: A dictionary containing the parsed wind data parameters.
    """
    full_name_mapping = {
        'Dn': 'wind_direction_minimum',
        'Dm': 'wind_direction_average',
        'Dx': 'wind_direction_maximum',
        'Sn': 'wind_speed_minimum',
        'Sm': 'wind_speed_average',
        'Sx': 'wind_speed_maximum',
        'Pa': 'air_pressure',
        'Ta': 'air_temperature',
        'Tp': 'internal_temperature',
        'Ua': 'relative_humidity',
        'Rc': 'rain_accumulation',
        'Rd': 'rain_duration',
        'Ri': 'rain_intensity',
        'Rp': 'rain_peak_intensity',
        'Hc': 'hail_accumulation',
        'Hd': 'hail_duration',
        'Hi': 'hail_intensity',
        'Hp': 'hail_peak_intensity',
        'Th': 'heating_temperature',
        'Vh': 'heating_voltage',
        'Vs': 'supply_voltage',
        'Vr': 'reference_voltage',
    }

    # Remove the <cr><lf> terminator if present
    response = response.strip()
    
    # Split the response into components
    data_parts = str(response).split(',')

    # Initialize a dictionary to hold the parsed data
    output_data = {}

    # Parse each part of the response
    for part in data_parts:
        if '=' in part:
            key, value = part.split('=')
            
            # Strip non-numeric characters from the value
            numeric_value = re.sub(r'[^\d.-]+', '', value)
            
            # Convert to float or int
            if numeric_value:
                numeric_value = float(numeric_value) if '.' in numeric_value else int(numeric_value)
                output_data[full_name_mapping[key]] = numeric_value

    return output_data

