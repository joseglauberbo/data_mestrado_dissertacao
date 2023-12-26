from csv import reader, writer
import csv

field_names = ['evolutionary_commit', 'merge_commit',
               'left', 'right', 'local_node_before', 'local_node_after', 'local_refactoring_before', 'local_refactoring_after', 'region_conflict_before',
               'region_conflict_after', 'region_refactoring_before', 'region_refactoring_after', 'there_are_refactors_file', 'there_are_refactors_region_conflict', 'refactor_type']

field_names_refactoring = ['qt_refactorings_arq', 'qt_refactorings_region_conflict', 
                           'qt_type_refactorings_arq', 'qt_type_refactorings_region_conflict',
                           'occur_type_refactorings_arq', 'occur_type_refactorings_region_conflict']
arrayWithDictionarys = []
arrayWithRefactorings = []

evolutionary_linhas = open('evolutionary.csv').readlines()
refactorings_linhas = open('refactorings.csv').readlines()

cont_cenarios_merge_region_conflict_file = []
cont_cenarios_merge_region_conflict = []
cont_commits_evolucionarios_refactoring_type_region_conflict_file = []
cont_refactoring_region_conflict_region_change = 0
array_local = []
type_refactoring_region_conflict = []

occurence = []
there_are_refactoring_file = False
there_are_refactoring_region_conflict = False
qt_refactoring_arq = []
type_refactoring_arq = []
occ_type_refactoring_arq = []
qt_refactoring_region_conflict = []
type_refactoring_region_conflict = []
occ_type_refactoring_region_conflict = []

