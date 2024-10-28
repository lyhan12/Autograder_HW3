import unittest

from gradescope_utils.autograder_utils.decorators import weight, number, partial_credit

import os
import pandas as pd
import numpy as np
import requests

from utils import (
        register_local_file, 
        extract_variables, 
        extract_initial_variables, 
        find_cells_with_text, 
        find_cells_by_indices,
        has_string_in_cell,
        has_string_in_code_cells,
        extract_cell_content_and_outputs,
        search_in_extracted_content,
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

        search_300, _ = search_in_extracted_content(cell_texts, "300")
        search_7, _ = search_in_extracted_content(cell_texts, "7")


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

        search_ID,_ = search_in_extracted_content(cell_texts, "ID")
        search_Name,_ = search_in_extracted_content(cell_texts, "Name")
        search_Location_during_crime,_ = search_in_extracted_content(cell_texts, "Location_during_crime")
        search_Eye_color,_ = search_in_extracted_content(cell_texts, "Eye_color")
        search_Skin_Color,_ = search_in_extracted_content(cell_texts, "Skin_Color")
        search_Hair_Color,_ = search_in_extracted_content(cell_texts, "Hair_Color")

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

        search_object, _ = search_in_extracted_content(cell_texts, "object")
        search_dtypes, _ = search_in_extracted_content(cell_texts, "dtypes")

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

        # Search a row with name "Amanda Brown" and get the age value
        if has_Age_column:
            age_Amanda_Brown = int(profiles_df.loc[profiles_df["Name"] == "Amanda Brown", "Age"].values[0])
            age_Harold_Watkins = int(profiles_df.loc[profiles_df["Name"] == "Harold Watkins", "Age"].values[0])
            age_William_Jones = int(profiles_df.loc[profiles_df["Name"] == "William Jones", "Age"].values[0])
        else:
            age_Amanda_Brown = -1
            age_Harold_Watkins = -1
            age_William_Jones = -1

        age_exact = (age_Amanda_Brown == 28) and (age_Harold_Watkins == 21) and (age_William_Jones == 34)
        age_similar = (27 <= age_Amanda_Brown <= 29) and (20 <= age_Harold_Watkins <= 22) and (33 <= age_William_Jones <= 35)

        print("Has Age column in Profile: ", has_Age_column)
        print("Age_Check_Amanda_Brown (28): ", age_Amanda_Brown)
        print("Age_Check_Harold_Watkins (21): ", age_Harold_Watkins)
        print("Age_Check_William_Jones (45):", age_William_Jones)
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
        expected_hair_colors = {'orange', 'green', 'blue', 'violet'}
        exists_potential_hair_colors = (potential_hair_colors is not None) and (type(potential_hair_colors) == list)
        unique_hair_colors = len(potential_hair_colors) == len(set(potential_hair_colors))
        correct_hair_colors = set(potential_hair_colors) == expected_hair_colors
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
        expected_skin_colors = {'red', 'green', 'orange'}
        exists_potential_skin_colors = (potential_skin_colors is not None) and (type(potential_skin_colors) == list)
        unique_skin_colors = len(potential_skin_colors) == len(set(potential_skin_colors))
        correct_skin_colors = set(potential_skin_colors) == expected_skin_colors
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





 #    @partial_credit(1.0)
 #    @number("2.2")
 #    def test_linear_thingz_1_1_1(self, set_score=None):
 #        print('')


 #        begin_cells = find_cells_with_text(self.notebook_path, "**1.1.1:** *In one line of code and **using only one function**")
 #        begin_cell = begin_cells[0]
 #        begin_cell_idx = begin_cell['index']

 #        end_cells = find_cells_with_text(self.notebook_path, "**1.1.2:** *In one line of code, list the **names** of all the **features** in the dataframe.*")
 #        end_cell = end_cells[0]
 #        end_cell_idx = end_cell['index']

 #        cell_vars = extract_variables(self.notebook_path, cell_idx=end_cell_idx - 1)
 #        cell_texts = extract_cell_content_and_outputs(self.notebook_path, begin_cell_idx, end_cell_idx)

 #        # search for shape, 200, 43
 #        search_shape, _ = search_in_extracted_content(cell_texts, "shape")
 #        search_200, _ = search_in_extracted_content(cell_texts, "200")
 #        search_43, _ = search_in_extracted_content(cell_texts, "43")

 #        found_shape_fn = search_shape
 #        found_shape_val = search_200 and search_43

 #        print("Found shape function: ", found_shape_fn)
 #        print("Found shape values: ", found_shape_val)

 #        if found_shape_val:
 #            set_score(0.5)
 #            if found_shape_fn:
 #                set_score(1.0)
 #        else:
 #            set_score(0.0)

 #    @partial_credit(1.0)
 #    @number("2.3")
 #    def test_linear_thingz_1_1_2(self, set_score=None):
 #        print('')


 #        begin_cells = find_cells_with_text(self.notebook_path, "**1.1.2:** *In one line of code, list the **names** of all the **features** in the dataframe.*")
 #        begin_cell = begin_cells[0]
 #        begin_cell_idx = begin_cell['index']

 #        end_cells = find_cells_with_text(self.notebook_path, "**1.1.3:** *In one line of code, create a **new dataframe** called **new_df** that **contains all** the features of the **old** dataframe **except the following**:*")
 #        end_cell = end_cells[0]
 #        end_cell_idx = end_cell['index']

 #        cell_texts = extract_cell_content_and_outputs(self.notebook_path, begin_cell_idx, end_cell_idx)

 #        search_columns, _ = search_in_extracted_content(cell_texts, "columns")

 #        search_feature_year, _ = search_in_extracted_content(cell_texts, "year")
 #        search_feature_housesDestroyedAmountOrderTotal, _ = search_in_extracted_content(cell_texts, "housesDestroyedAmountOrderTotal")
 #        search_feature_damageMillionsDollarsTotal, _ = search_in_extracted_content(cell_texts, "damageMillionsDollarsTotal")
 #        search_feature = search_feature_year and search_feature_housesDestroyedAmountOrderTotal and search_feature_damageMillionsDollarsTotal


 #        found_columns_fn = search_columns
 #        found_features_name = search_feature

 #        print("Found columns function: ", found_columns_fn)
 #        print("Found features names: ", found_features_name)


 #        if found_features_name:
 #            set_score(0.5)
 #            if found_columns_fn:
 #                set_score(1.0)
 #        else:
 #            set_score(0.0)


 #    @partial_credit(1.0)
 #    @number("2.4")
 #    def test_linear_thingz_1_1_3(self, set_score=None):
 #        print('')

 #        begin_cells = find_cells_with_text(self.notebook_path, "**1.1.3:** *In one line of code, create a **new dataframe** called **new_df** that **contains all** the features of the **old** dataframe **except the following**:*")
 #        begin_cell = begin_cells[0]
 #        begin_cell_idx = begin_cell['index']

 #        end_cells = find_cells_with_text(self.notebook_path, "#### **TASK 1.2: 1 Liner Shenaniganz (7 points)**")
 #        end_cell = end_cells[0]
 #        end_cell_idx = end_cell['index']

 #        cell_vars = extract_variables(self.notebook_path, cell_idx=end_cell_idx - 1)
 #        cell_texts = extract_cell_content_and_outputs(self.notebook_path, begin_cell_idx, end_cell_idx)
 #        search_drop, _ = search_in_extracted_content(cell_texts, "drop")

 #        new_df = cell_vars.get("new_df", None)

 #        excluded_columns = [
 #            'volcanoLocationNum', 'location', 'latitude', 'longitude', 'agent', 
 #            'significant', 'publish', 'eruption', 'status', 'timeErupt', 'damageAmountOrder', 
 #            'damageAmountOrderTotal', 'housesDestroyedAmountOrder', 'housesDestroyedAmountOrderTotal', 
 #            'housesDestroyed', 'housesDestroyedTotal', 'missingAmountOrder', 'missingAmountOrderTotal', 
 #            'missing', 'missingTotal', 'damageMillionsDollars', 'damageMillionsDollarsTotal', 
 #            'injuries', 'injuriesAmountOrder', 'injuriesTotal', 'injuriesAmountOrderTotal', 
 #            'deathsAmountOrderTotal', 'deathsAmountOrder'
 #        ]

 #        # Calculate flag: True if all required columns are present in new_df, False otherwise

 #        exists_new_df = (new_df is not None) and (type(new_df) == pd.DataFrame)

 #        if exists_new_df:
 #            excluded_columns = not any(col in new_df.columns for col in excluded_columns)
 #        else:
 #            excluded_columns = False


 #        print("Exists new_df: ", exists_new_df)
 #        print("Excluded columns correctly: ", excluded_columns)
 #        print("Used drop function: ", search_drop)

 #        set_score(0.0)
 #        if exists_new_df:
 #            if excluded_columns:
 #                set_score(0.5)
 #                if search_drop:
 #                    set_score(1.0)
 #        




 #    @partial_credit(2.0)
 #    @number("2.5")
 #    def test_Liner_Shenaniganz_1_2_1(self, set_score=None):
 #        print('')

 #        begin_cells = find_cells_with_text(self.notebook_path, "#### **TASK 1.2: 1 Liner Shenaniganz (7 points)**")
 #        begin_cell = begin_cells[0]
 #        begin_cell_idx = begin_cell['index']

 #        end_cells = find_cells_with_text(self.notebook_path, "**1.2.2:** *In one line of code, **reset** the **index column** of the dataframe so that it has **1-based indexing**.*")
 #        end_cell = end_cells[0]
 #        end_cell_idx = end_cell['index']

 #        cell_vars = extract_variables(self.notebook_path, cell_idx=end_cell_idx - 1)
 #        cell_texts = extract_cell_content_and_outputs(self.notebook_path, begin_cell_idx, end_cell_idx)

 #        search_dropna, _ = search_in_extracted_content(cell_texts, "dropna")
 #        new_df = cell_vars.get("new_df", None)

 #        exists_new_df = (new_df is not None) and (type(new_df) == pd.DataFrame)
 #            
 #        contains_nan = True
 #        if exists_new_df:
 #            # Check whether new_df contains NaN in any of the "year", "month", "day" columns
 #            contains_nan = new_df[['year', 'month', 'day']].isna().any().any()

 #        print("Exists new_df: ", exists_new_df)
 #        print("Contains NaN: ", contains_nan)
 #        print("Used dropna function: ", search_dropna)  

 #        set_score(0.0)
 #        if exists_new_df:
 #            if search_dropna:
 #                set_score(1.0)

 #            if not contains_nan:
 #                set_score(2.0)

 #    @partial_credit(2.0)
 #    @number("2.6")
 #    def test_Liner_Shenaniganz_1_2_2(self, set_score=None):
 #        print('')

 #        begin_cells = find_cells_with_text(self.notebook_path, "**1.2.2:** *In one line of code, **reset** the **index column** of the dataframe so that it has **1-based indexing**.*")
 #        begin_cell = begin_cells[0]
 #        begin_cell_idx = begin_cell['index']

 #        end_cells = find_cells_with_text(self.notebook_path, "**1.2.3:** *In one line of code, make a **new column** called **'totalDeaths'** that takes the **max** of the values given between")
 #        end_cell = end_cells[0]
 #        end_cell_idx = end_cell['index']

 #        cell_vars_prev = extract_variables(self.notebook_path, cell_idx=begin_cell_idx)
 #        cell_vars = extract_variables(self.notebook_path, cell_idx=end_cell_idx - 1)

 #        new_df = cell_vars.get("new_df", None)
 #        new_df_prev = cell_vars_prev.get("new_df", None)

 #        exists_new_df = (new_df is not None) and (type(new_df) == pd.DataFrame)

 #        min_idx_prev = new_df_prev.index.min()
 #        max_idx_prev = new_df_prev.index.max()

 #        min_idx = new_df.index.min()
 #        max_idx = new_df.index.max()
 #        len_idx = len(new_df.index)


 #        min_idx_changed = min_idx != min_idx_prev
 #        max_idx_changed = max_idx != max_idx_prev

 #        idx_changed = min_idx_changed or max_idx_changed
 #        idx_reindexd = (min_idx == 1) and (len_idx == max_idx)
 # 
 #        print("Exists new_df: ", exists_new_df)
 #        print("Index changed: ", idx_changed)
 #        print("Indexing is 1-based: ", idx_reindexd)

 #        set_score(0.0)
 #        if exists_new_df:
 #            if idx_changed:
 #                set_score(1.0)
 #            if idx_reindexd:
 #                set_score(2.0)

 #    @partial_credit(3.0)
 #    @number("2.7")
 #    def test_Liner_Shenaniganz_1_2_3(self, set_score=None):
 #        print('')

 #        begin_cells = find_cells_with_text(self.notebook_path, "**1.2.3:** *In one line of code, make a **new column** called **'totalDeaths'** that takes the **max** of the values given between")
 #        begin_cell = begin_cells[0]
 #        begin_cell_idx = begin_cell['index']

 #        end_cells = find_cells_with_text(self.notebook_path, "#### **TASK 1.3: Tailoring Time (10 Points)**")
 #        end_cell = end_cells[0]
 #        end_cell_idx = end_cell['index']

 #        cell_vars = extract_variables(self.notebook_path, cell_idx=end_cell_idx - 1)

 #        new_df = cell_vars.get("new_df", None)

 #        exists_new_df = (new_df is not None) and (type(new_df) == pd.DataFrame)

 #        has_totalDeaths = "totalDeaths" in new_df.keys()

 #        totalDeaths_gt = new_df[['deathsTotal', 'deaths']].max(axis=1, skipna=True)
 #        totalDeaths = new_df["totalDeaths"]

 #        correct_totalDeaths = (totalDeaths_gt.equals(totalDeaths))

 #        print("Exists new_df: ", exists_new_df)
 #        print("Has totalDeaths: ", has_totalDeaths)
 #        print("Correct totalDeaths: ", correct_totalDeaths)

 #        set_score(0.0)
 #        if exists_new_df:
 #            if has_totalDeaths:
 #                set_score(1.0)
 #                if correct_totalDeaths:
 #                    set_score(3.0)

 #    @partial_credit(10.0)
 #    @number("2.8")
 #    def test_Tailoring_Time_1_3(self, set_score=None):
 #        print('')

 #        begin_cells = find_cells_with_text(self.notebook_path, "#### **TASK 1.3: Tailoring Time (10 Points)**")
 #        begin_cell = begin_cells[0]
 #        begin_cell_idx = begin_cell['index']

 #        end_cells = find_cells_with_text(self.notebook_path, "**Part 2: Volcanic Matryoshkas")
 #        end_cell = end_cells[0]
 #        end_cell_idx = end_cell['index']

 #        cell_vars = extract_variables(self.notebook_path, cell_idx=end_cell_idx - 1)

 #        new_df = cell_vars.get("new_df", None)

 #        exists_new_df = (new_df is not None) and (type(new_df) == pd.DataFrame)

 #        date_column_exists = "date" in new_df.keys()

 #        def check_date_format(df, column_name):
 #            correct_format = []
 #            for date in df[column_name]:
 #                try:
 #                    # Check if it can be converted to datetime
 #                    pd.to_datetime(date, format='%Y-%m-%d', errors='raise')
 #                    correct_format.append(True)
 #                except (ValueError, TypeError):
 #                    correct_format.append(False)
 #            return correct_format

 #        date_column_correct_format = all(check_date_format(new_df, "date"))

 #        year_column_exists = "year" in new_df.keys()
 #        month_column_exists = "month" in new_df.keys()
 #        day_column_exists = "day" in new_df.keys()

 #        date_column_next_to_id = new_df.keys()[1] == "date"

 #        print("Exists new_df: ", exists_new_df)
 #        print("Date column exists: ", date_column_exists)
 #        print("Date column has correct format: ", date_column_correct_format)
 #        print("Date column next to id: ", date_column_next_to_id)
 #        print("Year column exists: ", year_column_exists)
 #        print("Month column exists: ", month_column_exists)
 #        print("Day column exists: ", day_column_exists)

 #        total_score = 0.0

 #        if exists_new_df:
 #            if date_column_exists:
 #                total_score = 10.0

 #                if month_column_exists or year_column_exists or day_column_exists:
 #                    total_score -= 2.0

 #                if not date_column_correct_format:
 #                    total_score -= 3.0

 #                if not date_column_next_to_id:
 #                    total_score -= 3.0

 #        set_score(total_score)
