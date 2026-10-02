# Helper functions to change database rows into python dictionaries

def row_to_dict(cursor, row):
    # check if row is empty
    if row is None:
        return None
    if cursor.description is None:
        return None
        
    # get column names from cursor description
    column_names = []
    for col in cursor.description:
        column_names.append(col[0].lower())
        
    # make a dictionary for the row
    row_dict = {}
    for i in range(len(column_names)):
        col_name = column_names[i]
        row_dict[col_name] = row[i]
        
    return row_dict

def rows_to_dicts(cursor, rows):
    # check if cursor description exists
    if cursor.description is None:
        return []
        
    # get column names
    column_names = []
    for col in cursor.description:
        column_names.append(col[0].lower())
        
    # convert all rows into list of dictionaries
    result_list = []
    for row in rows:
        row_dict = {}
        for i in range(len(column_names)):
            col_name = column_names[i]
            row_dict[col_name] = row[i]
        result_list.append(row_dict)
        
    return result_list


