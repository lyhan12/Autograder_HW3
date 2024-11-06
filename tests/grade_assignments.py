import unittest

from gradescope_utils.autograder_utils.decorators import weight, number, partial_credit

import os
import pandas as pd
import numpy as np
import requests

import json

from utils import (
        register_local_file, 
        extract_variables, 
        extract_initial_variables, 
        extract_cell_content_and_outputs,
        find_cells_with_text, 
        find_cells_by_indices,
        has_string_in_cell,
        has_string_in_code_cells,
        search_plots_in_extracted_vars,
        search_text_in_extracted_content,
        print_text_and_output_cells,
        print_code_and_output_cells)


class GradeAssignment(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(GradeAssignment, self).__init__(*args, **kwargs)
        self.notebook_path = None

        self.local_files = [
            "Interrogation_Statements.csv",
            "london_weather.csv",
            "Lot_11B.csv",
            "Lot_1B.csv",
            "Lot_6.csv",
            "Medical_Records.csv",
            "Profiles.csv",
            "Regents_Drive_Garage.csv",
            "Witness.csv"
        ]
        for file in self.local_files:
            register_local_file(file)

    @partial_credit(5.0)
    @number("1.1.9")
    def test_1_1_9(self, set_score=None):
        print('')

        begin_cells = find_cells_with_text(self.notebook_path, "**TASK *1.9* (5 points)**")
        begin_cell = begin_cells[0]
        begin_cell_idx = begin_cell['index'] - 1

        end_cells = find_cells_with_text(self.notebook_path, "# Part 2: Data Exploration")
        end_cell = end_cells[0]
        end_cell_idx = end_cell['index']

        cell_vars = extract_variables(self.notebook_path, cell_idx=end_cell_idx - 1)
        figure_list = search_plots_in_extracted_vars(cell_vars)

        if len(figure_list) == 0:
            print("No plots found")
            set_score(0.0)
            return


        # Step 2: Iterate over combinations and calculate scores
        max_score = 0.0
        best_figure = None

        for figure in figure_list:
            data_points = figure["data_points"]
            min_year = min([x for x, y in data_points])
            max_year = max([x for x, y in data_points])
            min_temp = min([y for x, y in data_points])
            max_temp = max([y for x, y in data_points])

            year_in_range = (min_year == 1990 and max_year == 2010)
            temp_in_range = (9.0 <= min_temp <= 11.0) and (11.5 <= max_temp <= 13.5)

            x_label_correct = (figure["x_label"] == "Year")
            y_label_correct = (figure["y_label"] == "Mean Temperature (°C)")
            title_correct = (figure["axis_title"] == "Average Temperature (1990-2010)" or figure["figure_title"] == "Average Temperature (1990-2010)")

            value_correct = (year_in_range and temp_in_range)
            label_correct = sum([x_label_correct, y_label_correct, title_correct]) >= 2

            # Calculate score for this combination
            score = 0.0
            if value_correct:
                score += 5.0
                if not label_correct:
                    score -= 2.0

            # Update max_score and best_combination if current score is higher
            if score > max_score:
                max_score = score
                best_figure = figure

        # Step 3: Print detailed information for the best combination
        if best_figure:
            print(f"Figure {best_figure['fig_index'] + 1}, Axis {best_figure['ax_index'] + 1}, Data Points {best_figure['dp_index'] + 1}")
            print("Min/Max Year: ", min([x for x, y in best_figure["data_points"]]), max([x for x, y in best_figure["data_points"]]))
            print("Min/Max Temp: ", min([y for x, y in best_figure["data_points"]]), max([y for x, y in best_figure["data_points"]]))
            print("X Label: ", best_figure["x_label"])
            print("Y Label: ", best_figure["y_label"])
            print("Figure Title: ", best_figure["figure_title"])
            print("Axis Title: ", best_figure["axis_title"])
            print("Score: ", max_score)

        # Set the highest score obtained
        set_score(max_score)

    @partial_credit(2.0)
    @number("2.1.1")
    def test_2_1_1(self, set_score=None):
        print('')

        begin_cells = find_cells_with_text(self.notebook_path, "**TASK 1.1 (2 Point):**  In the code boxes below")
        begin_cell = begin_cells[0]
        begin_cell_idx = begin_cell['index'] - 1

        end_cells = find_cells_with_text(self.notebook_path, "**TASK 1.2 (1 Point):**  Next,")
        end_cell = end_cells[0]
        end_cell_idx = end_cell['index']
        cell_vars = extract_variables(self.notebook_path, cell_idx=end_cell_idx - 1)

        profiles_df = cell_vars.get("profiles_df", None)
        medical_df = cell_vars.get("medical_df", None)

        profiles_df_gt = pd.read_csv("Profiles.csv")
        medical_df_gt = pd.read_csv("Medical_Records.csv")

        exists_profiles_df = (profiles_df is not None) and (type(profiles_df) == pd.DataFrame)
        exists_medical_df = (medical_df is not None) and (type(medical_df) == pd.DataFrame)

        correct_profiles_df = (profiles_df.equals(profiles_df_gt))
        correct_medical_df = (medical_df.equals(medical_df_gt))

        print("Exists profiles_df: ", exists_profiles_df)
        print("Exists medical_df: ", exists_medical_df)
        print("Equal profiles_df and gt: ", correct_profiles_df)
        print("Equal medical_df and gt: ", correct_medical_df) 



        score = 0.0
        if exists_profiles_df:
            if correct_profiles_df:
                score += 1.0

        if exists_medical_df:
            if correct_medical_df:
                score += 1.0

        set_score(score)

    @partial_credit(1.0)
    @number("2.1.2")
    def test_2_1_2(self, set_score=None):
        print('')

        begin_cells = find_cells_with_text(self.notebook_path, "**TASK 1.2 (1 Point):**  Next,")
        begin_cell = begin_cells[0]
        begin_cell_idx = begin_cell['index'] - 1

        end_cells = find_cells_with_text(self.notebook_path, "**TASK 1.3 (1 Point):**  Next,")
        end_cell = end_cells[0]
        end_cell_idx = end_cell['index']

        cell_texts = extract_cell_content_and_outputs(self.notebook_path, begin_cell_idx, end_cell_idx)

        search_300, _ = search_text_in_extracted_content(cell_texts, "300")
        search_7, _ = search_text_in_extracted_content(cell_texts, "7")


        print("Found 300, 7 : ", search_300 & search_7)

     
        set_score(0.0)
        if search_300 & search_7:
            set_score(1.0)

    @partial_credit(1.0)
    @number("2.1.3")
    def test_2_1_3(self, set_score=None):
        print('')

        begin_cells = find_cells_with_text(self.notebook_path, "**TASK 1.3 (1 Point):**  Next, ")
        begin_cell = begin_cells[0]
        begin_cell_idx = begin_cell['index'] - 1

        end_cells = find_cells_with_text(self.notebook_path, "**TASK 1.4 (1 Point):**  Now,")
        end_cell = end_cells[0]
        end_cell_idx = end_cell['index']

        cell_texts = extract_cell_content_and_outputs(self.notebook_path, begin_cell_idx, end_cell_idx)

        search_ID,_ = search_text_in_extracted_content(cell_texts, "ID")
        search_Name,_ = search_text_in_extracted_content(cell_texts, "Name")
        search_Location_during_crime,_ = search_text_in_extracted_content(cell_texts, "Location_during_crime")
        search_Eye_color,_ = search_text_in_extracted_content(cell_texts, "Eye_color")
        search_Skin_Color,_ = search_text_in_extracted_content(cell_texts, "Skin_Color")
        search_Hair_Color,_ = search_text_in_extracted_content(cell_texts, "Hair_Color")

        print("Found ID: ", search_ID)
        print("Found Name: ", search_Name)
        print("Found Location_during_crime: ", search_Location_during_crime)
        print("Found Eye_color: ", search_Eye_color)
        print("Found Skin_color: ", search_Skin_Color)
        print("Found Hair_color: ", search_Hair_Color)

        set_score(0.0)
        if search_ID & search_Name & search_Location_during_crime & search_Eye_color & search_Skin_Color & search_Hair_Color:
            set_score(1.0)

    @partial_credit(1.0)
    @number("2.1.4")
    def test_2_1_4(self, set_score=None):
        print('')

        begin_cells = find_cells_with_text(self.notebook_path, "**TASK 1.4 (1 Point):**  Now,")
        begin_cell = begin_cells[0]
        begin_cell_idx = begin_cell['index'] - 1

        end_cells = find_cells_with_text(self.notebook_path, "**TASK 1.5 (2 Points):** Utilizing")
        end_cell = end_cells[0]
        end_cell_idx = end_cell['index']

        cell_texts = extract_cell_content_and_outputs(self.notebook_path, begin_cell_idx, end_cell_idx)

        search_object, _ = search_text_in_extracted_content(cell_texts, "object")
        search_dtypes, _ = search_text_in_extracted_content(cell_texts, "dtypes")

        print("Use dtype: ", search_dtypes)
        print("Found object type:", search_object)

        set_score(0.0)
        if search_object or search_dtypes:
            set_score(1.0)


    @partial_credit(2.0)
    @number("2.1.5")
    def test_2_1_5(self, set_score=None):
        print('')

        begin_cells = find_cells_with_text(self.notebook_path, "**TASK 1.5 (2 Points):** Utilizing")
        begin_cell = begin_cells[0]
        begin_cell_idx = begin_cell['index'] - 1

        end_cells = find_cells_with_text(self.notebook_path, "**TASK 1.6 (4 Points):**")
        end_cell = end_cells[0]
        end_cell_idx = end_cell['index']

        cell_vars = extract_variables(self.notebook_path, cell_idx=end_cell_idx - 1)

        profiles_info = cell_vars.get("profiles_info", None)
        medical_info  = cell_vars.get("medical_info", None)

        profiles_df_gt = pd.read_csv("Profiles.csv")
        medical_df_gt = pd.read_csv("Medical_Records.csv")

        profiles_info_gt = profiles_df_gt.count()
        medical_info_gt = medical_df_gt.count()

        print("Exists Profiles Info: ", profiles_info is not None)
        print("Correct Profiles Info Format: ", type(profiles_info) == pd.Series)
        print("Correct Profiles Info Values Correct: ", profiles_info.equals(profiles_info_gt))
        print("Exists Medical Info: ", medical_info is not None)
        print("Correct Medical Info Format: ", type(medical_info) == pd.Series)
        print("Correct Medical Info Values Correct: ", medical_info.equals(medical_info_gt))


        score = 0.0

        if profiles_info is not None:
            if type(profiles_info) == pd.Series:
                if profiles_info.equals(profiles_info_gt):
                    score += 1.0

        if medical_info is not None:
            if type(medical_info) == pd.Series:
                if medical_info.equals(medical_info_gt):
                    score += 1.0

        set_score(score)

    @partial_credit(10.0)
    @number("2.2.1")
    def test_2_2_1(self, set_score=None):
        print('')

        begin_cells = find_cells_with_text(self.notebook_path, "**TASK 2.1 (10 Points):** ")
        begin_cell = begin_cells[0]
        begin_cell_idx = begin_cell['index'] - 1

        end_cells = find_cells_with_text(self.notebook_path, "**TASK 2.2 (5 Points):** Now")
        end_cell = end_cells[0]
        end_cell_idx = end_cell['index']

        cell_vars = extract_variables(self.notebook_path, cell_idx=end_cell_idx - 1)

        medical_df = cell_vars.get("Medical_Records", None)
        if medical_df is None:
            medical_df = cell_vars.get("medical_df", None)

        profiles_df = cell_vars.get("Profiles", None)
        if profiles_df is None:
            profiles_df = cell_vars.get("profiles_df", None)


        def check_date_format(df, column_name):
            correct_format = []
            for date in df[column_name]:
                try:
                    # Check if it can be converted to datetime
                    pd.to_datetime(date, format='%Y-%m-%d', errors='raise')
                    correct_format.append(True)
                except (ValueError, TypeError):
                    correct_format.append(False)
            return correct_format

        Birthday_YYYY_mm_dd = all(check_date_format(medical_df, "Birthday"))

        print("Birthday column has correct format: ", Birthday_YYYY_mm_dd)

        set_score(0.0)
        if Birthday_YYYY_mm_dd:
            set_score(10.0)

    @partial_credit(5.0)
    @number("2.2.2")
    def test_2_2_2(self, set_score=None):
        print('')

        begin_cells = find_cells_with_text(self.notebook_path, "**TASK 2.2 (5 Points):** Now")
        begin_cell = begin_cells[0]
        begin_cell_idx = begin_cell['index'] - 1

        end_cells = find_cells_with_text(self.notebook_path, "**TASK 2.3 (10 Points):** Now that we")
        end_cell = end_cells[0]
        end_cell_idx = end_cell['index']

        cell_vars = extract_variables(self.notebook_path, cell_idx=end_cell_idx - 1)

        profiles_df = cell_vars.get("Profiles", None)
        if profiles_df is None:
            profiles_df = cell_vars.get("profiles_df", None)

        exists_profiles_df = (profiles_df is not None) and (type(profiles_df) == pd.DataFrame)
        has_Age_column = "Age" in profiles_df.columns

        if not has_Age_column:
            medical_df = cell_vars.get("Medical_Records", None)
            if medical_df is None:
                medical_df = cell_vars.get("medical_df", None)

            profiles_df = medical_df
            has_Age_column = "Age" in profiles_df.columns

            print("Dit not define Age in the Profiles dataframe, but in Medical Records dataframe")
            set_score(3.0)
            return


        # Search a row with name "Amanda Brown" and get the age value
        if has_Age_column:
            age_Amanda_Brown = int(profiles_df.loc[profiles_df["Name"] == "Amanda Brown", "Age"].values[0])
            age_Harold_Watkins = int(profiles_df.loc[profiles_df["Name"] == "Harold Watkins", "Age"].values[0])
            age_William_Jones = int(profiles_df.loc[profiles_df["Name"] == "William Jones", "Age"].values[0])
        else:
            age_Amanda_Brown = -1
            age_Harold_Watkins = -1
            age_William_Jones = -1

        age_exact = (age_Amanda_Brown == 28 or age_Amanda_Brown == 29) and (age_Harold_Watkins == 21 or age_Harold_Watkins == 22) and (age_William_Jones == 34)
        age_similar = (27 <= age_Amanda_Brown <= 29) and (20 <= age_Harold_Watkins <= 22) and (33 <= age_William_Jones <= 35)

        print("Has Age column in Profile: ", has_Age_column)
        print("Age_Check_Amanda_Brown (28): ", age_Amanda_Brown)
        print("Age_Check_Harold_Watkins (21): ", age_Harold_Watkins)
        print("Age_Check_William_Jones (34):", age_William_Jones)
        print("Exact Age for Amanda, Harold, William: ", age_exact)
        print("Similar Age for Amanda, Harold, William: ", age_similar)

        score = 0.0
        
        if exists_profiles_df and has_Age_column:
            score += 1.0

            if age_similar:
                score += 2.0

                if age_exact:
                    score += 2.0

        set_score(score)

    @partial_credit(5.0)
    @number("2.3.1")
    def test_2_3_1(self, set_score=None):
        print('')
        begin_cells = find_cells_with_text(self.notebook_path, "**TASK 3.1 (5 Points):**")
        begin_cell = begin_cells[0]
        begin_cell_idx = begin_cell['index'] - 1
        end_cells = find_cells_with_text(self.notebook_path, "**TASK 3.2 (5 Points):**")
        end_cell = end_cells[0]
        end_cell_idx = end_cell['index']
        cell_vars = extract_variables(self.notebook_path, cell_idx=end_cell_idx - 1)
        important_witnesses = cell_vars.get("important_witnesses", None)


        exists_important_witnesses = (important_witnesses is not None) and (type(important_witnesses) == pd.DataFrame)
        
        witness_df = pd.read_csv("Witness.csv")
        profiles_df = pd.read_csv("Profiles.csv")
        second_floor_profiles_df = profiles_df[profiles_df['Location_during_crime'].str.contains('second floor', case=False, na=False)]
        ref_important_witnesses = pd.merge(second_floor_profiles_df[['ID']], witness_df, on='ID', how='inner')

    

        important_witnesses_ids = set(important_witnesses["ID"])
        ref_important_witnesses_ids = set(ref_important_witnesses["ID"])
        
        # Check if sets are equal
        correct_important_witnesses = important_witnesses_ids == ref_important_witnesses_ids
        score = 0.0
        if exists_important_witnesses:
            score += 2.0
            if correct_important_witnesses:
                score += 3
        set_score(score)


    @partial_credit(5.0)
    @number("2.3.2")
    def test_2_3_2(self, set_score=None):
        print('')
        begin_cells = find_cells_with_text(self.notebook_path, "**TASK 3.2 (5 Points):**")
        begin_cell = begin_cells[0]
        begin_cell_idx = begin_cell['index'] - 1
        end_cells = find_cells_with_text(self.notebook_path, "**TASK 3.3 (5 Points):**")
        end_cell = end_cells[0]
        end_cell_idx = end_cell['index']
        cell_vars = extract_variables(self.notebook_path, cell_idx=end_cell_idx - 1)
        potential_eye_colors = cell_vars.get("potential_eye_colors", None)
        exists_potential_eye_colors = (potential_eye_colors is not None)


        expected_eye_colors = {'orange', 'green', 'blue', 'violet'}

        correct_eye_colors = True
        for color in expected_eye_colors:
            if color not in str(potential_eye_colors):
                print(f"Expected eye color {color} not found in potential_eye_colors")
                correct_eye_colors = False


        unique_eye_colors = True
        print("Exists potential_eye_colors: ", exists_potential_eye_colors)
        print("No duplicate values in potential_eye_colors: ", unique_eye_colors)
        print("Correct eye colors found: ", correct_eye_colors)
        score = 0.0
        if exists_potential_eye_colors:
            score += 2.0
            if unique_eye_colors:
                score += 1.5
            if correct_eye_colors:
                score += 1.5
        set_score(score)


    @partial_credit(5.0)
    @number("2.3.3")
    def test_2_3_3(self, set_score=None):
        print('')
        begin_cells = find_cells_with_text(self.notebook_path, "**TASK 3.3 (5 Points):**")
        begin_cell = begin_cells[0]
        begin_cell_idx = begin_cell['index'] - 1
        end_cells = find_cells_with_text(self.notebook_path, "**TASK 3.4 (5 Points):**")
        end_cell = end_cells[0]
        end_cell_idx = end_cell['index']
        cell_vars = extract_variables(self.notebook_path, cell_idx=end_cell_idx - 1)
        potential_hair_colors = cell_vars.get("potential_hair_colors", None)
        exists_potential_hair_colors = (potential_hair_colors is not None)

        expected_hair_colors = {'orange', 'green', 'blue', 'violet'}

        correct_hair_colors = True
        for color in expected_hair_colors:
            if color not in str(potential_hair_colors):
                print(f"Expected hair color {color} not found in potential_hair_colors")
                correct_hair_colors = False

        unique_hair_colors = True

        print("Exists potential_hair_colors: ", exists_potential_hair_colors)
        print("No duplicate values in potential_hair_colors: ", unique_hair_colors)
        print("Correct hair colors found: ", correct_hair_colors)
        score = 0.0

        if exists_potential_hair_colors:
            score += 2.0
            if unique_hair_colors:
                score += 1.5
            if correct_hair_colors:
                score += 1.5
        set_score(score)

    @partial_credit(5.0)
    @number("2.3.4")
    def test_2_3_4(self, set_score=None):
        print('')
        begin_cells = find_cells_with_text(self.notebook_path, "**TASK 3.4 (5 Points):**")
        begin_cell = begin_cells[0]
        begin_cell_idx = begin_cell['index'] - 1
        end_cells = find_cells_with_text(self.notebook_path, "**TASK 3.5 (5 Points):**")
        end_cell = end_cells[0]
        end_cell_idx = end_cell['index']
        cell_vars = extract_variables(self.notebook_path, cell_idx=end_cell_idx - 1)

        potential_skin_colors = cell_vars.get("potential_skin_colors", None)
        exists_potential_skin_colors = (potential_skin_colors is not None)

        expected_skin_colors = {'red', 'green', 'orange'}

        correct_skin_colors = True
        for color in expected_skin_colors:
            if color not in str(potential_skin_colors):
                print(f"Expected skin color {color} not found in potential_skin_colors")
                correct_skin_colors = False

        unique_skin_colors = True
        print("Exists potential_skin_colors: ", exists_potential_skin_colors)
        print("No duplicate values in potential_skin_colors: ", unique_skin_colors)
        print("Correct skin colors found: ", correct_skin_colors)
        score = 0.0
        if exists_potential_skin_colors:
            score += 2.0
            if unique_skin_colors:
                score += 1.5
                if correct_skin_colors:
                    score += 1.5
        set_score(score)

    @partial_credit(5.0)
    @number("2.3.5")
    def test_2_3_5(self, set_score=None):
        print('')

        begin_cells = find_cells_with_text(self.notebook_path, "**TASK 3.5 (5 Points):**")
        begin_cell = begin_cells[0]
        begin_cell_idx = begin_cell['index'] - 1

        end_cells = find_cells_with_text(self.notebook_path, "**TASK 3.6 (5 Points):**")
        end_cell = end_cells[0]
        end_cell_idx = end_cell['index']

        cell_vars = extract_variables(self.notebook_path, cell_idx=end_cell_idx - 1)
        smallest_height_cell = cell_vars.get("smallest_height", cell_vars.get("min_height", None))
        largest_height_cell = cell_vars.get("largest_height", cell_vars.get("max_height", None))

        exists_s_df = True if smallest_height_cell is not None else False
        exists_l_df = True if largest_height_cell is not None else False


        case_1 = smallest_height_cell == 150
        case_2 = largest_height_cell == 170

        total_score = 0.0
        if exists_s_df:
            total_score += 1.0
        if exists_l_df:
            total_score += 1.0

        if case_1:
            total_score += 1.5
        if case_2:
            total_score += 1.5

        print("Found df of smallest_height: ", exists_s_df)
        print("Found df of largest_height: ", exists_l_df)
        print("smallest_height val: ", case_1)
        print("largest_height val: ", case_2)

        set_score(total_score)

    @partial_credit(5.0)
    @number("2.3.6")
    def test_2_3_6(self, set_score=None):
        print('')

        begin_cells = find_cells_with_text(self.notebook_path, "**TASK 3.6 (5 Points):**")
        begin_cell = begin_cells[0]
        begin_cell_idx = begin_cell['index'] - 1

        end_cells = find_cells_with_text(self.notebook_path, "## Q4) Parking Permit")
        end_cell = end_cells[0]
        end_cell_idx = end_cell['index']

        cell_vars = extract_variables(self.notebook_path, cell_idx=end_cell_idx - 1)
        smallest_age_cell = cell_vars.get("smallest_age", cell_vars.get("min_age", None))
        largest_age_cell = cell_vars.get("largest_age", cell_vars.get("max_age", None))

        exists_s_df = True if smallest_age_cell is not None else False
        exists_l_df = True if largest_age_cell is not None else False


        case_1 = smallest_age_cell == 21
        case_2 = largest_age_cell == 35

        total_score = 0.0
        if exists_s_df:
            total_score += 1.0
        if exists_l_df:
            total_score += 1.0

        if case_1:
            total_score += 1.5
        if case_2:
            total_score += 1.5

        print("Found df of smallest_age: ", exists_s_df)
        print("Found df of largest_age: ", exists_l_df)
        print("smallest_age val: ", case_1)
        print("largest_age val: ", case_2)

        set_score(total_score)


# EDITS by Aishani
    @partial_credit(2.0)
    @number("2.4.1")
    def test_2_4_1(self, set_score=None):
        print('')

        expected_vars = ["lot_11B", "lot_1B", "lot_6", "regents_garage", "interrogation_df"]
        
        begin_cells = find_cells_with_text(self.notebook_path, "**TASK 4.1 (2 Points)**:")
        begin_cell = begin_cells[0]
        begin_cell_idx = begin_cell['index'] - 1

        end_cells = find_cells_with_text(self.notebook_path, "**TASK 4.2 (5 Points):**")
        end_cell = end_cells[0]
        end_cell_idx = end_cell['index']
        
        cell_vars = extract_variables(self.notebook_path, cell_idx=end_cell_idx - 1)

        all_vars_loaded = all(var in cell_vars and cell_vars.get(var) is not None for var in expected_vars)
        print("Loaded variables: ", {var: cell_vars.get(var) is not None for var in expected_vars})
        
        total_score = 2.0 if all_vars_loaded else 0.0
        set_score(total_score)



    @partial_credit(5.0)
    @number("2.4.2")
    def test_2_4_2(self, set_score=None):

        begin_cells = find_cells_with_text(self.notebook_path, "**TASK 4.2 (5 Points):**")
        begin_cell = begin_cells[0]
        begin_cell_idx = begin_cell['index'] - 1

        end_cells = find_cells_with_text(self.notebook_path, "**TASK 5.1(5 Points):**")
        end_cell = end_cells[0]
        end_cell_idx = end_cell['index']

        cell_texts = extract_cell_content_and_outputs(self.notebook_path, begin_cell_idx, end_cell_idx)

        search_11b, _ = search_text_in_extracted_content(cell_texts, "11b")

        search_hex, _ = search_text_in_extracted_content(cell_texts, "hex")
        search_53, _ = search_text_in_extracted_content(cell_texts, "53")
        search_083, _ = search_text_in_extracted_content(cell_texts, "083")
        search_s, _ = search_text_in_extracted_content(cell_texts, "s")
        search_ascii, _ = search_text_in_extracted_content(cell_texts, "ascii")
        search_single, _ = search_text_in_extracted_content(cell_texts, "ascii")

        search_01000101, _ = search_text_in_extracted_content(cell_texts, "01000101")
        search_45,_ = search_text_in_extracted_content(cell_texts, "45")
        search_E,_ = search_text_in_extracted_content(cell_texts, "E")
        search_east,_ = search_text_in_extracted_content(cell_texts, "east")


        answer_correct = search_11b
        explained_single_leveled = search_hex or search_53 or search_083 or search_s or search_ascii or search_single
        explained_east = search_01000101 or search_45 or search_E or search_east

        print("Answer correct (11B): ", answer_correct)
        print("Explained about single leveld parking garage(hex, 53, 083, s, ...):", explained_single_leveled)
        print("Explained that the garage is east of the stadium (01000101, 45, E, east):", explained_east)

        total_score = 0.0
        if answer_correct:
            total_score += 2.5
        if explained_single_leveled or explained_east:
            total_score += 1.0

            if explained_single_leveled and explained_east:
                total_score += 1.5


        set_score(total_score)





    @partial_credit(5.0)
    @number("2.5.1")
    def test_2_5_1(self, set_score=None):
        print('')
        
        begin_cells = find_cells_with_text(self.notebook_path, "**TASK 5.1(5 Points):**")
        begin_cell = begin_cells[0]
        begin_cell_idx = begin_cell['index'] - 1

        end_cells = find_cells_with_text(self.notebook_path, "**TASK 5.2 (1 Points):**")
        end_cell = end_cells[0]
        end_cell_idx = end_cell['index']


        cell_vars = extract_variables(self.notebook_path, cell_idx=end_cell_idx - 1)
        culprit_var = cell_vars.get("culprit", None)

        # pandas dataframe
        # if type(culprit_var) == pd.DataFrame:
        #     culprit_var = culprit_var["Name"].values[0]

        culprit = str(culprit_var) if culprit_var is not None else None

        total_score = 0.0
        expected_culprit = "Arthur Gutierrez"

        if culprit is not None:
            if expected_culprit in culprit:
                total_score += 5.0
            else:
                total_score += 3.0 

        print("Culprit name found: ", culprit)
        print("Total Score: ", total_score)

        set_score(total_score)