for evolutionary in evolutionary_linhas:

    evolutionary = evolutionary.split(',')

    for refactorings in refactorings_linhas:
        refactorings = refactorings.split(',')

        if (evolutionary[0] == refactorings[0]):


            there_are_refactoring_file = False
            there_are_refactoring_region_conflict = False

            occurence.append(evolutionary[0])

            ##### COMMIT EVOLUCIONARIO #####

            # local da mudança no commit evolucionario
            local_before = evolutionary[5]
            local_before_plus = evolutionary[6]

            local_after = evolutionary[7]
            local_after_plus = evolutionary[8]

            source_before = evolutionary[9]
            source_before = source_before.split('\n')
            source_before = source_before[0]
            source_before = source_before[2:]

            source_after = evolutionary[10]
            source_after = source_after.split('\n')
            source_after = source_after[0]
            source_after = source_after[2:]

            ##### COMMIT REFACTORING #####
            # local da aplicação do refactoring
            source_refactoring_before = refactorings[2]
            source_refactoring_after = refactorings[3]

            # formatando local da aplicação do refactoring
            source_refactoring_before = source_refactoring_before.split(' ')
            source_refactoring_before = source_refactoring_before[-1]
            source_refactoring_before = source_refactoring_before.split('}')
            source_refactoring_before = source_refactoring_before[0]
            source_refactoring_before = source_refactoring_before.split(':')
            local_refactoring_before = source_refactoring_before[-1]
            source_refactoring_before = source_refactoring_before[0]

            source_refactoring_after = source_refactoring_after.split(' ')
            source_refactoring_after = source_refactoring_after[-1]
            source_refactoring_after = source_refactoring_after.split('}')
            source_refactoring_after = source_refactoring_after[0]
            source_refactoring_after = source_refactoring_after.split(':')
            local_refactoring_after = source_refactoring_after[-1]
            source_refactoring_after = source_refactoring_after[0]

            # verificar se o caminho do arquivo é o mesmo, caso seja adiciono e verifico a região de mudança
            if (source_before == source_refactoring_before or source_after == source_refactoring_after):

                occ_type_refactoring_arq.append(refactorings[1])

                if (refactorings not in qt_refactoring_arq):
                    qt_refactoring_arq.append(refactorings)
                
                if (refactorings[1] not in type_refactoring_arq):
                    type_refactoring_arq.append(refactorings[1])

                there_are_refactoring_file = True

                # existe refactoring realizado dentro do mesmo arquivo que construiu as regiões de conflito.
                if (evolutionary[1] not in cont_cenarios_merge_region_conflict_file):

                    cont_cenarios_merge_region_conflict_file.append(
                        evolutionary[1])

                if (refactorings[1] not in cont_commits_evolucionarios_refactoring_type_region_conflict_file):
                    cont_commits_evolucionarios_refactoring_type_region_conflict_file.append(
                        refactorings[1])

                # existe no mesmo arquivo, porém é interessente avaliar a região de conflito

                ##### REGIÃO DO CÓDIGO ENVOLVIDO NO CONFLITO ANTES DO COMMIT EVOLUCIONARIO  #####
                # formatando a região de mudança que representa a mudança antes do conflito
                region_change_before_begin = evolutionary[5]
                region_change_before_begin = region_change_before_begin.split(
                    '"')

                if (region_change_before_begin[1][0] == '-'):
                    region_change_before_begin = region_change_before_begin[1].split(
                        '-')
                    region_change_before_begin[0] = '-'
                if (region_change_before_begin[1][0] == '+'):
                    region_change_before_begin = region_change_before_begin[1].split(
                        '+')
                    region_change_before_begin[0] = '+'

                region_change_before_dimension = evolutionary[6]

                region_change_before_dimension = region_change_before_dimension.split(
                    '"')
                region_change_before_dimension = int(
                    region_change_before_dimension[0])
                region_change_before_begin[1] = int(
                    region_change_before_begin[1])

                interval_change_before = region_change_before_dimension + \
                    region_change_before_begin[1] - 1

                
                # formatando o local onde o refactoring foi realizado
                region_refactoring_before = refactorings[2]
                region_refactoring_before = region_refactoring_before.split(
                    ':')
                region_refactoring_before = region_refactoring_before[1].split(
                    '}')
                region_refactoring_before = region_refactoring_before[0]
                region_refactoring_before = int(region_refactoring_before)

                ##### COMMIT EVOLUCIONARIO REGIÃO DE MUDANÇA REFERENTE DEPOIS DO CONFLITO #####
                # formatando a região de mudança que representa a mudança depois do conflito
                region_change_after_begin = evolutionary[7]
                region_change_after_begin = region_change_after_begin.split(
                    '"')

                if (region_change_after_begin[1][0] == '-'):
                    region_change_after_begin = region_change_after_begin[1].split(
                        '-')
                    region_change_after_begin[0] = '-'
                if (region_change_after_begin[1][0] == '+'):
                    region_change_after_begin = region_change_after_begin[1].split(
                        '+')
                    region_change_after_begin[0] = '+'

                region_change_after_dimension = evolutionary[8]

                region_change_after_dimension = region_change_after_dimension.split(
                    '"')
                region_change_after_dimension = int(
                    region_change_after_dimension[0])
                region_change_after_begin[1] = int(
                    region_change_after_begin[1])

                interval_change_after = region_change_after_dimension + \
                    region_change_after_begin[1] - 1

                # formatando o local onde o refactoring está depois da refatoração
                region_refactoring_after = refactorings[3]
                region_refactoring_after = region_refactoring_after.split(':')
                region_refactoring_after = region_refactoring_after[1].split(
                    '}')
                region_refactoring_after = region_refactoring_after[0]
                region_refactoring_after = int(region_refactoring_after)

                # verificando se o refactoring está dentro da região de conflito anterior

                if (region_change_after_begin[1] <= region_refactoring_after and region_refactoring_after <= interval_change_after or 
                    region_change_after_begin[1] <= region_refactoring_before and region_refactoring_before <= interval_change_after or 
                    region_change_before_begin[1] <= region_refactoring_after and region_refactoring_after <= interval_change_before or 
                    region_change_before_begin[1] <= region_refactoring_before and region_refactoring_before <= interval_change_before):

                    occ_type_refactoring_region_conflict.append(refactorings[1]) 

                    if (refactorings not in qt_refactoring_region_conflict):
                        qt_refactoring_region_conflict.append(refactorings)

                    if (refactorings[1] not in type_refactoring_region_conflict):
                        type_refactoring_region_conflict.append(refactorings[1])

                    cont_refactoring_region_conflict_region_change = cont_refactoring_region_conflict_region_change + 1
                    there_are_refactoring_region_conflict = True

                    if (evolutionary[1] not in cont_cenarios_merge_region_conflict):
                        cont_cenarios_merge_region_conflict.append(
                            evolutionary[1])

                    if (refactorings[1] not in type_refactoring_region_conflict):
                        type_refactoring_region_conflict.append(
                            refactorings[1])

                    if (evolutionary[0] not in array_local):
                        array_local.append(evolutionary[0])

                my_dict_evolutionary_commit = {
                    'evolutionary_commit': '', 'merge_commit': '', 'left': '', 'right': ''}
                my_dict_evolutionary_commit['evolutionary_commit'] = evolutionary[0]
                my_dict_evolutionary_commit['merge_commit'] = evolutionary[1]
                my_dict_evolutionary_commit['left'] = evolutionary[2]
                my_dict_evolutionary_commit['right'] = evolutionary[3]
                my_dict_evolutionary_commit['local_node_before'] = source_before
                my_dict_evolutionary_commit['local_node_after'] = source_after
                my_dict_evolutionary_commit['local_refactoring_before'] = source_refactoring_before
                my_dict_evolutionary_commit['local_refactoring_after'] = source_refactoring_after
                my_dict_evolutionary_commit['region_conflict_before'] = [
                    region_change_before_begin[1], interval_change_before]
                my_dict_evolutionary_commit['region_conflict_after'] = [
                    region_change_after_begin[1], interval_change_after]
                my_dict_evolutionary_commit['region_refactoring_before'] = region_refactoring_before
                my_dict_evolutionary_commit['region_refactoring_after'] = region_refactoring_after
                my_dict_evolutionary_commit['there_are_refactors_file'] = there_are_refactoring_file
                my_dict_evolutionary_commit['refactor_type'] = refactorings[1]
                my_dict_evolutionary_commit['there_are_refactors_region_conflict'] = there_are_refactoring_region_conflict
                arrayWithDictionarys.append(my_dict_evolutionary_commit)

                with open('result.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerows(arrayWithDictionarys)

my_dict_refactorings = {
                    'qt_refactorings_arq': '', 'qt_refactorings_region_conflict': '', 
                    'qt_type_refactorings_arq': '', 'qt_type_refactorings_region_conflict': '',
                    'occur_type_refactorings_arq': '', 'occur_type_refactorings_region_conflict': ''}

my_dict_refactorings['qt_refactorings_arq'] = len(qt_refactoring_arq)
my_dict_refactorings['qt_refactorings_region_conflict'] = len(qt_refactoring_region_conflict)
my_dict_refactorings['qt_type_refactorings_arq'] = len(type_refactoring_arq)
my_dict_refactorings['qt_type_refactorings_region_conflict'] = len(type_refactoring_region_conflict)
my_dict_refactorings['occur_type_refactorings_arq'] = occ_type_refactoring_arq
my_dict_refactorings['occur_type_refactorings_region_conflict'] = occ_type_refactoring_region_conflict
arrayWithRefactorings.append(my_dict_refactorings)

with open('type_refactorings.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names_refactoring)
    writer.writeheader()
    writer.writerows(arrayWithRefactorings)
