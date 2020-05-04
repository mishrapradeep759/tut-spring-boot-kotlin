import math

from xlrd import XL_CELL_NUMBER, open_workbook


def parse_xlsx(_file, header=False, row_dict=False, int_as_str=True):

    # check if file is an InMemoryFile
    if hasattr(_file, "read"):

        # open InMemory excel file as workbook
        workbook = open_workbook(filename=None, file_contents=_file.read())

    else:

        # open excel file from file system as workbook
        workbook = open_workbook(_file)

    # get sheets in excel workbook
    sheets = workbook.sheet_names()

    # select first sheet containg records
    active_sheet = workbook.sheet_by_name(sheets[0])

    # get number of rows in selected sheet
    num_rows = active_sheet.nrows

    # get number of column in selected sheet
    num_cols = active_sheet.ncols

    # get header row from selected sheet
    _header = [active_sheet.cell_value(0, cell) for cell in range(num_cols)]

    # loop through each row in sheet
    for row_idx in range(0 if header and not row_dict else 1, num_rows):

        # get all columns data in current loop row
        row_cell = [
            str(int(active_sheet.cell_value(row_idx, col_idx)))
            if active_sheet.cell(row_idx, col_idx).ctype == XL_CELL_NUMBER
            and math.ceil(active_sheet.cell_value(row_idx, col_idx))
            == active_sheet.cell_value(row_idx, col_idx)
            and int_as_str
            else active_sheet.cell_value(row_idx, col_idx)
            for col_idx in range(num_cols)
        ]

        # zip current loop row with header and convert to dictionary and yield final result
        yield dict(zip(_header, row_cell)) if row_dict else row_cell
