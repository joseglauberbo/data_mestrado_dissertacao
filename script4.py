import csv
from csv import reader, writer

field_names_infos_per_cen_conflicts = ['merge', 'left', 'right', 'arquivos_conflitos_analisados', 'arquivos_conflitos_nao_analisados',
                                       'quantidade_total_de_conflitos_validos_js', 'quantidade_regioes_de_conflito_total',
                                       'quantidade_regioes_de_conflito_total_valido_js', 'qt_relations_arq', 'qt_relations_region_conflict']
arrayWithDictionarysRelations = []
relations_linhas = open('result.csv').readlines()

qt_relations = 0
qt_relations_region_conflict = 0

with open('conflicts_per_cenario.csv', 'r+', encoding="utf8", errors='ignore') as file_obj:

    # Create reader object by passing the file
    # object to reader method
    reader_obj = reader((line.replace('\0', '')
                        for line in file_obj), delimiter=",")
    writer_obj = writer(file_obj, quoting=csv.QUOTE_ALL)

    # Iterate over each row in the csv
    # file using reader object
    for row in reader_obj:

        qt_relations = 0
        qt_relations_region_conflict = 0

        for relations in relations_linhas:
            relations = relations.split(',')

            if ((relations[1] == row[0]) and (relations[2] == row[1]) and (relations[3] == row[2])):
                print('essa relação pertence a esse cenário à nível de arquivo')
                qt_relations = qt_relations + 1

                if (relations[15] == 'True'):
                    print('essa relação pertence a esse cenário à nível de região de conflito')
                    qt_relations_region_conflict = qt_relations_region_conflict + 1                    

        my_dict_relation = {}
        my_dict_relation['merge'] = row[0]
        my_dict_relation['left'] = row[1]
        my_dict_relation['right'] = row[2]
        my_dict_relation['arquivos_conflitos_analisados'] = row[3]
        my_dict_relation['arquivos_conflitos_nao_analisados'] = row[4]
        my_dict_relation['quantidade_total_de_conflitos_validos_js'] = row[5]
        my_dict_relation['quantidade_regioes_de_conflito_total'] = row[6]
        my_dict_relation['quantidade_regioes_de_conflito_total_valido_js'] = row[7]
        my_dict_relation['qt_relations_arq'] = qt_relations
        my_dict_relation['qt_relations_region_conflict'] = qt_relations_region_conflict
        arrayWithDictionarysRelations.append(my_dict_relation)

        with open('resultFinal.csv', 'w') as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=field_names_infos_per_cen_conflicts)
            writer.writeheader()
            writer.writerows(arrayWithDictionarysRelations)