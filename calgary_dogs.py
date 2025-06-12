# calgary_dogs.py
# Edmund Yu
#
# A terminal-based application for computing and printing statistics based on given input.
# Detailed specifications are provided via the Assignment 4 README file.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc.
# You may import any modules from the standard Python library.
# Remember to include docstrings and comments.
import pandas as pd


def main():
    """
    Main function that runs the dog breed analysis program.
    Loads Calgary dog breed data, prompts user for breed input with validation,
    and performs analysis including yearly percentages,
    total registrations, and popular months for the selected breed.

    The function uses pandas DataFrame operations including multi-indexing,
    IndexSlice, masking, and groupby operations.

    Parameters:
        None

    Returns:
        None
    """

    # Import data here
    df = pd.read_excel('CalgaryDogBreeds.xlsx')
    breed_year_indexed_dataframe = df.set_index(['Breed', 'Year'])
    valid_breed_names = breed_year_indexed_dataframe.index.get_level_values(
        0).unique().str.upper()

    print("ENSF 692 Dogs of Calgary")

    # User input stage
    while True:
        try:
            user_breed_input = input("Please enter a dog breed: ").upper()

            if user_breed_input not in valid_breed_names:
                raise KeyError(
                    "Dog breed not found in data. Please try again.")
            else:
                break
        except KeyError as e:
            print(e)

    # Data anaylsis stage
    idx = pd.IndexSlice
    # Select the data for the user input breed
    selected_breed_data = breed_year_indexed_dataframe.loc[idx[user_breed_input, :], :]
    # Check if the breed exists in the data
    selected_breed_years = selected_breed_data.index.get_level_values(
        'Year').unique().tolist()

    if selected_breed_years:
        years_str = ' '.join(map(str, selected_breed_years))
        print(
            f"The {user_breed_input} was found in the top breeds for years: {years_str}")
    else:
        print(f"The {user_breed_input} was never the top breed in any year.")

    # Calculate total registrations for the selected breed
    selected_breed_total_registrations = selected_breed_data['Total'].sum()
    print(
        f"There have been {selected_breed_total_registrations} {user_breed_input} dogs registered total.")

    # Calculate yearly percentages for the selected breed
    selected_breed_yearly_totals = selected_breed_data.groupby('Year')[
        'Total'].sum()
    total_by_year = df.groupby('Year')['Total'].sum()
    breed_yearly_percentages = (
        (selected_breed_yearly_totals / total_by_year) * 100)

    for year, percentage in breed_yearly_percentages.items():
        print(
            f"The {user_breed_input} was {percentage:.6f}% of top breeds in {year}.")

    # Calculate overall percentage of the selected breed across all years
    selected_breed_total_all_years = selected_breed_yearly_totals.sum()
    all_breeds_total_all_years = total_by_year.sum()
    breed_overall_percentage = (
        selected_breed_total_all_years / all_breeds_total_all_years) * 100
    print(
        f"The {user_breed_input} was {breed_overall_percentage:.6f}% of top breeds across all years.")

    # Find the most popular month(s) for the selected breed
    selected_breed_monthly_totals = selected_breed_data.groupby('Month')[
        'Total'].sum()
    monthly_registrations_mean = selected_breed_monthly_totals.mean()
    above_average_months_mask = selected_breed_monthly_totals >= monthly_registrations_mean
    popular_months_list = selected_breed_monthly_totals[above_average_months_mask].index.tolist(
    )
    if popular_months_list:
        print(
            f"Most popular month(s) for {user_breed_input} dogs: {' '.join(popular_months_list)}")
    else:
        print(f"The {user_breed_input} was never registered in any month.")


if __name__ == '__main__':
    main()
