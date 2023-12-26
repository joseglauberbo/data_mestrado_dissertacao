import csv
from csv import reader, writer
import os 

field_names_infos_per_cen_conflicts = ['repository', 'rename', 'move', 'inline', 'extract',
                                       'internal_move', 'extract_move',
                                       'move_rename', 'internal_move_rename']

rename_file = 0
move_file = 0 
inline_file = 0
extract_file = 0
internal_move_file = 0
extract_move_file = 0
move_rename_file = 0
internal_move_rename_file = 0
arrayWithDictionarysRefactorings = []

rename_rc = 0
move_rc = 0 
inline_rc = 0
extract_rc = 0
internal_move_rc = 0
extract_move_rc = 0
move_rename_rc = 0
internal_move_rename_rc = 0
arrayWithDictionarysRefactoringsRC = []

with open('type_refactorings.csv', 'r+', encoding="utf8", errors='ignore') as file_obj:

    currentDirectory = os.getcwd()
    currentDirectory = currentDirectory.split('/')
    currentDirectory = currentDirectory[-1]

    # Create reader object by passing the file
    # object to reader method
    reader_obj = reader((line.replace('\0', '')
                        for line in file_obj), delimiter=",")
    writer_obj = writer(file_obj, quoting=csv.QUOTE_ALL)

    # Iterate over each row in the csv
    # file using reader object
    for row in reader_obj:

        result = row[4].split('[')
        result = result[-1]
        result2 = result.split(']')
        result2 = result2[0]
        result3 = result2.split(', ')

        # file
        for object in result3:

            if (object == "'RENAME'"):
                rename_file += 1
            if (object == "'MOVE'"):
                move_file += 1
            if (object == "'INLINE'"):
                inline_file += 1
            if (object == "'EXTRACT'"):
                extract_file += 1
            if (object == "'INTERNAL_MOVE'"):
                internal_move_file += 1
            if (object == "'EXTRACT_MOVE'"):
                extract_move_file += 1
            if (object == "'MOVE_RENAME'"):
                move_rename_file += 1
            if (object == "'INTERNAL_MOVE_RENAME'"):
                internal_move_rename_file += 1
        
        my_dict_relation = {}
        my_dict_relation['repository'] = currentDirectory
        my_dict_relation['rename'] = rename_file
        my_dict_relation['move'] = move_file
        my_dict_relation['inline'] = inline_file
        my_dict_relation['extract'] = extract_file
        my_dict_relation['internal_move'] = internal_move_file
        my_dict_relation['extract_move'] = extract_move_file
        my_dict_relation['move_rename'] = move_rename_file
        my_dict_relation['internal_move_rename'] = internal_move_rename_file
        arrayWithDictionarysRefactorings.append(my_dict_relation)

        with open('occurenciesFile.csv', 'w') as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=field_names_infos_per_cen_conflicts)
            writer.writeheader()
            writer.writerows(arrayWithDictionarysRefactorings)
        
        result4 = row[5].split('[')
        result4 = result4[-1]
        result5 = result4.split(']')
        result5 = result5[0]
        result6 = result5.split(', ')
        
        for object in result6:

            if (object == "'RENAME'"):
                rename_rc += 1
            if (object == "'MOVE'"):
                move_rc += 1
            if (object == "'INLINE'"):
                inline_rc += 1
            if (object == "'EXTRACT'"):
                extract_rc += 1
            if (object == "'INTERNAL_MOVE'"):
                internal_move_rc += 1
            if (object == "'EXTRACT_MOVE'"):
                extract_move_rc += 1
            if (object == "'MOVE_RENAME'"):
                move_rename_rc += 1
            if (object == "'INTERNAL_MOVE_RENAME'"):
                internal_move_rename_rc += 1
        
        my_dict_relationRC = {}
        my_dict_relationRC['repository'] = currentDirectory
        my_dict_relationRC['rename'] = rename_rc
        my_dict_relationRC['move'] = move_rc
        my_dict_relationRC['inline'] = inline_rc
        my_dict_relationRC['extract'] = extract_rc
        my_dict_relationRC['internal_move'] = internal_move_rc
        my_dict_relationRC['extract_move'] = extract_move_rc
        my_dict_relationRC['move_rename'] = move_rename_rc
        my_dict_relationRC['internal_move_rename'] = internal_move_rename_rc
        arrayWithDictionarysRefactoringsRC.append(my_dict_relationRC)

        with open('occurenciesFileRC.csv', 'w') as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=field_names_infos_per_cen_conflicts)
            writer.writeheader()
            writer.writerows(arrayWithDictionarysRefactoringsRC)
