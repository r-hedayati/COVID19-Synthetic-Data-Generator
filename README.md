# COVID19Synthetic

This repository generates synthetic COVID-19 patient data for research and educational purposes. It uses the [Faker](https://faker.readthedocs.io/) library to simulate demographic and symptom data based on WHO-reported probabilities.

## Features
- Generates synthetic patient records with realistic demographics
- Simulates COVID-19 symptoms and test results
- Outputs data as a CSV file for use in machine learning or analysis

## Usage
1. **Install dependencies:**
   ```bash
   pip install pandas numpy faker
   ```
2. **Run the generator:**
   ```bash
   python dataGenerator.py
   ```
3. **Output:**
   - The script creates `positiveCases.csv` with synthetic data.

## Customization
- Change `n_people` in `dataGenerator.py` to adjust the number of records.
- Modify symptom probabilities or add new symptoms as needed.

## License
This project is licensed under the MIT License.

## Disclaimer
This data is synthetic and for demonstration only. It does not represent real patient information.
